---
title: "SQL ALTER TABLE & TRUNCATE TABLE: Schema Migrations, Lock Queues & HWM Reset"
slug: "sql-alter-truncate-table"
subject: "sql"
vertical: "notes"
category: "2. Database & Table Management"
order: 5
tier: "free"
price_inr: 0
reading_time: "8 min read"
description: "Deep dive into SQL ALTER and TRUNCATE: why ALTER TABLE causes production connection exhaustion, instant metadata DDL vs heap rewrites, and TRUNCATE High-Water Mark reset."
tags: ["SQL", "DDL", "Database Administration", "Performance", "Transactions", "PostgreSQL", "MySQL"]
status: "published"
last_updated: "2026-11-21"
---

## 1. Academic Definition & Core Syntax

In standard Data Definition Language (DDL), **`ALTER TABLE`** modifies an existing table structure without destroying stored rows, while **`TRUNCATE TABLE`** empties all records from a table:

```sql
-- Adding and dropping columns
ALTER TABLE students ADD COLUMN enrolled_at TIMESTAMP;
ALTER TABLE students DROP COLUMN legacy_notes;

-- Modifying column definitions (Syntax varies by engine)
-- PostgreSQL syntax:
ALTER TABLE students ALTER COLUMN phone TYPE VARCHAR(20);
-- MySQL syntax:
ALTER TABLE students MODIFY COLUMN phone VARCHAR(20) NOT NULL;

-- Fast table wipe
TRUNCATE TABLE student_audit_logs;
```

While syntactically straightforward, executing these statements naively against large production tables is a leading cause of severe database outages.

---

## 2. What Textbooks Skip: The `ACCESS EXCLUSIVE` Lock Trap

Standard classroom tutorials teach that `ALTER TABLE` completes in a few milliseconds. In production under active query load, `ALTER TABLE` can bring down the entire application.

### The Lock Acquisition Queue Problem
Relational engines (such as PostgreSQL and MySQL) require an exclusive metadata lock (**`ACCESS EXCLUSIVE`** in PostgreSQL, **`Exclusive Metadata Lock`** in MySQL) to alter table structure. This lock blocks all concurrent reads (`SELECT`) and writes (`INSERT`, `UPDATE`, `DELETE`).

```
Time ──►
Conn 1: [Long SELECT Query running: 15s .........................]
Conn 2:           [ALTER TABLE ADD COLUMN ...]  ◄── BLOCKED! Waiting for Conn 1
Conn 3:                    [SELECT * FROM ...]   ◄── BLOCKED! Waiting behind ALTER
Conn 4:                    [INSERT INTO ...]     ◄── BLOCKED! Waiting behind ALTER
Conn 5:                    [SELECT * FROM ...]   ◄── BLOCKED! Waiting behind ALTER
Result: Connection pool exhausted (Max 100/100). Entire website returns HTTP 504.
```

Even if `ALTER TABLE` itself takes only **2 milliseconds**, it cannot start until every prior read on that table finishes. Crucially, **all incoming requests queue behind the waiting `ALTER`**, causing connection pool saturation within seconds.

### The Production Migration Pattern
Always set a strict lock timeout before running DDL migrations in production. If the lock cannot be acquired immediately, fail fast instead of holding up the connection queue:

```sql
-- PostgreSQL Zero-Downtime Migration Pattern
BEGIN;
-- Fail if lock is not acquired within 2 seconds
SET LOCAL lock_timeout = '2s';

ALTER TABLE students ADD COLUMN national_id VARCHAR(32);
COMMIT;
```

---

## 3. Instant DDL vs. Table Heap Rewrites

Not all `ALTER TABLE` operations execute with equal performance. Engines process changes through two distinct physical mechanisms:

```
┌─────────────────────────────────┬─────────────────────────────────┐
│ Metadata-Only (Instant DDL)      │ Table Rewrite (Full Heap Copy)  │
├─────────────────────────────────┼─────────────────────────────────┤
│ Updates system catalog tables.  │ Reads every 8KB disk page,      │
│ Execution time: < 5ms.          │ writes new pages, rebuilds all  │
│ Zero disk I/O, zero bloat.      │ indexes. High I/O, hours long.  │
└─────────────────────────────────┴─────────────────────────────────┘
```

### 1. Adding a Nullable Column
Adding a nullable column with no default (`ADD COLUMN bio TEXT`) is purely metadata-only in PostgreSQL and MySQL 8.0. The engine merely appends an entry to `pg_attribute` or `information_schema.columns`.

### 2. Adding a Column with a Default Value
* **Legacy MySQL / Old Postgres (< v11)**: Required reading and rewriting every row on disk to physically write the default value. On a 50-million row table, this locked writes for hours.
* **Modern Engines (Postgres 11+, MySQL 8.0 `ALGORITHM=INSTANT`)**: Supports **Fast Default**. The default value is stored in the catalog metadata. Existing rows evaluate the default lazily when read, requiring zero disk rewrite.

### 3. Altering Data Types
Widening or converting types represents the highest risk:

```sql
-- SAFE in Postgres (Metadata-only operation):
-- Widening unconstrained VARCHAR or VARCHAR(20) to VARCHAR(100)
ALTER TABLE students ALTER COLUMN name TYPE VARCHAR(100);

-- DANGEROUS in Postgres (Full table rewrite + full index rebuild):
-- Narrowing VARCHAR(100) to VARCHAR(50) (must validate every row)
-- Converting INT (4 bytes) to BIGINT (8 bytes) (changes binary layout)
ALTER TABLE transactions ALTER COLUMN id TYPE BIGINT;
```

---

## 4. `TRUNCATE TABLE` vs. `DELETE FROM`

Textbooks frequently state: *"TRUNCATE and DELETE both remove all records."* Under the storage engine, their physical execution physics are fundamentally different:

| Operational Dimension | `DELETE FROM table;` | `TRUNCATE TABLE table;` |
| :--- | :--- | :--- |
| **SQL Category** | DML (Data Manipulation) | DDL (Data Definition) |
| **Execution Mechanism** | Row-by-row traversal | Deallocates disk extents |
| **Lock Level** | Row-level locks (`RowExclusive`) | Table-level lock (`Exclusive`) |
| **WAL / Redo Logging** | Logs every row deletion | Logs allocation map change |
| **High-Water Mark (HWM)**| Preserved (disk space not freed)| Reset to zero (space freed) |
| **Trigger Activation** | Fires `ON DELETE` row triggers | Skips row-level triggers |

### The High-Water Mark (HWM) Trap
When you execute `DELETE FROM logs;`, the rows are marked as deleted (dead tuples), but the allocated physical disk pages are **not returned to the filesystem**:

```
Disk File Layout after DELETE:
[Page 1: Empty] [Page 2: Empty] [Page 3: Empty] ... [Page 10,000: Empty]
Sequential Scan: Engine still reads all 10,000 empty 8KB pages from disk!
```

Subsequent queries still perform sequential table scans across thousands of empty 8KB pages. Conversely, `TRUNCATE` cuts the storage allocation back to page zero, releasing storage immediately and resetting sequential scan latency to near-zero.

---

## 5. Transactional Rollback & Foreign Key Physics

### 1. Transactional DDL Differences
Can you undo a `TRUNCATE`? The answer depends entirely on your database engine:

```sql
-- In PostgreSQL: TRUNCATE is fully transactional!
BEGIN;
TRUNCATE TABLE user_cache;
-- Realized mistake:
ROLLBACK;
-- Table data is completely restored!

-- In MySQL / Oracle: TRUNCATE causes an implicit commit!
START TRANSACTION;
TRUNCATE TABLE user_cache; -- MySQL automatically commits here!
ROLLBACK;
-- Data is permanently destroyed. Rollback has no effect.
```

### 2. The Foreign Key Constraint Block
You cannot truncate a table that is referenced by an active foreign key constraint in another table, even if the referencing table is completely empty:

```sql
-- Fails with: cannot truncate a table referenced in a foreign key constraint
TRUNCATE TABLE customers;

-- PostgreSQL resolution: Truncate child tables simultaneously
TRUNCATE TABLE customers, orders CASCADE;

-- MySQL resolution: Temporarily disable constraint checks (Superuser only)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE customers;
SET FOREIGN_KEY_CHECKS = 1;
```

---

## 6. Production Quick-Reference Rules

1. **Never run bare `ALTER TABLE` on high-traffic tables**: Always wrap in a transaction with `SET LOCAL lock_timeout = '2s';`.
2. **Beware of type changes**: Changing `INT` to `BIGINT` rewrites every table page on disk. For 100M+ row tables, use zero-downtime shadow table tooling like `pg_repack` or `gh-ost`.
3. **Use `TRUNCATE` for batch resets**: Use `TRUNCATE` when emptying staging or scratch tables to reclaim disk extents and reset the High-Water Mark.
4. **Remember MySQL DDL autocommit**: Unlike PostgreSQL, MySQL auto-commits before and after every DDL command (`ALTER`, `TRUNCATE`). You cannot rollback a DDL migration in MySQL.
