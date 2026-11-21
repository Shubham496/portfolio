---
title: "SQL SELECT & SELECT DISTINCT: Execution Physics, Hash Aggregates & Projection Overhead"
slug: "sql-select-distinct"
subject: "sql"
vertical: "notes"
category: "3. Querying & Filtering"
order: 6
tier: "free"
price_inr: 0
reading_time: "8 min read"
description: "Master SQL projection and deduplication: why SELECT * breaks index-only scans, Sort Unique vs Hash Aggregate in-memory physics, and how DISTINCT handles NULL values."
tags: ["SQL", "DQL", "Query Optimization", "Performance", "Indexing", "PostgreSQL", "MySQL"]
status: "published"
last_updated: "2026-11-21"
---

## 1. Academic Definition & Core Syntax

In standard Data Query Language (DQL), **`SELECT`** retrieves specific attributes (columns) from one or more tables, while **`SELECT DISTINCT`** eliminates duplicate rows from the resulting projection:

```sql
-- Standard projection
SELECT student_id, first_name, email 
FROM students;

-- Duplicate elimination across projection
SELECT DISTINCT city, state 
FROM student_addresses;

-- Counting unique entities
SELECT COUNT(DISTINCT state) AS unique_states 
FROM student_addresses;
```

While projection appears conceptually trivial, how you write your `SELECT` list directly controls whether the database storage engine uses high-speed memory caches or expensive random disk I/O.

---

## 2. What Textbooks Skip: The True Cost of `SELECT *`

Tutorials use `SELECT *` everywhere for simplicity. In production systems, `SELECT *` is considered a critical anti-pattern for three architectural reasons:

### 1. Breaking Index-Only Scans
When a database has a secondary index on `(department_id, salary)`, the engine can satisfy this query entirely from RAM without touching the main table on disk:

```sql
-- FAST: Index-Only Scan (0 disk heap accesses)
SELECT department_id, salary 
FROM employees 
WHERE department_id = 10;
```

However, if you write `SELECT *`, the index alone cannot satisfy the query. For every matching row in the index, the engine must perform a **random I/O lookup into the table heap** to fetch the remaining unindexed columns, degrading query throughput by up to 20x.

### 2. Serialization & Network Bandwidth Saturation
Large tables frequently include text columns (`bio`, `json_metadata`, `audit_trail`). Fetching `SELECT *` over a 10,000-row batch transfers tens of megabytes over the network socket, saturating database CPU in row serialization and stalling client application deserializers.

### 3. Schema Drift & Positional Binding Breakage
If application code maps columns positionally (or downstream ETL models rely on ordinal column offsets), adding a new column to the table schema upstream silently breaks downstream ingestion pipelines.

---

## 3. Physical Execution: Sort Unique vs. Hash Aggregate

How does the database actually eliminate duplicates when you run `SELECT DISTINCT`? Relational engines execute deduplication using one of two physical algorithms:

```
┌─────────────────────────────────┬─────────────────────────────────┐
│ Hash Aggregate (O(N))           │ Sort Unique (O(N log N))        │
├─────────────────────────────────┼─────────────────────────────────┤
│ Builds in-memory hash table of  │ Sorts all candidate tuples      │
│ distinct keys. Emits unique row │ in order, then streams through  │
│ on first hash occurrence.       │ comparing adjacent rows.        │
└─────────────────────────────────┴─────────────────────────────────┘
```

### The In-Memory `work_mem` Disk Spill
In engines like PostgreSQL, deduplication occurs in allocated query memory (`work_mem`, default: 4MB). 

```
Query: SELECT DISTINCT client_ip FROM web_traffic_logs;

If distinct keys fit in work_mem (e.g. 2MB):
   Engine builds in-memory hash table -> Latency: 12ms.

If distinct keys exceed work_mem (e.g. 50MB):
   Engine switches to External Merge Disk Sort!
   Writes temporary batch files to disk -> Latency: 4,800ms.
```

When cardinality is high, exceeding `work_mem` forces the database to write temporary spill files to disk storage, causing sudden 100x latency spikes in production.

---

## 4. Multi-Column `DISTINCT` & The `NULL` Gotcha

### 1. `DISTINCT` Applies to the Entire Row Tuple
A common beginner misconception is that `DISTINCT` can apply to only one column in a multi-column projection:

```sql
-- MISCONCEPTION: Does NOT evaluate DISTINCT on first_name only!
-- Evaluates the unique combination of (first_name, department_id, city)
SELECT DISTINCT first_name, department_id, city 
FROM employees;
```

`DISTINCT` is not a function; it is a query-level modifier. It checks uniqueness across the **entire selected tuple**. If you need unique values on a single key while retrieving arbitrary columns, you must use window functions (`ROW_NUMBER()`) or engine extensions like PostgreSQL's `DISTINCT ON`:

```sql
-- PostgreSQL Specific: First record per department ordered by salary
SELECT DISTINCT ON (department_id) 
    department_id, employee_id, salary
FROM employees
ORDER BY department_id, salary DESC;
```

### 2. How `DISTINCT` Evaluates `NULL` Values
In relational logic (Three-Valued Logic / 3VL), comparing two `NULL`s with equality (`NULL = NULL`) evaluates to `UNKNOWN` (falsy).

However, under the ANSI SQL standard for `SELECT DISTINCT`, **all `NULL` values are treated as mutually equal and deduplicated into a single group**:

```sql
-- Given table with values: [10, 20, NULL, 30, NULL]
SELECT DISTINCT referral_code FROM signups;

-- Output: [10, 20, 30, NULL]
-- The multiple NULL entries collapse into exactly one NULL row.
```

---

## 5. `SELECT DISTINCT` vs. `GROUP BY`

A classic junior interview question asks: *"What is the performance difference between SELECT DISTINCT and GROUP BY without aggregate functions?"*

```sql
-- Query A:
SELECT DISTINCT department_id FROM employees;

-- Query B:
SELECT department_id FROM employees GROUP BY department_id;
```

### Production Optimizer Reality
In modern cost-based query optimizers (PostgreSQL, MySQL 8.0, Microsoft SQL Server, Oracle), **Query A and Query B produce the exact same execution plan**. Both compile into identical `HashAggregate` or `GroupAggregate` physical operators.

However, when combined with counting (`COUNT(DISTINCT column)`), performance characteristics diverge:

```sql
-- Requires an internal hash set per group to eliminate duplicates
-- Prevents pushdown to stream aggregators
SELECT department_id, COUNT(DISTINCT job_title)
FROM employees
GROUP BY department_id;
```

`COUNT(DISTINCT)` requires allocating an internal hash bucket for every distinct key per group. On massive datasets, computing exact distinct counts is heavily CPU-bound; high-scale analytics engines frequently use probabilistic estimators (such as HyperLogLog) to avoid this overhead.

---

## 6. Production Quick-Reference Rules

1. **Ban `SELECT *` from API & Backend queries**: Explicitly enumerate required columns to preserve Index-Only Scans and save network I/O.
2. **Do not use `DISTINCT` to mask broken JOINs**: If a `JOIN` produces unexpected duplicate rows, fix the join condition or relationship cardinality instead of slapping `DISTINCT` on top to hide the Cartesian multiplication.
3. **Be mindful of `DISTINCT` on high-cardinality keys**: Running `DISTINCT` over UUIDs or timestamps forces expensive sorting and potential disk spillover.
4. **Remember `NULL` deduplication**: Multiple `NULL` rows always collapse into a single `NULL` row under `DISTINCT`.
