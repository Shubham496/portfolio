"""
MYTHOS Knowledge & Resource Engine Services.
Comprehensive catalog of all major coding languages, databases, data tools,
frameworks, and DevOps software with topic-wise curriculum outlines.
"""

from __future__ import annotations

import os
import re
import math
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

import markdown
import frontmatter


# Path configuration
CONTENT_DIR = Path(__file__).resolve().parent.parent.parent / "content"


# ═══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE TECHNOLOGY CATALOG WITH STRUCTURED TOPIC CURRICULA
# ═══════════════════════════════════════════════════════════════════════════════

SUBJECT_GROUPS = {
    "all": "All Technologies",
    "languages": "Programming Languages",
    "databases": "Databases & Storage",
    "data_bi": "Data Analytics & BI",
    "frameworks": "Web Frameworks & Backends",
    "devops": "DevOps, Cloud & Systems",
    "marketing": "Growth & Marketing",
}

SUBJECTS: Dict[str, Dict[str, Any]] = {
    # ─── 1. DATABASES & STORAGE ───────────────────────────────────────────────
    "sql": {
        "slug": "sql",
        "title": "SQL & Relational Databases",
        "short_title": "SQL",
        "group": "databases",
        "tagline": "From Textbook Theory to Production Query Engines",
        "description": "Comprehensive guides to relational database internals, non-equi joins, execution planners, indexing, and high-frequency viva/interview traps.",
        "icon_type": "devicon",
        "icon": "devicon-azuresqldatabase-plain colored",
        "badge": "Core Track",
        "topics": [
            # 1. SQL Basics
            {"title": "What is a Database & RDBMS?", "slug": "sql-what-is-database", "category": "1. SQL Basics", "vertical": "notes", "reading_time": "5 min read", "order": 1},
            {"title": "SQL Introduction & Syntax", "slug": "sql-intro-syntax", "category": "1. SQL Basics", "vertical": "notes", "reading_time": "6 min read", "order": 2},

            # 2. Database & Table Management (DDL)
            {"title": "SQL CREATE & DROP DATABASE", "slug": "sql-create-drop-database", "category": "2. Database & Table Management", "vertical": "notes", "reading_time": "5 min read", "order": 3},
            {"title": "SQL CREATE & DROP TABLE", "slug": "sql-create-drop-table", "category": "2. Database & Table Management", "vertical": "notes", "reading_time": "6 min read", "order": 4},
            {"title": "SQL ALTER TABLE & TRUNCATE TABLE", "slug": "sql-alter-truncate-table", "category": "2. Database & Table Management", "vertical": "notes", "reading_time": "6 min read", "order": 5},

            # 3. Querying & Filtering (DQL)
            {"title": "SQL SELECT & SELECT DISTINCT", "slug": "sql-select-distinct", "category": "3. Querying & Filtering", "vertical": "notes", "reading_time": "6 min read", "order": 6},
            {"title": "SQL WHERE Clause & Comparison Operators", "slug": "sql-where-clause", "category": "3. Querying & Filtering", "vertical": "notes", "reading_time": "6 min read", "order": 7},
            {"title": "SQL AND, OR & NOT Operators", "slug": "sql-and-or-not", "category": "3. Querying & Filtering", "vertical": "notes", "reading_time": "5 min read", "order": 8},
            {"title": "SQL ORDER BY (Sorting Data)", "slug": "sql-order-by", "category": "3. Querying & Filtering", "vertical": "notes", "reading_time": "5 min read", "order": 9},

            # 4. Data Manipulation (DML)
            {"title": "SQL INSERT INTO (Adding Rows)", "slug": "sql-insert-into", "category": "4. Data Manipulation", "vertical": "notes", "reading_time": "6 min read", "order": 10},
            {"title": "SQL NULL Values (IS NULL & IS NOT NULL)", "slug": "sql-null-values", "category": "4. Data Manipulation", "vertical": "notes", "reading_time": "6 min read", "order": 11},
            {"title": "SQL UPDATE (Modifying Records)", "slug": "sql-update", "category": "4. Data Manipulation", "vertical": "notes", "reading_time": "6 min read", "order": 12},
            {"title": "SQL DELETE (Removing Records)", "slug": "sql-delete", "category": "4. Data Manipulation", "vertical": "notes", "reading_time": "6 min read", "order": 13},
            {"title": "SQL LIMIT & TOP Records", "slug": "sql-limit-top", "category": "4. Data Manipulation", "vertical": "notes", "reading_time": "5 min read", "order": 14},

            # 5. Aggregations & Grouping
            {"title": "SQL Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)", "slug": "sql-aggregate-functions", "category": "5. Aggregations & Grouping", "vertical": "notes", "reading_time": "7 min read", "order": 15},
            {"title": "SQL GROUP BY Statement", "slug": "sql-group-by", "category": "5. Aggregations & Grouping", "vertical": "notes", "reading_time": "7 min read", "order": 16},
            {"title": "SQL HAVING Clause", "slug": "sql-having", "category": "5. Aggregations & Grouping", "vertical": "notes", "reading_time": "6 min read", "order": 17},

            # 6. Advanced Filtering & Operators
            {"title": "SQL LIKE Operator & Wildcards", "slug": "sql-like-wildcards", "category": "6. Advanced Filtering", "vertical": "notes", "reading_time": "6 min read", "order": 18},
            {"title": "SQL IN & BETWEEN Operators", "slug": "sql-in-between", "category": "6. Advanced Filtering", "vertical": "notes", "reading_time": "6 min read", "order": 19},
            {"title": "SQL Aliases (Column & Table AS)", "slug": "sql-aliases", "category": "6. Advanced Filtering", "vertical": "notes", "reading_time": "5 min read", "order": 20},

            # 7. Constraints & Keys
            {"title": "SQL Constraints (NOT NULL, UNIQUE, CHECK, DEFAULT)", "slug": "sql-constraints-overview", "category": "7. Constraints & Keys", "vertical": "notes", "reading_time": "7 min read", "order": 21},
            {"title": "SQL PRIMARY KEY & FOREIGN KEY", "slug": "sql-primary-foreign-key", "category": "7. Constraints & Keys", "vertical": "notes", "reading_time": "7 min read", "order": 22},
            {"title": "SQL AUTO_INCREMENT & Identity", "slug": "sql-auto-increment", "category": "7. Constraints & Keys", "vertical": "notes", "reading_time": "5 min read", "order": 23},

            # 8. SQL Joins
            {"title": "SQL Joins Overview & Venn Diagrams", "slug": "sql-joins-introduction", "category": "8. SQL Joins", "vertical": "notes", "reading_time": "6 min read", "order": 24},
            {"title": "SQL INNER JOIN", "slug": "sql-inner-join", "category": "8. SQL Joins", "vertical": "notes", "reading_time": "7 min read", "order": 25},
            {"title": "SQL LEFT JOIN (Outer Join)", "slug": "sql-left-join", "category": "8. SQL Joins", "vertical": "notes", "reading_time": "7 min read", "order": 26},
            {"title": "SQL RIGHT JOIN & FULL OUTER JOIN", "slug": "sql-right-full-join", "category": "8. SQL Joins", "vertical": "notes", "reading_time": "7 min read", "order": 27},
            {"title": "SQL Joins: What Textbooks Teach vs. Production Reality", "slug": "sql-joins-textbook-vs-reality", "category": "8. SQL Joins", "vertical": "notes", "reading_time": "8 min read", "order": 28},

            # 9. Advanced SQL & Analysis
            {"title": "SQL UNION & UNION ALL", "slug": "sql-union-all", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "6 min read", "order": 29},
            {"title": "SQL CASE Statement", "slug": "sql-case-expression", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "6 min read", "order": 30},
            {"title": "SQL Subqueries & Nested Queries", "slug": "sql-subqueries", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "8 min read", "order": 31},
            {"title": "SQL Views (CREATE & DROP VIEW)", "slug": "sql-views", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "6 min read", "order": 32},
            {"title": "Window Functions Masterclass: ROW_NUMBER, RANK, DENSE_RANK & LEAD/LAG", "slug": "sql-window-functions-deep-dive", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "9 min read", "order": 33},
            {"title": "Common Table Expressions (CTEs) & Recursive Hierarchical Queries", "slug": "sql-recursive-ctes-and-hierarchies", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "7 min read", "order": 34},
            {"title": "ACID Properties & Transaction Isolation Levels (Dirty Read vs Phantom Read)", "slug": "sql-acid-transactions-and-isolation-levels", "category": "9. Advanced SQL", "vertical": "notes", "reading_time": "10 min read", "order": 35},

            # 10. Query Optimization & Internals (Featured in Notes)
            {"title": "B-Tree vs Hash Indexing: Internals, Clustered Indexes & Scans", "slug": "sql-indexing-btree-hash-internals", "category": "10. Query Optimization", "vertical": "notes", "reading_time": "10 min read", "order": 36},
            {"title": "Database Normalization (1NF to BCNF) vs. Star Schema Denormalization", "slug": "sql-database-normalization-vs-star-schema", "category": "10. Query Optimization", "vertical": "notes", "reading_time": "11 min read", "order": 37},

            # 11. Interview Prep (Featured in Interview Questions)
            {"title": "Top 45 SQL Viva Practical & Junior Interview Traps", "slug": "sql-viva-top-45-interview-traps", "category": "11. Interview Prep", "vertical": "viva", "reading_time": "12 min read", "order": 38},
        ],
    },
    "mysql": {
        "slug": "mysql",
        "title": "MySQL Database Server",
        "short_title": "MySQL",
        "group": "databases",
        "tagline": "InnoDB Engine Architecture, Replication & Buffer Pool",
        "description": "Master InnoDB storage internals, redo/undo logs, binlog replication, slow query logs, and index optimization.",
        "icon_type": "devicon",
        "icon": "devicon-mysql-plain colored",
        "badge": "Enterprise RDBMS",
        "topics": [
            {"title": "InnoDB vs MyISAM: Crash Safety, Row-Level Locks & MVCC", "slug": "mysql-innodb-vs-myisam-architecture", "category": "Storage Engines", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "MySQL EXPLAIN & EXPLAIN ANALYZE: Reading JSON Query Plans", "slug": "mysql-explain-query-plan-optimization", "category": "Query Optimization", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Buffer Pool Tuning, Dirty Pages & Redo Log Checkpoints", "slug": "mysql-buffer-pool-and-redo-logs", "category": "Server Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "MySQL Master-Replica Replication & GTID Failover", "slug": "mysql-replication-gtid-high-availability", "category": "High Availability", "vertical": "notes", "reading_time": "11 min read"},
            {"title": "Top 30 MySQL Viva Questions & Common Connection Pitfalls", "slug": "mysql-viva-top-30-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "10 min read"},
        ],
    },
    "postgresql": {
        "slug": "postgresql",
        "title": "PostgreSQL Advanced RDBMS",
        "short_title": "PostgreSQL",
        "group": "databases",
        "tagline": "MVCC, VACUUM Internals, GIN/GiST Indexes & JSONB",
        "description": "Production Postgres internals: Multi-Version Concurrency Control (MVCC), autovacuum tuning, foreign data wrappers, and JSONB indexing.",
        "icon_type": "devicon",
        "icon": "devicon-postgresql-plain colored",
        "badge": "Modern Standard",
        "topics": [
            {"title": "How PostgreSQL MVCC Works: Tuple Headers, cmin/cmax & Dead Rows", "slug": "postgres-mvcc-and-tuple-visibility", "category": "Engine Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "VACUUM, Autovacuum & Transaction ID (XID) Wraparound Safety", "slug": "postgres-vacuum-and-wraparound-prevention", "category": "Engine Internals", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "GIN & GiST Indexes for High-Speed JSONB & Full-Text Search", "slug": "postgres-gin-gist-jsonb-indexing", "category": "Advanced Indexing", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Partitioning Strategies: Declarative Range, List & Hash Partitioning", "slug": "postgres-table-partitioning-deep-dive", "category": "Database Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Top 35 PostgreSQL Interview & Viva Trap Questions", "slug": "postgres-viva-top-35-traps", "category": "Interview Prep", "vertical": "viva", "reading_time": "11 min read"},
        ],
    },
    "sqlite": {
        "slug": "sqlite",
        "title": "SQLite Embedded Database",
        "short_title": "SQLite",
        "group": "databases",
        "tagline": "Single-File Architecture, WAL Mode & Embedded Storage",
        "description": "Explore SQLite's zero-configuration B-Tree engine, Write-Ahead Logging (WAL) concurrency, and dynamic type affinity.",
        "icon_type": "devicon",
        "icon": "devicon-sqlite-plain colored",
        "badge": "Embedded Storage",
        "topics": [
            {"title": "SQLite Single-File VFS Architecture & Dynamic Typing Rules", "slug": "sqlite-architecture-and-type-affinity", "category": "Core Architecture", "vertical": "notes", "reading_time": "7 min read"},
            {"title": "WAL Mode vs Rollback Journal: High-Concurrency Reads & Writes", "slug": "sqlite-wal-mode-concurrency", "category": "Performance Tuning", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Top 20 SQLite Oral Exam Viva Questions", "slug": "sqlite-viva-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "8 min read"},
        ],
    },
    "mongodb": {
        "slug": "mongodb",
        "title": "MongoDB Document Database",
        "short_title": "MongoDB",
        "group": "databases",
        "tagline": "BSON Documents, Aggregation Pipelines & Sharding",
        "description": "NoSQL document store fundamentals: flexible schemas, WiredTiger storage engine, replica sets, and multi-stage aggregation pipelines.",
        "icon_type": "devicon",
        "icon": "devicon-mongodb-plain colored",
        "badge": "NoSQL Core",
        "topics": [
            {"title": "Document Data Modeling: Embedding vs Referencing Trade-offs", "slug": "mongodb-schema-design-embed-vs-reference", "category": "Data Modeling", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Aggregation Framework Pipeline: $match, $group, $project, $lookup", "slug": "mongodb-aggregation-pipeline-masterclass", "category": "Query Engine", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "WiredTiger Storage Engine: Cache Eviction & Compression", "slug": "mongodb-wiredtiger-storage-internals", "category": "Engine Internals", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Replica Sets, Election Protocols & Write Concerns (w: majority)", "slug": "mongodb-replica-sets-and-write-concern", "category": "High Availability", "vertical": "notes", "reading_time": "9 min read"},
        ],
    },
    "redis": {
        "slug": "redis",
        "title": "Redis In-Memory Key-Value",
        "short_title": "Redis",
        "group": "databases",
        "tagline": "Single-Threaded Event Loop, Data Structures & Caching",
        "description": "High-throughput in-memory architecture: Strings, Hashes, Sorted Sets, Pub/Sub, RDB/AOF persistence, and distributed lock patterns.",
        "icon_type": "devicon",
        "icon": "devicon-redis-plain colored",
        "badge": "In-Memory Store",
        "topics": [
            {"title": "Redis Data Structures: Hashes, Bitmaps, HyperLogLog & Sorted Sets", "slug": "redis-data-structures-and-time-complexity", "category": "Core Data Structures", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Persistence Mechanics: RDB Snapshots vs AOF Append-Only Logs", "slug": "redis-rdb-vs-aof-persistence", "category": "Persistence", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Distributed Locks & Redlock Algorithm Pitfalls", "slug": "redis-distributed-locks-and-redlock", "category": "System Design", "vertical": "notes", "reading_time": "9 min read"},
        ],
    },
    "snowflake": {
        "slug": "snowflake",
        "title": "Snowflake Cloud Data Warehouse",
        "short_title": "Snowflake",
        "group": "databases",
        "tagline": "Decoupled Storage & Compute, Virtual Warehouses & Micro-Partitions",
        "description": "Modern cloud analytics data warehousing: columnar micro-partitions, Zero-Copy Cloning, Time Travel, and auto-scaling compute clusters.",
        "icon_type": "devicon",
        "icon": "devicon-snowflake-plain colored",
        "badge": "Cloud Warehouse",
        "topics": [
            {"title": "Snowflake 3-Tier Architecture: Cloud Services, Virtual Warehouses & S3 Storage", "slug": "snowflake-three-tier-architecture", "category": "Cloud Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Micro-Partitions & Automatic Clustering: Zero Indexing Architecture", "slug": "snowflake-micro-partitions-and-clustering", "category": "Query Engine", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Time Travel, Fail-Safe & Zero-Copy Cloning Mechanics", "slug": "snowflake-time-travel-and-zero-copy-cloning", "category": "Data Management", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },

    # ─── 2. PROGRAMMING LANGUAGES ─────────────────────────────────────────────
    "python": {
        "slug": "python",
        "title": "Python & Data Engineering",
        "short_title": "Python",
        "group": "languages",
        "tagline": "Modern Python Internals, OOP & ETL Pipelines",
        "description": "In-depth explorations of Python syntax, data types, control flow, data structures, OOP, CPython memory architecture, mutable traps, and production pipelines.",
        "icon_type": "devicon",
        "icon": "devicon-python-plain colored",
        "badge": "Core Track",
        "topics": [
            # 1. Python Basics
            {"title": "Python Syntax & Comments", "slug": "python-syntax-comments", "category": "Python Basics", "vertical": "notes", "reading_time": "5 min read"},
            {"title": "Python Variables & Dynamic Typing", "slug": "python-variables-datatypes", "category": "Python Basics", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python Numbers & Type Casting", "slug": "python-numbers-casting", "category": "Python Basics", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python Booleans & Logical Operators", "slug": "python-booleans-operators", "category": "Python Basics", "vertical": "notes", "reading_time": "5 min read"},
            {"title": "Python Strings, Slicing & F-Strings", "slug": "python-strings-formatting", "category": "Python Basics", "vertical": "notes", "reading_time": "7 min read"},

            # 2. Control Flow
            {"title": "Python If...Else & Conditional Logic", "slug": "python-if-else-conditionals", "category": "Control Flow", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python While Loops, Break & Continue", "slug": "python-while-loops", "category": "Control Flow", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python For Loops & Range Function", "slug": "python-for-loops-range", "category": "Control Flow", "vertical": "notes", "reading_time": "7 min read"},

            # 3. Data Structures
            {"title": "Python Lists & List Comprehensions", "slug": "python-lists-comprehensions", "category": "Data Structures", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Python Tuples & Tuple Unpacking", "slug": "python-tuples-unpacking", "category": "Data Structures", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python Sets & Set Theory Operations", "slug": "python-sets-operations", "category": "Data Structures", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python Dictionaries & Hash Map Mechanics", "slug": "python-dictionaries-methods", "category": "Data Structures", "vertical": "notes", "reading_time": "8 min read"},

            # 4. Functions & Modules
            {"title": "Python Functions, Scope & *args / **kwargs", "slug": "python-functions-args-kwargs", "category": "Functions & Modules", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Python Lambda Functions & Map/Filter", "slug": "python-lambda-map-filter", "category": "Functions & Modules", "vertical": "notes", "reading_time": "6 min read"},
            {"title": "Python Modules, Packages & Virtual Environments", "slug": "python-modules-packages", "category": "Functions & Modules", "vertical": "notes", "reading_time": "7 min read"},

            # 5. Object-Oriented Programming
            {"title": "Classes, Objects & __init__ Constructor", "slug": "python-classes-objects-init", "category": "Object-Oriented Design", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Inheritance, Polymorphism & super() Method", "slug": "python-inheritance-polymorphism", "category": "Object-Oriented Design", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Dunder Methods & Python Data Model: Building Pythonic Classes", "slug": "python-dunder-methods-and-data-model", "category": "Object-Oriented Design", "vertical": "notes", "reading_time": "9 min read"},

            # 6. Internals & Production Gotchas
            {"title": "CPython Memory Architecture: Heap, Stack, Reference Counting & Cyclic GC", "slug": "python-memory-model-and-gc", "category": "Core Architecture", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "The Mutable Default Argument Trap & Object Identity in Python", "slug": "python-mutable-default-argument-trap", "category": "Core Gotchas", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Iterators, Generators & Memory-Efficient Stream Processing", "slug": "python-generators-and-stream-processing", "category": "Advanced Programming", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Decorators with Arguments, Wraps & Class Decorators", "slug": "python-decorators-deep-dive", "category": "Advanced Programming", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "GIL Internals: Multithreading vs Multiprocessing vs Asyncio", "slug": "python-gil-threading-multiprocessing-asyncio", "category": "Concurrency & Parallelism", "vertical": "notes", "reading_time": "11 min read"},
            {"title": "File I/O, Context Managers & With Statement Internals", "slug": "python-file-io-context-managers", "category": "System & File I/O", "vertical": "notes", "reading_time": "8 min read"},

            # 7. Viva & Interview Prep
            {"title": "Top 40 Python Viva & Technical Interview Traps", "slug": "python-viva-top-40-traps", "category": "Interview Prep", "vertical": "viva", "reading_time": "12 min read"},
            {"title": "Python Closures, Dynamic Binding & Scope Trap Questions", "slug": "python-trick-questions-closures", "category": "Interview Prep", "vertical": "viva", "reading_time": "10 min read"},
        ],
    },
    "javascript": {
        "slug": "javascript",
        "title": "JavaScript Core & Modern ES6+",
        "short_title": "JavaScript",
        "group": "languages",
        "tagline": "V8 Engine, Event Loop, Microtasks & Prototype Chains",
        "description": "Deep-dive into the V8 JavaScript engine, event loop execution phases, closures, prototypal inheritance, and async/await gotchas.",
        "icon_type": "devicon",
        "icon": "devicon-javascript-plain colored",
        "badge": "Web Standard",
        "topics": [
            {"title": "The Event Loop, Microtasks (Promises) vs Macrotasks (setTimeout)", "slug": "js-event-loop-microtasks-macrotasks", "category": "Runtime Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Closures, Lexical Scope & Garbage Collection Traps in JS", "slug": "js-closures-lexical-scope-internals", "category": "Language Core", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Prototypal Inheritance vs ES6 Classes: Prototype Chain Lookup", "slug": "js-prototypes-and-prototype-chain", "category": "Object Model", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "The 'this' Keyword Rules: Default, Implicit, Explicit & Arrow Functions", "slug": "js-this-keyword-binding-rules", "category": "Language Core", "vertical": "notes", "reading_time": "7 min read"},
            {"title": "Top 35 JavaScript Interview & Viva Coding Traps", "slug": "js-viva-top-35-coding-traps", "category": "Interview Prep", "vertical": "viva", "reading_time": "11 min read"},
        ],
    },
    "typescript": {
        "slug": "typescript",
        "title": "TypeScript Type System",
        "short_title": "TypeScript",
        "group": "languages",
        "tagline": "Static Typing, Generics, Discriminated Unions & Utility Types",
        "description": "Master TypeScript's structural type system: conditional types, mapped types, type narrowing, inference, and type-level programming.",
        "icon_type": "devicon",
        "icon": "devicon-typescript-plain colored",
        "badge": "Enterprise JS",
        "topics": [
            {"title": "Structural Typing vs Nominal Typing & Type Narrowing", "slug": "ts-structural-typing-and-narrowing", "category": "Type System Core", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Generics & Generic Constraints (extends keyof) in Production", "slug": "ts-generics-and-constraints", "category": "Advanced Types", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Conditional Types, Infer Keyword & Mapped Utility Types", "slug": "ts-conditional-types-and-infer", "category": "Type-Level Programming", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Discriminated Unions & Exhaustive Type Checking with Never", "slug": "ts-discriminated-unions-and-never", "category": "Pattern Design", "vertical": "notes", "reading_time": "7 min read"},
        ],
    },
    "java": {
        "slug": "java",
        "title": "Java & JVM Architecture",
        "short_title": "Java",
        "group": "languages",
        "tagline": "JVM Bytecode, Memory Model (Heap/Metaspace) & Garbage Collectors",
        "description": "Comprehensive guide to Java enterprise development, JVM memory allocation, G1/ZGC collectors, multithreading, and Spring Boot patterns.",
        "icon_type": "devicon",
        "icon": "devicon-java-plain colored",
        "badge": "Enterprise Core",
        "topics": [
            {"title": "JVM Architecture: ClassLoader, Execution Engine & Bytecode JIT", "slug": "java-jvm-architecture-and-jit", "category": "JVM Internals", "vertical": "notes", "reading_time": "11 min read"},
            {"title": "Java Memory Model: Young Gen, Old Gen, Metaspace & G1 GC", "slug": "java-memory-model-and-g1gc", "category": "JVM Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Java Collections Framework: HashMap Bucket Collision & Rehashing", "slug": "java-hashmap-internals-and-collisions", "category": "Collections Core", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Multithreading & Synchronization: Volatile, Synchronized & Locks", "slug": "java-multithreading-volatile-locks", "category": "Concurrency", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Top 45 Java Viva Questions for College Labs & Placements", "slug": "java-viva-top-45-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "12 min read"},
        ],
    },
    "cpp": {
        "slug": "cpp",
        "title": "C++ & Modern Systems Programming",
        "short_title": "C++",
        "group": "languages",
        "tagline": "Manual Memory, RAII, Smart Pointers, Move Semantics & STL",
        "description": "High-performance systems programming: pointers, virtual function tables (vtable), templates, copy elision, and modern C++20 features.",
        "icon_type": "devicon",
        "icon": "devicon-cplusplus-plain colored",
        "badge": "Systems & HFT",
        "topics": [
            {"title": "Pointers, References & Dynamic Memory Allocation (new/delete)", "slug": "cpp-pointers-and-memory-allocation", "category": "Core Memory", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "RAII & Smart Pointers: unique_ptr, shared_ptr & weak_ptr Cycles", "slug": "cpp-raii-and-smart-pointers", "category": "Modern C++", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Virtual Functions, VTables & Dynamic Polymorphism Overhead", "slug": "cpp-vtable-and-virtual-functions", "category": "Object Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Lvalues, Rvalues, std::move & Perfect Forwarding", "slug": "cpp-move-semantics-and-forwarding", "category": "Modern C++", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Top 40 C++ College Viva & Technical Screening Questions", "slug": "cpp-viva-top-40-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "11 min read"},
        ],
    },
    "c": {
        "slug": "c",
        "title": "C Systems Programming",
        "short_title": "C",
        "group": "languages",
        "tagline": "Memory Pointers, Struct Padding, Stack vs Heap & Bitwise",
        "description": "Foundation of all modern computing: manual memory management, pointer arithmetic, struct alignment, preprocessors, and POSIX system calls.",
        "icon_type": "devicon",
        "icon": "devicon-c-plain colored",
        "badge": "Foundational",
        "topics": [
            {"title": "Pointer Arithmetic, Void Pointers & Function Pointers", "slug": "c-pointer-arithmetic-and-function-pointers", "category": "Core Memory", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Struct Padding, Memory Alignment & Byte Packing in C", "slug": "c-struct-padding-and-memory-alignment", "category": "Memory Architecture", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Stack vs Heap, malloc/calloc/realloc & Segmentation Fault Traps", "slug": "c-dynamic-memory-segfaults-valgrind", "category": "Memory Management", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Top 35 C Lab Viva Questions & University Exam Traps", "slug": "c-viva-top-35-university-traps", "category": "Interview Prep", "vertical": "viva", "reading_time": "10 min read"},
        ],
    },
    "go": {
        "slug": "go",
        "title": "Go (Golang) Cloud Systems",
        "short_title": "Go",
        "group": "languages",
        "tagline": "Goroutines, Channels, CSP Concurrency & Memory Escapes",
        "description": "Cloud-native backend language: Communicating Sequential Processes (CSP), channels, interfaces, escape analysis, and microservice patterns.",
        "icon_type": "devicon",
        "icon": "devicon-go-original-wordmark colored",
        "badge": "Cloud Backend",
        "topics": [
            {"title": "Goroutines, Channels & CSP Concurrency Patterns", "slug": "go-goroutines-channels-concurrency", "category": "Concurrency", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Go Scheduler (GMP Model): How Go M:N Scheduling Works", "slug": "go-gmp-scheduler-internals", "category": "Runtime Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Escape Analysis: Stack vs Heap Allocation in the Go Compiler", "slug": "go-escape-analysis-stack-heap", "category": "Compiler Internals", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "rust": {
        "slug": "rust",
        "title": "Rust Systems Programming",
        "short_title": "Rust",
        "group": "languages",
        "tagline": "Ownership, Borrow Checker, Lifetimes & Fearless Concurrency",
        "description": "Zero-cost abstractions with complete memory safety: affine type system, borrow checker, lifetime annotations, and unsafe Rust boundaries.",
        "icon_type": "devicon",
        "icon": "devicon-rust-plain colored",
        "badge": "Memory Safe",
        "topics": [
            {"title": "The Ownership Model: Move Semantics & Copy Trait", "slug": "rust-ownership-and-move-semantics", "category": "Memory Safety", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "The Borrow Checker: Mutable vs Immutable Reference Rules", "slug": "rust-borrow-checker-rules", "category": "Memory Safety", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Lifetime Annotations ('a) & How the Compiler Resolves Them", "slug": "rust-lifetime-annotations-explained", "category": "Type System", "vertical": "notes", "reading_time": "10 min read"},
        ],
    },
    "csharp": {
        "slug": "csharp",
        "title": "C# & .NET Enterprise Core",
        "short_title": "C#",
        "group": "languages",
        "tagline": "CLR Execution, Async/Await, LINQ Internals & ASP.NET Core",
        "description": "Modern cross-platform .NET development: Common Language Runtime (CLR), task-based asynchronous patterns, Span<T> zero-copy memory, and LINQ execution.",
        "icon_type": "devicon",
        "icon": "devicon-csharp-plain colored",
        "badge": "Enterprise .NET",
        "topics": [
            {"title": "CLR Architecture, IL Bytecode Compilation & JIT Modes", "slug": "csharp-clr-architecture-and-jit", "category": "Runtime Internals", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "LINQ Internals: Deferred Execution vs Immediate Execution", "slug": "csharp-linq-deferred-execution-internals", "category": "Core Language", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Async/Await State Machine & Synchronization Contexts", "slug": "csharp-async-await-state-machine", "category": "Concurrency", "vertical": "notes", "reading_time": "10 min read"},
        ],
    },
    "php": {
        "slug": "php",
        "title": "PHP 8 & Modern Web Engines",
        "short_title": "PHP",
        "group": "languages",
        "tagline": "Zend Engine, OPcache, JIT & Modern Framework Architectures",
        "description": "Modern PHP 8+ web applications: OPcache preloading, typed properties, fibers for asynchronous execution, and MVC framework fundamentals.",
        "icon_type": "devicon",
        "icon": "devicon-php-plain colored",
        "badge": "Web Platforms",
        "topics": [
            {"title": "Zend Engine Architecture, OPcache & The PHP 8 JIT Compiler", "slug": "php-zend-engine-opcache-jit", "category": "Engine Internals", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Modern PHP 8 Features: Attributes, Match Expressions & Fibers", "slug": "php-8-features-and-modern-patterns", "category": "Modern Language", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Top 25 PHP Lab Viva & University Exam Questions", "slug": "php-viva-top-25-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "9 min read"},
        ],
    },
    "html-css": {
        "slug": "html-css",
        "title": "HTML5 & Modern CSS3",
        "short_title": "HTML/CSS",
        "group": "languages",
        "tagline": "Semantic DOM, CSS Grid, Flexbox, Box Model & Rendering Pipeline",
        "description": "Web interface foundations: Critical Rendering Path, reflow vs repaint, CSS Grid vs Flexbox architectures, and responsive media queries.",
        "icon_type": "devicon",
        "icon": "devicon-html5-plain colored",
        "badge": "UI Foundation",
        "topics": [
            {"title": "Critical Rendering Path: DOM, CSSOM, Render Tree, Reflow & Repaint", "slug": "html-css-critical-rendering-path", "category": "Browser Internals", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "CSS Box Model: Content-Box vs Border-Box & Margin Collapse", "slug": "css-box-model-and-margin-collapsing", "category": "Layout Engine", "vertical": "notes", "reading_time": "7 min read"},
            {"title": "CSS Grid vs Flexbox: 1D vs 2D Layout Architectures", "slug": "css-grid-vs-flexbox-guide", "category": "Layout Engine", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },

    # ─── 3. DATA SCIENCE & BI TOOLS ───────────────────────────────────────────
    "pandas": {
        "slug": "pandas",
        "title": "Pandas Data Wrangling",
        "short_title": "Pandas",
        "group": "data_bi",
        "tagline": "DataFrame Memory Models, Vectorization, GroupBy & Merges",
        "description": "Production Python data processing: BlockManager internals, chained indexing gotchas (.loc vs .iloc), vectorized string operations, and multi-index aggregation.",
        "icon_type": "devicon",
        "icon": "devicon-pandas-plain colored",
        "badge": "Data Science",
        "topics": [
            {"title": "Pandas Memory Optimization: Categoricals, Downcasting & Chunking", "slug": "pandas-memory-optimization-chunking", "category": "Performance", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "SettingWithCopyWarning Explained: Views vs Copies in DataFrames", "slug": "pandas-settingwithcopywarning-views-copies", "category": "Gotchas", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Advanced GroupBy, Custom Aggregations & Pivot Table Internals", "slug": "pandas-groupby-aggregations-deep-dive", "category": "Data Wrangling", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Top 25 Pandas Technical Interview Challenges", "slug": "pandas-viva-top-25-challenges", "category": "Interview Prep", "vertical": "viva", "reading_time": "10 min read"},
        ],
    },
    "numpy": {
        "slug": "numpy",
        "title": "NumPy Numerical Computing",
        "short_title": "NumPy",
        "group": "data_bi",
        "tagline": "Ndarrays, Strides, Broadcasting Rules & C-Contiguity",
        "description": "Fast numerical matrix operations in C: strided memory layouts, broadcasting dimensions, memory views, and BLAS/LAPACK linear algebra.",
        "icon_type": "devicon",
        "icon": "devicon-numpy-plain colored",
        "badge": "Scientific Computing",
        "topics": [
            {"title": "Ndarray Architecture: Strides, Offsets & C vs Fortran Contiguity", "slug": "numpy-ndarray-strides-and-memory", "category": "Core Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Broadcasting Rules & Multi-Dimensional Array Arithmetic", "slug": "numpy-broadcasting-rules-explained", "category": "Vectorization", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "bi": {
        "slug": "bi",
        "title": "Business Intelligence & Analytics",
        "short_title": "Power BI & Tableau",
        "group": "data_bi",
        "tagline": "Star Schemas, Advanced DAX & Executive Storytelling",
        "description": "Fact/dimension modeling, complex DAX measures, Tableau LOD calculations, and real-world interactive BI dashboards.",
        "icon_type": "devicon",
        "icon": "devicon-unifiedmodelinglanguage-plain colored",
        "badge": "Core Track",
        "topics": [
            {"title": "Star Schema vs Snowflake Schema: Designing Production Data Marts", "slug": "bi-star-schema-vs-snowflake-schema", "category": "Data Modeling", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "DAX Filter Context vs Row Context: The CALCULATE Function Demystified", "slug": "powerbi-dax-filter-context-calculate", "category": "Power BI & DAX", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Tableau LOD Expressions: FIXED, INCLUDE, EXCLUDE Calculations", "slug": "tableau-lod-fixed-include-exclude", "category": "Tableau Analytics", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Time Intelligence in DAX: YTD, QTD, SAMEPERIODLASTYEAR & Calendars", "slug": "powerbi-dax-time-intelligence", "category": "Power BI & DAX", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Top 35 BI Analyst Viva & Dashboard Defense Questions", "slug": "bi-viva-top-35-interview-questions", "category": "Interview Prep", "vertical": "viva", "reading_time": "11 min read"},
        ],
    },
    "powerbi": {
        "slug": "powerbi",
        "title": "Microsoft Power BI",
        "short_title": "Power BI",
        "group": "data_bi",
        "tagline": "VertiPaq Engine, Tabular Models, DAX Measures & Power Query M",
        "description": "Executive reporting platform: VertiPaq columnar compression, relationship cardinality (1:*, *:*), context transition, and automated gateway refresh.",
        "icon_type": "svg",
        "icon": "powerbi",
        "badge": "Enterprise BI",
        "topics": [
            {"title": "VertiPaq In-Memory Columnar Engine & Dictionary Compression", "slug": "powerbi-vertipaq-engine-compression", "category": "Engine Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Context Transition in DAX: How Row Context Becomes Filter Context", "slug": "powerbi-context-transition-explained", "category": "DAX Mastery", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Bidirectional Cross-Filtering Pitfalls in Star Schemas", "slug": "powerbi-bidirectional-relationships-risks", "category": "Data Modeling", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "tableau": {
        "slug": "tableau",
        "title": "Tableau Visual Analytics",
        "short_title": "Tableau",
        "group": "data_bi",
        "tagline": "Level of Detail (LOD), Hyper Data Extracts & Story Dashboards",
        "description": "Visual data exploration: Hyper in-memory engine, table calculation partitions, parameter actions, multi-axis dual charts, and dashboard stories.",
        "icon_type": "svg",
        "icon": "tableau",
        "badge": "Visual Analytics",
        "topics": [
            {"title": "Tableau Order of Operations: The Visual Pipeline Explained", "slug": "tableau-order-of-operations-pipeline", "category": "Core Architecture", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Table Calculations vs LOD Calculations: When to Use Which", "slug": "tableau-table-calcs-vs-lod-expressions", "category": "Calculations", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "excel": {
        "slug": "excel",
        "title": "Advanced Excel & Power Query",
        "short_title": "Excel",
        "group": "data_bi",
        "tagline": "Power Query M Language, Dynamic Arrays, XLOOKUP & Financial Models",
        "description": "Enterprise spreadsheet engineering: automated Power Query ETL pipelines, dynamic arrays (FILTER, UNIQUE, SORT), What-If scenarios, and financial modeling.",
        "icon_type": "svg",
        "icon": "excel",
        "badge": "Business Foundation",
        "topics": [
            {"title": "Power Query ETL Automation: M Code Custom Transforms & Folders", "slug": "excel-power-query-m-automation", "category": "ETL Pipelines", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Modern Formula Architecture: Dynamic Arrays, LET, LAMBDA & XLOOKUP", "slug": "excel-dynamic-arrays-let-lambda", "category": "Advanced Formulas", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Financial Three-Statement Modeling & What-If Scenario Analysis", "slug": "excel-financial-modeling-scenarios", "category": "Business Modeling", "vertical": "notes", "reading_time": "10 min read"},
        ],
    },

    # ─── 4. WEB FRAMEWORKS & RUNTIMES ─────────────────────────────────────────
    "fastapi": {
        "slug": "fastapi",
        "title": "FastAPI Async Web Framework",
        "short_title": "FastAPI",
        "group": "frameworks",
        "tagline": "Starlette, Pydantic V2, ASGI Event Loops & Dependency Injection",
        "description": "High-performance asynchronous Python API framework: automatic OpenAPI docs generation, Pydantic data validation, and async database sessions.",
        "icon_type": "devicon",
        "icon": "devicon-fastapi-plain colored",
        "badge": "Modern Backend",
        "topics": [
            {"title": "ASGI Architecture vs WSGI: Why FastAPI Outperforms Django/Flask", "slug": "fastapi-asgi-vs-wsgi-architecture", "category": "Architecture", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "FastAPI Dependency Injection (Depends) in Production Microservices", "slug": "fastapi-dependency-injection-masterclass", "category": "Design Patterns", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Async SQLAlchemy 2.0 with PostgreSQL & Connection Pooling", "slug": "fastapi-async-sqlalchemy-postgres-pooling", "category": "Database Layer", "vertical": "notes", "reading_time": "10 min read"},
        ],
    },
    "django": {
        "slug": "django",
        "title": "Django & Django REST Framework",
        "short_title": "Django",
        "group": "frameworks",
        "tagline": "ORM QuerySets, Middleware Stack, Signals & Production DRF",
        "description": "Batteries-included enterprise web framework: Django ORM select_related/prefetch_related optimization, authentication, and REST APIs.",
        "icon_type": "devicon",
        "icon": "devicon-django-plain colored",
        "badge": "Full-Stack Python",
        "topics": [
            {"title": "Django ORM Optimization: Solving the N+1 Query Problem", "slug": "django-orm-n-plus-1-optimization", "category": "ORM Mastery", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "The Django Request-Response Lifecycle: Middleware Pipeline Order", "slug": "django-request-response-lifecycle", "category": "Architecture", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "react": {
        "slug": "react",
        "title": "React & Modern Component Systems",
        "short_title": "React",
        "group": "frameworks",
        "tagline": "Virtual DOM, Fiber Reconciliation, Hooks & State Managers",
        "description": "Component-driven frontend engineering: React Fiber architecture, useEffect lifecycle nuances, custom hooks, and state management.",
        "icon_type": "devicon",
        "icon": "devicon-react-original colored",
        "badge": "Frontend Standard",
        "topics": [
            {"title": "React Fiber Reconciliation & The Virtual DOM Diffing Algorithm", "slug": "react-fiber-reconciliation-vdom", "category": "Engine Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "useEffect Pitfalls: Stale Closures, Dependencies & Cleanup", "slug": "react-useeffect-stale-closures-traps", "category": "Hooks Core", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
    "nodejs": {
        "slug": "nodejs",
        "title": "Node.js & Server-Side JavaScript",
        "short_title": "Node.js",
        "group": "frameworks",
        "tagline": "Libuv Event Loop, Worker Threads, Streams & Buffers",
        "description": "Asynchronous event-driven JavaScript runtime: libuv thread pool, backpressure in streams, child processes, and clustering.",
        "icon_type": "devicon",
        "icon": "devicon-nodejs-plain colored",
        "badge": "JavaScript Backend",
        "topics": [
            {"title": "Libuv Event Loop: Timers, Poll, Check & Thread Pool Internals", "slug": "nodejs-libuv-event-loop-internals", "category": "Runtime Architecture", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Streams & Buffers: Handling Large Files with Backpressure", "slug": "nodejs-streams-buffers-backpressure", "category": "Data Streaming", "vertical": "notes", "reading_time": "9 min read"},
        ],
    },

    # ─── 5. DEVOPS, CLOUD & SYSTEMS ───────────────────────────────────────────
    "git": {
        "slug": "git",
        "title": "Git Version Control Internals",
        "short_title": "Git",
        "group": "devops",
        "tagline": "Content-Addressable Storage, DAG Commits, Rebase & Merge",
        "description": "Understand the true internal plumbing of Git: blob, tree, commit and tag objects, detached HEAD, rebasing vs merging, and reflog recovery.",
        "icon_type": "devicon",
        "icon": "devicon-git-plain colored",
        "badge": "Developer Core",
        "topics": [
            {"title": "Git Object Database: Blobs, Trees, Commits & SHA-1 Hashes", "slug": "git-object-database-internals", "category": "Git Plumbing", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Git Rebase vs Merge: Rewriting History vs Preserving True Context", "slug": "git-rebase-vs-merge-clean-history", "category": "Team Workflows", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Reflog & Reset: Recovering Lost Commits & Dropped Branches", "slug": "git-reflog-and-commit-recovery", "category": "Disaster Recovery", "vertical": "notes", "reading_time": "7 min read"},
        ],
    },
    "docker": {
        "slug": "docker",
        "title": "Docker Containers & Images",
        "short_title": "Docker",
        "group": "devops",
        "tagline": "Linux Namespaces, Cgroups, Union File Systems & Multi-Stage Builds",
        "description": "Container virtualization from scratch: process isolation via Linux namespaces, resource limiting via cgroups, overlay2 storage, and multi-stage Dockerfiles.",
        "icon_type": "devicon",
        "icon": "devicon-docker-plain colored",
        "badge": "DevOps Standard",
        "topics": [
            {"title": "How Containers Actually Work: Namespaces, Cgroups & Chroot", "slug": "docker-namespaces-cgroups-virtualization", "category": "Container Internals", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Multi-Stage Dockerfiles: Slashing Container Image Sizes by 80%", "slug": "docker-multi-stage-build-optimization", "category": "Production Images", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Docker Networking: Bridge, Host, Overlay & Port Mapping", "slug": "docker-networking-bridge-overlay", "category": "Networking", "vertical": "notes", "reading_time": "9 min read"},
        ],
    },
    "kubernetes": {
        "slug": "kubernetes",
        "title": "Kubernetes (K8s) Orchestration",
        "short_title": "Kubernetes",
        "group": "devops",
        "tagline": "Control Plane, etcd, Pods, Deployments & Service Meshes",
        "description": "Container orchestration at scale: kube-apiserver, kube-scheduler, kubelet, ingress controllers, rolling deployments, and self-healing systems.",
        "icon_type": "devicon",
        "icon": "devicon-kubernetes-plain colored",
        "badge": "Cloud Orchestration",
        "topics": [
            {"title": "K8s Control Plane Architecture: API Server, etcd, Scheduler & Controller", "slug": "k8s-control-plane-architecture", "category": "Cluster Architecture", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Pods, ReplicaSets & Zero-Downtime Rolling Deployments", "slug": "k8s-pods-and-rolling-deployments", "category": "Workloads", "vertical": "notes", "reading_time": "9 min read"},
        ],
    },
    "linux": {
        "slug": "linux",
        "title": "Linux & Bash Systems",
        "short_title": "Linux",
        "group": "devops",
        "tagline": "File Descriptors, Pipes, System Calls, Permissions & Cron",
        "description": "Operating system foundations for software engineers: stdout/stdin/stderr redirection, pipe mechanics, process signals (SIGTERM/SIGKILL), and shell automation.",
        "icon_type": "devicon",
        "icon": "devicon-linux-plain colored",
        "badge": "OS Foundation",
        "topics": [
            {"title": "Standard Streams & File Descriptors: stdin (0), stdout (1), stderr (2)", "slug": "linux-file-descriptors-and-redirection", "category": "OS Core", "vertical": "notes", "reading_time": "8 min read"},
            {"title": "Linux Process States, Signals (SIGTERM vs SIGKILL) & Zombie Processes", "slug": "linux-process-management-and-signals", "category": "Process Management", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Top 30 Linux Lab Viva & Practical Command Questions", "slug": "linux-viva-top-30-commands", "category": "Interview Prep", "vertical": "viva", "reading_time": "10 min read"},
        ],
    },
    "aws": {
        "slug": "aws",
        "title": "AWS Cloud Architecture",
        "short_title": "AWS",
        "group": "devops",
        "tagline": "VPC Subnets, EC2, S3 Storage, IAM Roles & Lambda Serverless",
        "description": "Essential Amazon Web Services: Virtual Private Clouds (VPC), security groups, IAM least-privilege policies, S3 storage tiers, and serverless compute.",
        "icon_type": "devicon",
        "icon": "devicon-amazonwebservices-plain-wordmark colored",
        "badge": "Cloud Computing",
        "topics": [
            {"title": "VPC Network Architecture: Public Subnets, Private Subnets & NAT Gateways", "slug": "aws-vpc-subnets-and-nat-gateways", "category": "Cloud Networking", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "IAM Security: Users, Groups, Roles & Least-Privilege Policies", "slug": "aws-iam-roles-and-least-privilege", "category": "Cloud Security", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },

    # ─── 6. GROWTH & MARKETING ────────────────────────────────────────────────
    "digital-marketing": {
        "slug": "digital-marketing",
        "title": "Performance Marketing & Growth",
        "short_title": "Marketing",
        "group": "marketing",
        "tagline": "Paid Ad Scaling, SEO Funnels & CRO Architecture",
        "description": "Technical SEO audits, Meta Ads ROAS optimization, Google Ads PMax bidding algorithms, and multi-channel attribution.",
        "icon_type": "devicon",
        "icon": "devicon-google-plain colored",
        "badge": "Core Track",
        "topics": [
            {"title": "Meta Ads Manager Architecture: Campaign, AdSet & Creative Scaling", "slug": "marketing-meta-ads-manager-scaling", "category": "Paid Advertising", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "Google Ads & Performance Max (PMax): Smart Bidding & Target ROAS", "slug": "marketing-google-ads-pmax-smart-bidding", "category": "Paid Advertising", "vertical": "notes", "reading_time": "9 min read"},
            {"title": "GA4 Event Tracking & GTM Server-Side Container Configuration", "slug": "marketing-ga4-event-tracking-and-gtm", "category": "Analytics & Funnels", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Technical SEO Audits: Core Web Vitals, Crawl Budget & Canonical Tags", "slug": "marketing-technical-seo-audits-and-crawl-budget", "category": "Search Engine Optimization", "vertical": "notes", "reading_time": "10 min read"},
            {"title": "Conversion Rate Optimization (CRO) & High-Converting Landing Page Design", "slug": "marketing-cro-landing-page-architecture", "category": "Conversion Science", "vertical": "notes", "reading_time": "8 min read"},
        ],
    },
}

VERTICALS: Dict[str, Dict[str, Any]] = {
    "notes": {
        "slug": "notes",
        "title": "Comprehensive Notes",
        "singular": "Note",
        "icon": "file-text",
        "badge": "Free & In-Depth",
    },
    "viva": {
        "slug": "viva",
        "title": "Practice & Viva Banks",
        "singular": "Viva Bank",
        "icon": "help-circle",
        "badge": "Exam & Viva Q&A",
    },
    "datasets": {
        "slug": "datasets",
        "title": "Practice Datasets",
        "singular": "Dataset",
        "icon": "layers",
        "badge": "Portfolio Ready",
    },
    "books": {
        "slug": "books",
        "title": "Books & Handbooks",
        "singular": "Handbook",
        "icon": "book-open",
        "badge": "Complete Guide",
    },
    "projects": {
        "slug": "projects",
        "title": "Capstone Projects",
        "singular": "Capstone",
        "icon": "rocket",
        "badge": "Production Code",
    },
}


@dataclass
class DocumentMetadata:
    title: str
    slug: str
    subject: str
    vertical: str = "notes"
    category: str = "General"
    order: int = 999
    tier: str = "free"
    price_inr: int = 0
    reading_time: str = "5 min read"
    description: str = ""
    tags: List[str] = field(default_factory=list)
    last_updated: str = ""
    file_path: Optional[str] = None
    mtime: float = 0.0

    @property
    def is_free(self) -> bool:
        return self.price_inr == 0 or self.tier == "free"

    @property
    def access_label(self) -> str:
        """Zero-upfront pricing label: price is only shown on paywall block or purchase click."""
        if self.is_free:
            return "Free Access"
        if self.tier == "student_login":
            return "Student Account"
        if self.vertical == "viva":
            return "Viva Bank"
        if self.vertical == "books":
            return "Complete Handbook"
        if self.vertical == "projects":
            return "Capstone Repo"
        return "Full Resource"

    @property
    def formatted_price(self) -> str:
        if self.price_inr == 0:
            return "Free"
        return f"₹{self.price_inr}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "slug": self.slug,
            "subject": self.subject,
            "vertical": self.vertical,
            "category": self.category,
            "order": self.order,
            "tier": self.tier,
            "price_inr": self.price_inr,
            "access_label": self.access_label,
            "formatted_price": self.formatted_price,
            "reading_time": self.reading_time,
            "description": self.description,
            "tags": self.tags,
            "last_updated": self.last_updated,
            "is_free": self.is_free,
        }


@dataclass
class ParsedDocument:
    metadata: DocumentMetadata
    html_content: str
    toc_tokens: List[Dict[str, Any]]
    toc_html: str
    raw_content: str


# In-memory document and metadata cache:
_DOCUMENT_CACHE: Dict[tuple, tuple[float, ParsedDocument]] = {}


def _preprocess_github_alerts(text: str) -> str:
    """Transforms GitHub-style alerts into standard Python-Markdown admonitions."""
    pattern = re.compile(
        r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|EXAM|PRO-TIP)\]\s*\n((?:>[^\n]*\n?)*)",
        re.IGNORECASE,
    )

    def _replace(match: re.Match) -> str:
        tag = match.group(1).lower().replace("-", "")
        if tag in ("pro-tip", "protip"):
            tag = "tip"
        elif tag in ("exam",):
            tag = "warning"
        body = match.group(2)
        indented_body = re.sub(r"^>\s?", "    ", body, flags=re.MULTILINE)
        return f'!!! {tag}\n{indented_body}\n'

    return pattern.sub(_replace, text)


def _calculate_reading_time(word_count: int, wpm: int = 200) -> str:
    minutes = max(1, math.ceil(word_count / wpm))
    return f"{minutes} min read"


def _build_markdown_parser() -> markdown.Markdown:
    """Configures Markdown parser with PyMdown extensions and TOC."""
    return markdown.Markdown(
        extensions=[
            "tables",
            "admonition",
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.tabbed",
            "pymdownx.tasklist",
            "pymdownx.betterem",
            "pymdownx.caret",
            "pymdownx.mark",
            "pymdownx.tilde",
            "toc",
        ],
        extension_configs={
            "pymdownx.highlight": {
                "use_pygments": False,
                "css_class": "code-block",
            },
            "pymdownx.superfences": {
                "css_class": "code-block-wrapper",
            },
            "toc": {
                "permalink": False,
                "baselevel": 2,
            },
        },
    )


def parse_markdown_file(file_path: Path) -> ParsedDocument:
    """Parses a single markdown file with frontmatter into ParsedDocument."""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    meta = post.metadata or {}
    slug = meta.get("slug") or file_path.stem
    subject = meta.get("subject") or file_path.parent.name
    title = meta.get("title") or slug.replace("-", " ").title()
    category = meta.get("category", "General")
    vertical = meta.get("vertical", "notes")
    order = int(meta.get("order", 999))
    tier = meta.get("tier", "free")
    price_inr = int(meta.get("price_inr", 0))
    tags = meta.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    last_updated = meta.get("last_updated", "")

    raw_body = post.content
    words = len(raw_body.split())
    reading_time = meta.get("reading_time") or _calculate_reading_time(words)
    description = meta.get("description", "")
    if not description and raw_body:
        paragraphs = [p.strip() for p in raw_body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        if paragraphs:
            description = paragraphs[0][:160] + "..."

    doc_meta = DocumentMetadata(
        title=title,
        slug=slug,
        subject=subject,
        vertical=vertical,
        category=category,
        order=order,
        tier=tier,
        price_inr=price_inr,
        reading_time=reading_time,
        description=description,
        tags=tags,
        last_updated=str(last_updated),
        file_path=str(file_path),
        mtime=file_path.stat().st_mtime,
    )

    preprocessed_body = _preprocess_github_alerts(raw_body)
    md = _build_markdown_parser()
    html_content = md.convert(preprocessed_body)
    toc_tokens = getattr(md, "toc_tokens", [])
    toc_html = getattr(md, "toc", "")

    return ParsedDocument(
        metadata=doc_meta,
        html_content=html_content,
        toc_tokens=toc_tokens,
        toc_html=toc_html,
        raw_content=raw_body,
    )


def _get_specialized_topic_content(subject: str, slug: str, title: str) -> Optional[str]:
    """
    Returns rich, practical code blueprints and explanations for foundational language topics.
    Zero code execution: strictly static copy-friendly syntax.
    """
    if subject == "python":
        if slug == "python-syntax-comments":
            return """
## 1. Academic Definition & Objectives

In Python, code structure is defined by **whitespace indentation** rather than curly braces (`{}`) or `begin...end` blocks found in C, Java, or Pascal. A block of code begins with a colon (`:`) followed by indented statements.

Key Competencies:
* PEP 8 indentation standards (strictly 4 spaces per indentation level; never mix tabs and spaces).
* Comment syntax: inline single-line comments (`#`) vs docstrings (`\"\"\"`).
* The Python execution cycle: source code (`.py`) is compiled into bytecode (`.pyc`) and interpreted by the CPython virtual machine.

> [!NOTE]
> **PEP 8 Standard**: The official Python Style Guide mandates using 4 spaces per indentation level. Avoid using the Tab character in production codebases to prevent cross-platform syntax errors.

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. PYTHON SYNTAX & INDENTATION RULES
# ==============================================================================

# Statements do not require semicolons
greeting = "Hello, Mythos Engineer"
user_role = "Data Platform Architect"

# Indentation defines scope blocks
if user_role == "Data Platform Architect":
    print(f"[ACCESS GRANTED] Role: {user_role}")
    # Nested block requires 4 additional spaces (8 spaces total)
    audit_logged = True
    if audit_logged:
        print("[AUDIT] Session recorded in security pipeline.")
else:
    print("[ACCESS DENIED]")

# ==============================================================================
# 2. COMMENT PATTERNS & DOCSTRINGS
# ==============================================================================

# Single-line comment: explain the "WHY", not the "WHAT"
CACHE_TTL_SECONDS = 300  # Enforce 5-minute cache expiry for real-time dashboards

def calculate_throughput(records_processed: int, elapsed_seconds: float) -> float:
    \"\"\"
    Compute records-per-second ingestion throughput.

    Args:
        records_processed: Total count of validated incoming records.
        elapsed_seconds: Total wall-clock time spent in extraction pipeline.

    Returns:
        Throughput rate expressed in records per second.
    \"\"\"
    if elapsed_seconds <= 0:
        return 0.0
    return records_processed / elapsed_seconds
```

---

## 3. The Production Reality ("What Textbooks Skip")

Textbooks often say comments are always good. In enterprise repositories:

* **Stale Comment Debt**: Code evolves during production incidents, but comments are frequently forgotten. A misleading comment is worse than no comment at all.
* **Self-Documenting Code**: Senior engineers write expressive variable and function names (`is_transaction_settled` instead of `flag1`) so code reads like plain English.
* **TabError in Multi-Developer Git Repositories**: When developers on Windows (using Notepad++ or legacy IDEs) push tabs into a file where Linux developers used spaces, Python raises `TabError: inconsistent use of tabs and spaces in indentation`. Always enforce automated linting (`ruff` or `flake8`) in your CI pipeline.

> [!WARNING]
> **Production Gotcha**: Never commit executable code commented out with `#`. Use Git version control for history; commented-out dead code creates clutter and confuses automated security scanners.

---

## 4. Exam & Technical Interview Gotchas

1. **Tab vs Space Mixing**: Python 3 completely disallows mixing tabs and spaces for indentation within the same source file.
2. **Docstrings are Stored at Runtime**: Unlike `#` comments which are discarded by the lexer, docstrings (`\"\"\"`) are compiled and accessible at runtime via `object.__doc__`.
3. **Line Continuation**: Long statements can be broken across lines using parentheses `(...)` or explicit backslashes `\\`. Parenthesized continuation is strongly preferred in PEP 8.

---

## 5. Mythos Mentorship Bridge

Mastering basic syntax is just step zero. In the **[MYTHOS Weekend Mentorship Cohort](/register?source=library_python_syntax)**, you will learn to structure production-grade Python packages, write automated PyTest suites, and deploy real-time ETL pipelines.
"""

        elif slug == "python-variables-datatypes":
            return """
## 1. Academic Definition & Objectives

Python uses **dynamic typing** with **strong typing**.
* **Dynamic Typing**: Variables do not have fixed types; variable names are simply pointers (references) in a namespace bound to objects living on the heap.
* **Strong Typing**: The interpreter will not implicitly coerce incompatible types (e.g., `'10' + 5` raises `TypeError`, unlike JavaScript which produces `'105'`).

Key Competencies:
* Understanding `id()`, `type()`, and `isinstance()`.
* Mutable types (lists, dictionaries, sets) vs Immutable types (integers, floats, strings, tuples, frozensets).
* The concept of object reference binding: `a = b` never copies an object; it binds another name to the existing object.

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. VARIABLE LABELS & OBJECT REFERENCES
# ==============================================================================

# In C, 'x' is a memory box holding 42.
# In Python, 42 is an int object on the heap, and 'x' is a pointer referencing it.
x = 42
y = x  # y now points to the exact same object as x

print(f"id(x): {id(x)} == id(y): {id(y)} -> {x is y}")  # True

# Rebinding 'x' creates or points to a new object
x = 100
print(f"After x = 100: x={x}, y={y}")  # x=100, y=42 (y still references 42)

# ==============================================================================
# 2. MUTABLE VS IMMUTABLE REFERENCE BEHAVIOR
# ==============================================================================

# Mutable example: Lists
list_a = [1, 2, 3]
list_b = list_a  # Both variables point to the exact same list in memory!

list_b.append(99)
print(f"list_a after modifying list_b: {list_a}")  # [1, 2, 3, 99]

# To create a true independent clone:
list_c = list_a.copy()  # Shallow copy
list_c.append(500)
print(f"list_a remains unaffected by list_c: {list_a}")  # [1, 2, 3, 99]

# ==============================================================================
# 3. CORE BUILT-IN DATA TYPES
# ==============================================================================
server_id = 101                 # int
cpu_utilization = 84.75         # float
is_active = True                # bool (subclass of int)
hostname = "worker-node-04"     # str (immutable)
ip_whitelist = ("10.0.0.1", "10.0.0.2") # tuple (immutable)
metrics = {"req_count": 1420}   # dict (mutable)
```

---

## 3. The Production Reality ("What Textbooks Skip")

In production backend microservices:

* **CPython Small Integer Caching**: CPython pre-allocates an array of integer objects for values between `-5` and `256` at startup. Any code assigning `a = 250; b = 250` will result in `a is b` being `True`. For integers outside this range (e.g. `1000`), `a is b` may be `False`. Never use `is` for value equality; always use `==`.
* **Unexpected Mutation in Data Pipelines**: Passing a dictionary or list into third-party functions can result in in-place mutations that silently corrupt global state. Prefer frozen dataclasses or defensive shallow/deep copies.

> [!WARNING]
> **Production Gotcha**: Never use `type(obj) == TargetType` for type checks. Always use `isinstance(obj, TargetType)` to properly respect subclassing and inheritance.

---

## 4. Exam & Technical Interview Gotchas

1. **Identity vs. Equality**: `==` checks value equality (invoking `__eq__`), while `is` checks memory address identity (`id(a) == id(b)`).
2. **String Immutability**: Modifying a string (e.g. `s += "text"`) creates a brand-new string object on the heap. In loops, this creates $O(N^2)$ memory churn; always use `''.join(list_of_strings)` for $O(N)$ efficiency.
3. **Walrus Operator (`:=`)**: Introduced in Python 3.8, assignment expressions allow assigning values to variables inside expressions: `if (n := len(data)) > 100: print(n)`.

---

## 5. Mythos Mentorship Bridge

Understanding pointers and memory references is what separates script kiddies from senior backend engineers. Build resilient data architectures in the **[MYTHOS Live Weekend Cohort](/register?source=library_python_datatypes)**.
"""

        elif slug == "python-numbers-casting":
            return """
## 1. Academic Definition & Objectives

Python provides three distinct numerical types:
1. **Integers (`int`)**: Arbitrary precision in Python 3 (there is no 32-bit or 64-bit integer overflow limit).
2. **Floating-Point (`float`)**: Implemented using C's `double` (64-bit IEEE 754 binary floating-point).
3. **Complex Numbers (`complex`)**: Stored as real and imaginary float components (e.g., `3 + 4j`).

Key Competencies:
* Type casting functions: `int()`, `float()`, `complex()`, `str()`.
* Integer division (`//`) vs True division (`/`).
* Precision limitations of binary floating-point arithmetic (`0.1 + 0.2 != 0.3`) and the standard `decimal` module for financial applications.

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. NUMERICAL TYPES & OPERATIONS
# ==============================================================================

count = 1_000_000  # Underscore visual separators for readability (PEP 515)
ratio = 7 / 2      # True division -> 3.5 (always returns float)
quotient = 7 // 2  # Floor division -> 3 (returns int)
remainder = 7 % 2  # Modulo -> 1
power = 2 ** 8     # Exponentiation -> 256

# Arbitrary Precision Integer demonstration
huge_number = 10 ** 100  # A googol (1 followed by 100 zeroes) - executes with zero overflow!
print(f"Huge number length: {len(str(huge_number))} digits")

# ==============================================================================
# 2. TYPE CASTING & CONVERSIONS
# ==============================================================================

str_val = "1042"
int_val = int(str_val)       # 1042
float_val = float(str_val)   # 1042.0

# Truncation behavior in int() casting
truncated = int(9.99)        # 9 (truncates toward zero, does NOT round!)

# ==============================================================================
# 3. FLOATING POINT PRECISION TRAP & THE DECIMAL FIX
# ==============================================================================

print(0.1 + 0.2)             # 0.30000000000000004
print(0.1 + 0.2 == 0.3)      # False!

from decimal import Decimal

# For banking and e-commerce transactions:
price1 = Decimal("0.10")
price2 = Decimal("0.20")
total = price1 + price2
print(f"Accurate financial decimal sum: {total}")  # 0.30 (Exact!)
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **Financial Rounding Bugs**: Storing currencies as raw `float` in PostgreSQL or Python will cause rounding discrepancies in reconciliation ledgers. Always store monetary figures in base units (cents/paise) as integers, or use Python's `decimal.Decimal`.
* **Casting Unsanitized User Input**: `int("12.5")` raises `ValueError: invalid literal for int() with base 10`. You must first cast to float: `int(float("12.5"))` or properly validate with schemas (e.g. Pydantic).

> [!WARNING]
> **Production Gotcha**: Floor division with negative numbers rounds down away from zero: `-7 // 2` is `-4`, not `-3`!

---

## 4. Exam & Technical Interview Gotchas

1. **How `int()` Handles Different Radices**: `int("1010", 2)` parses binary to 10; `int("FF", 16)` parses hex to 255.
2. **Boolean is an Integer Subclass**: `isinstance(True, int)` evaluates to `True`. Because `bool` inherits from `int`, `True + True == 2`.
3. **Comparing Floats**: Never compare floats using `a == b`. Always use `math.isclose(a, b, rel_tol=1e-9)`.

---

## 5. Mythos Mentorship Bridge

Learn how senior engineers design high-accuracy calculation engines in the **[MYTHOS Live Weekend Cohort](/register?source=library_python_numbers)**.
"""

        elif slug == "python-booleans-operators":
            return """
## 1. Academic Definition & Objectives

The `bool` type represents truth values in Python. It has exactly two singleton instances: `True` and `False`.
In Python, all objects can be tested for truth value (often referred to as **Truthy** vs. **Falsy**) when evaluated inside an `if` or `while` condition.

Key Competencies:
* The Falsy set: `None`, `False`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`.
* Logical operators: `and`, `or`, `not`.
* **Short-circuit evaluation**: Python stops evaluating logical expressions as soon as the outcome is deterministic.
* Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) vs Logical operators (`and`, `or`, `not`).

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. TRUTHY AND FALSY EVALUATION
# ==============================================================================

def validate_user_payload(payload: dict) -> bool:
    # Direct pythonic check: empty dict evaluates to False
    if not payload:
        return False
    
    # Check required fields
    has_email = bool(payload.get("email"))
    has_valid_age = payload.get("age", 0) >= 18
    return has_email and has_valid_age

# ==============================================================================
# 2. SHORT-CIRCUIT EVALUATION PATTERNS
# ==============================================================================

# 'or' returns the first Truthy operand, or the last operand if all are Falsy
configured_port = None
port = configured_port or 8080  # Defaults to 8080
print(f"Target Port: {port}")

# 'and' returns the first Falsy operand, or the last operand if all are Truthy
user = {"name": "Aditya", "role": "admin"}
is_admin = user and user.get("role") == "admin"
print(f"Is Admin: {is_admin}")

# ==============================================================================
# 3. IDENTITY (is) VS EQUALITY (==)
# ==============================================================================

a = [10, 20]
b = [10, 20]

print(a == b)  # True: values are equal
print(a is b)  # False: separate memory locations on heap!

val = None
# ALWAYS use 'is None' or 'is not None' for singleton checks
if val is None:
    print("Value is explicitly unassigned.")
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Zero-Default Bug**: Using `port = input_port or 8080` fails when `input_port = 0` (a valid port for dynamic OS binding in networking) because `0` is Falsy. Use `input_port if input_port is not None else 8080`.
* **Bitwise vs Logical Confusion**: Using `&` instead of `and` between booleans does not perform short-circuiting! If the right-hand operand causes an exception (e.g. `obj is not None & obj.is_valid()`), using `&` will crash with `AttributeError`.

> [!WARNING]
> **Production Gotcha**: Never write `if variable == True:`. Write `if variable:`. Comparing to `True` using `==` breaks custom classes implementing `__bool__` and exposes subtle typing bugs.

---

## 4. Exam & Technical Interview Gotchas

1. **Return Values of `and` and `or`**: In Python, `and` and `or` do not return boolean `True` or `False`; they return the actual operand that determined the result! `("Mythos" or 50)` evaluates to `"Mythos"`.
2. **Chained Comparison Operators**: Python supports mathematical chained comparisons: `1 < x < 10` is evaluated as `(1 < x) and (x < 10)`, evaluating `x` only once.
3. **Operator Precedence**: `not` has higher precedence than `and`, and `and` has higher precedence than `or`.

---

## 5. Mythos Mentorship Bridge

Step into professional software engineering with hands-on labs in the **[MYTHOS Live Weekend Cohort](/register?source=library_python_booleans)**.
"""

        elif slug == "python-while-loops":
            return """
## 1. Academic Definition & Objectives

A `while` loop repeatedly executes a target block of statements as long as a given boolean condition remains `True`.

Key Competencies:
* Loop condition evaluation and loop termination mechanics.
* `break` (immediate loop termination) vs `continue` (skip to the next iteration).
* The unique Python `while ... else` construct: the `else` block executes when the loop condition becomes `False`, but is skipped if the loop is broken via `break`.

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. BASIC WHILE LOOP WITH ITERATOR STEP
# ==============================================================================

retry_count = 0
MAX_RETRIES = 3

while retry_count < MAX_RETRIES:
    retry_count += 1
    print(f"[RETRY ATTEMPT] {retry_count}/{MAX_RETRIES} attempting database connection...")

# ==============================================================================
# 2. BREAK AND CONTINUE IN POLLING LOOPS
# ==============================================================================

import time

queue = ["job_1", "skip_me", "job_2", "STOP", "job_3"]

while queue:
    current_job = queue.pop(0)
    
    if current_job.startswith("skip_"):
        print(f"[SKIPPED] {current_job}")
        continue  # Skip processing and move to next item
        
    if current_job == "STOP":
        print("[TERMINATING] Emergency stop signal received.")
        break  # Exit loop immediately
        
    print(f"[PROCESSED] Successfully executed {current_job}")

# ==============================================================================
# 3. THE PYTHON 'WHILE ... ELSE' PATTERN
# ==============================================================================

# Search algorithm: find prime candidate
number = 17
divisor = 2
is_prime = True

while divisor * divisor <= number:
    if number % divisor == 0:
        print(f"{number} is composite (divisible by {divisor})")
        break
    divisor += 1
else:
    # Executes ONLY if loop finished without hitting a 'break'
    print(f"{number} is confirmed a Prime Number!")
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **Infinite Loop CPU Starvation**: Writing `while True:` without a blocking sleep (`time.sleep()`), socket poll, or async wait (`await asyncio.sleep()`) will peg the CPU core at 100% utilization.
* **Exponential Backoff**: In production distributed systems, polling loops must implement exponential backoff with jitter to avoid hammering downstream services during outages.

> [!WARNING]
> **Production Gotcha**: Modifying a collection while iterating over it in a `while` loop can cause index drift or infinite loops. Always maintain explicit tracking variables.

---

## 4. Exam & Technical Interview Gotchas

1. **`while ... else` Semantics**: In oral exams and viva questions, 90% of candidates mistakenly claim that the `else` block in a `while` loop executes if the condition is false initially. In fact, it executes whenever the loop finishes naturally without executing `break`.
2. **Off-by-One Errors**: Be meticulous with `<` vs `<=`.
3. **Condition Mutation**: Always ensure the variable governing the loop test is mutated inside the block, or the loop will never terminate.

---

## 5. Mythos Mentorship Bridge

Build distributed job workers and streaming consumer loops in the **[MYTHOS Live Weekend Cohort](/register?source=library_python_while)**.
"""

        elif slug == "python-for-loops-range":
            return """
## 1. Academic Definition & Objectives

Unlike traditional C or Java `for` loops that manipulate an index variable (`for (int i=0; i<n; i++)`), Python's `for` loop is a **collection iterator**. It iterates over items in any **iterable** (lists, tuples, strings, dictionaries, sets, generators) following the **Iterator Protocol** (`__iter__()` and `__next__()`).

Key Competencies:
* The `range(start, stop, step)` built-in sequence generator.
* Built-in iteration helpers: `enumerate()`, `zip()`, `reversed()`, `sorted()`.
* Dictionary iteration (`.keys()`, `.values()`, `.items()`).
* The `for ... else` clause.

---

## 2. Core Concepts & Implementation Blueprint

```python
# ==============================================================================
# 1. RANGE FUNCTION & ENUMERATE
# ==============================================================================

# range(start, stop, step) generates values on-demand without storing them in memory
for i in range(1, 10, 2):
    print(f"Odd step value: {i}")  # 1, 3, 5, 7, 9

# Idiomatic index tracking with enumerate() - NEVER use range(len(items))!
servers = ["web-01", "api-01", "db-primary", "cache-01"]

for rank, server in enumerate(servers, start=1):
    print(f"Priority #{rank}: {server}")

# ==============================================================================
# 2. PARALLEL ITERATION WITH ZIP()
# ==============================================================================

metrics = ["CPU", "Memory", "Disk I/O"]
readings = [42.5, 78.1, 12.0]

for metric, reading in zip(metrics, readings):
    print(f"[TELEMETRY] {metric}: {reading}%")

# ==============================================================================
# 3. DICTIONARY UNPACKING & FOR...ELSE
# ==============================================================================

configs = {"host": "127.0.0.1", "port": 5432, "ssl_mode": "require"}

for key, val in configs.items():
    print(f"Configuration -> {key} = {val}")

# Search with for...else
forbidden_keys = ["admin_password", "secret_key"]
for k in configs.keys():
    if k in forbidden_keys:
        print(f"[SECURITY ALERT] Leak detected: {k}")
        break
else:
    print("[SECURITY CLEAR] No sensitive secrets in payload.")
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **Range in Python 3 is Memory Efficient**: In Python 2, `range(1000000)` allocated a list of one million integers in RAM. In Python 3, `range()` is an immutable sequence object that computes elements lazily on demand in $O(1)$ memory.
* **`zip()` Truncation Trap**: By default, `zip(list_a, list_b)` silently stops at the shortest list! If `list_a` has 10 items and `list_b` has 3, 7 items are silently ignored. In production, use `itertools.zip_longest()` when mismatched lengths indicate data loss.

> [!WARNING]
> **Production Gotcha**: Never write `for i in range(len(my_list)): val = my_list[i]`. It is an unpythonic anti-pattern. Use `for item in my_list:` or `for idx, item in enumerate(my_list):`.

---

## 4. Exam & Technical Interview Gotchas

1. **Modifying an Iterable During Iteration**: Modifying a list (adding or deleting elements) while iterating over it causes skipped elements or infinite loops. Always iterate over a shallow copy (`for item in my_list.copy():`).
2. **Unpacking with `zip(*matrix)`**: Used to transpose matrices in one line: `transposed = list(zip(*matrix))`.
3. **`range()` Object Attributes**: `range` objects support $O(1)$ containment checks (`x in range(...)`) and index slicing without generating elements.

---

## 5. Mythos Mentorship Bridge

Learn to build high-performance data transformation loops and vectorization workflows in the **[MYTHOS Live Weekend Cohort](/register?source=library_python_for)**.
"""

    elif subject == "sql":
        if slug == "sql-what-is-database":
            return """
## 1. Academic Definition & Objectives

A **Database** is an organized, structured collection of digital data stored electronically in a computer system, managed by a dedicated software suite called a **Database Management System (DBMS)**.

In relational systems (RDBMS) formulated by Dr. Edgar F. Codd (1970), data is structured into **Relations** (commonly called **Tables**), consisting of:
* **Attributes (Columns / Fields)**: Named properties with defined data types (e.g., `student_id INT`, `email VARCHAR(100)`).
* **Tuples (Rows / Records)**: Individual entity entries conforming to the table schema.
* **Domain**: The set of permissible atomic values for a given column.

Key Competencies:
* The difference between flat files (CSV, JSON, Excel) and an RDBMS (concurrency, crash recovery, ACID transactions).
* Client-Server Architecture: Database engine listening on a TCP port (e.g. MySQL `3306`, PostgreSQL `5432`) receiving SQL queries from client applications.
* Relational terminology: Relation = Table, Tuple = Row, Attribute = Column, Cardinality = Number of Rows, Degree (Arity) = Number of Columns.

---

## 2. Core Concepts & Implementation Blueprint

```text
+-------------------------------------------------------------------------+
|                       RELATIONAL DATABASE MODEL                         |
+-------------------------------------------------------------------------+
| DATABASE: mythos_institute                                              |
|                                                                         |
|  TABLE: students (Degree/Arity = 4 Attributes)                          |
|  +------------+------------------+---------------------+--------------+  |
|  | student_id | full_name        | email               | phone        |  |
|  +------------+------------------+---------------------+--------------+  |
|  | 101        | Aditya Sharma    | aditya@example.com  | 9876543210   |  |
|  | 102        | Priya Patel      | priya@example.com   | 9876543211   |  |
|  | 103        | Rohan Verma      | rohan@example.com   | 9876543212   |  |
|  +------------+------------------+---------------------+--------------+  |
|  (Cardinality = 3 Tuples/Rows)                                          |
+-------------------------------------------------------------------------+

CLIENT-SERVER ARCHITECTURE PIPELINE:
[ Backend App / API ] ---> [ Connection Pool ] ---> [ SQL Parser ] ---> [ Query Planner ] ---> [ Storage Engine (B-Tree / Disk) ]
```

```sql
-- Conceptual database verification queries
-- 1. Inspect existing databases on the server
SHOW DATABASES;

-- 2. View active connection status
SELECT current_user, version();
```

---

## 3. The Production Reality ("What Textbooks Skip")

Textbooks explain databases as simple storage boxes. In enterprise production systems:

* **Connection Pool Saturation**: Every incoming API worker opens a TCP socket to the database. Without connection pooling (such as PgBouncer or HikariCP), 500 concurrent HTTP requests will spawn 500 OS processes/threads on PostgreSQL, exhausting server RAM and leading to `FATAL: remaining connection slots are reserved for non-replication superuser connections`.
* **ACID vs. BASE Trade-Offs**: Relational databases guarantee ACID (Atomicity, Consistency, Isolation, Durability) at the expense of horizontal write scalability. NoSQL databases (like Cassandra or DynamoDB) sacrifice strong consistency for distributed horizontal scaling.
* **Disk IOPS & WAL**: Updates in an RDBMS do not immediately rewrite table files on SSDs; they append to a sequential Write-Ahead Log (WAL / Redo Log) in memory before asynchronous flush to minimize random disk I/O.

> [!NOTE]
> **Production Rule**: Never store binary media files (PDFs, images, videos) inside an RDBMS as `BLOB` columns. Store the binary file in cloud object storage (Amazon S3, Google Cloud Storage) and save only the resulting CDN URL string in the database column.

---

## 4. Exam & Technical Interview Gotchas

1. **Cardinality vs. Arity (Degree)**: In written exams, 80% of students confuse these terms:
   - **Cardinality** = Total number of **Rows (Tuples)** in a table.
   - **Degree (Arity)** = Total number of **Columns (Attributes)** in a table.
2. **Data Redundancy vs. Inconsistency**: Redundancy means duplicate data stored in multiple places. Inconsistency occurs when one copy is updated and another copy remains outdated.
3. **Data Independence**: Logical Data Independence means modifying conceptual schemas (adding a column) without breaking user applications. Physical Data Independence means modifying storage structures (switching from B-Tree to Hash index) without modifying SQL queries.

---

## 5. Mythos Mentorship Bridge

Learn to design normalized schemas, tune connection pools, and deploy cloud PostgreSQL clusters in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_what_is_database)**.
"""

        elif slug == "sql-intro-syntax":
            return """
## 1. Academic Definition & Objectives

**SQL (Structured Query Language)** is the international standard declarative domain-specific language (ANSI/ISO) used to communicate with, query, and manipulate relational database management systems.

Unlike imperative languages (like Python or Java) where you write step-by-step instructions on *how* to calculate an outcome, SQL is **declarative**: you specify *what* data you need, and the database query engine's cost-based optimizer determines the most efficient execution plan.

Key Competencies:
* The 5 functional sublanguages of SQL.
* Case-insensitivity rules: Keywords are case-insensitive (`SELECT` vs `select`), but identifier case-sensitivity depends on the underlying OS and database configuration.
* Semicolons: The standard SQL statement terminator required in multi-statement scripts.
* Comments: Single-line (`--`) and multi-line (`/* ... */`).

### The 5 SQL Sublanguages Taxonomy

| Sublanguage | Full Name | Core Commands | Purpose |
| :--- | :--- | :--- | :--- |
| **DQL** | Data Query Language | `SELECT` | Retrieve data tuples matching criteria |
| **DDL** | Data Definition Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | Define, alter, and destroy schemas & tables |
| **DML** | Data Manipulation Language | `INSERT`, `UPDATE`, `DELETE` | Mutate row data within tables |
| **DCL** | Data Control Language | `GRANT`, `REVOKE` | Manage security privileges and user roles |
| **TCL** | Transaction Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Manage atomic transaction boundaries |

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. SQL SYNTAX STANDARD CONVENTIONS
-- ==============================================================================

-- Best Practice: UPPERCASE for SQL keywords, lowercase for table and column names
-- Single-line comment starts with double hyphen (--)

/*
   Multi-line block comment:
   This script demonstrates standard DDL, DML, and DQL query structures.
*/

-- DDL: Create a schema structure
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    track VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- DML: Insert tuple records
INSERT INTO courses (course_id, course_name, track)
VALUES 
    (1, 'Performance Marketing & Paid Ads', 'Digital Marketing'),
    (2, 'Data Analysis Masterclass', 'Data Analytics');

-- DQL: Query projected attributes
SELECT 
    course_id,
    course_name,
    track
FROM courses
WHERE is_active = TRUE
ORDER BY course_id ASC;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **Table Name Case Sensitivity on Linux**: On Windows, MySQL table names are case-insensitive because NTFS filesystem paths are case-insensitive. On Linux (production servers), MySQL uses the case-sensitive ext4 filesystem by default! A query like `SELECT * FROM Courses;` that works on your local Windows laptop will crash with `Table 'mythos.Courses' doesn't exist` when deployed to Linux. Always use strictly lowercase identifiers (`lower_case_table_names`).
* **SQL Injection Vulnerabilities**: String concatenation (`f"SELECT * FROM users WHERE email = '{user_email}'"`) allows malicious attackers to enter `' OR 1=1 --` to dump entire databases. In production, **always** use parameterized queries / prepared statements (`cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))`).
* **Semicolon Mandatory in Scripts**: While some GUI tools let you run a single query without a trailing semicolon, automated CI/CD migration runners (like Flyway, Alembic, or Liquibase) require semicolons to parse statement boundaries.

> [!WARNING]
> **Production Gotcha**: Never execute ad-hoc, untracked DDL statements directly in production terminals. Always version-control all database schema changes inside migration files (`versions/001_initial_tables.sql`).

---

## 4. Exam & Technical Interview Gotchas

1. **Is `TRUNCATE` DDL or DML?**: High-frequency exam question! `DELETE` is DML (it scans rows and can be rolled back in some engines). `TRUNCATE` is strictly **DDL** because it deallocates the table's underlying storage pages and resets high-water marks.
2. **Which sublanguage does `SELECT` belong to?**: In textbook classification, `SELECT` belongs to **DQL (Data Query Language)**, though some older university syllabi group it under DML.
3. **Keyword Precedence**: SQL execution order is **NOT** the same as written syntax order! Written order starts with `SELECT`, but the engine executes `FROM` and `WHERE` first.

---

## 5. Mythos Mentorship Bridge

Master production SQL query design, migration tools, and query plan profiling in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_intro_syntax)**.
"""

        elif slug == "sql-create-drop-database":
            return """
## 1. Academic Definition & Objectives

In SQL systems, a **Database** (or **Catalog**) is a named namespace container that encapsulates tables, views, stored routines, indexes, and user permissions.

DDL database management commands initialize, configure, and destroy these database catalog namespaces:
* `CREATE DATABASE`: Allocates a new physical directory and catalog registry on the storage engine.
* `DROP DATABASE`: Deletes the database catalog and permanently unlinks all underlying data files, tables, and indexes from disk.
* `USE`: Sets the active working database context for subsequent queries in the current session.

Key Competencies:
* Idempotency with `IF NOT EXISTS` and `IF EXISTS`.
* Character sets (`utf8mb4`) and collation sequences (`utf8mb4_unicode_ci`).
* Server privilege requirements (`CREATE` and `DROP` privileges).

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. CREATING DATABASES IDEMPOTENTLY WITH CHARACTER SETS
-- ==============================================================================

-- Create database only if it does not already exist
-- utf8mb4 supports full 4-byte UTF-8, including emojis and international characters
CREATE DATABASE IF NOT EXISTS mythos_academy
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- View all databases on the database instance
SHOW DATABASES;

-- Switch session context to the new database
USE mythos_academy;

-- Inspect currently selected database
SELECT DATABASE();

-- ==============================================================================
-- 2. DROPPING DATABASES SAFELY
-- ==============================================================================

-- Dropping a database permanently removes all contained tables and data
DROP DATABASE IF EXISTS test_staging_db;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Disaster of `DROP DATABASE`**: In production environments, running `DROP DATABASE` is instantaneous and unrecoverable without restoring Point-In-Time Backups (PITR) from WAL logs. Production application database users must **never** have the `DROP` privilege granted to their service credentials.
* **Character Set Trap (`utf8` vs `utf8mb4`)**: In MySQL, the legacy `utf8` character set only supports up to 3 bytes per character. Inserting a 4-byte character (such as an emoji 🚀 or certain Asian language glyphs) will cause queries to crash with `Incorrect string value`. Always specify `utf8mb4`.
* **Collation and Sorting**: Collation defines how strings are compared and sorted. `utf8mb4_bin` performs exact binary comparisons (case-sensitive), whereas `utf8mb4_unicode_ci` performs case-insensitive comparisons where `'admin'` equals `'Admin'`.

> [!WARNING]
> **Production Gotcha**: Cloud databases (like AWS RDS, Azure Database, Render PostgreSQL) do not allow running `CREATE DATABASE` from ordinary user accounts. The database is provisioned through cloud console or Terraform blueprints.

---

## 4. Exam & Technical Interview Gotchas

1. **What happens to active client connections when `DROP DATABASE` executes?**: In PostgreSQL and MySQL, if clients are connected to the target database, dropping it will either fail with `database is being accessed by other users` or forcibly sever all active TCP sockets.
2. **Database vs Schema in PostgreSQL vs MySQL**:
   - In **MySQL**, `DATABASE` and `SCHEMA` are exact synonyms (`CREATE SCHEMA` is identical to `CREATE DATABASE`).
   - In **PostgreSQL**, a single Database can contain multiple isolated `Schemas` (namespaces), commonly defaulting to the `public` schema.
3. **`SHOW DATABASES` Permission Filtering**: Non-superuser accounts only see databases they have explicit privileges to access.

---

## 5. Mythos Mentorship Bridge

Learn to provision secure cloud databases, configure replication clusters, and automate backups in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_create_drop_database)**.
"""

        elif slug == "sql-create-drop-table":
            return """
## 1. Academic Definition & Objectives

The `CREATE TABLE` statement is the core DDL command used to establish a new relation in the active database. It declares the table name, its constituent attributes (columns), their data types, default values, and column/table-level integrity constraints.

`DROP TABLE` destroys the table definition and all row data stored within it, removing the catalog metadata entry.

Key Competencies:
* Fundamental SQL Data Types:
  - Exact Numerics: `INT`, `BIGINT`, `SMALLINT`, `DECIMAL(precision, scale)`
  - Strings: `VARCHAR(length)`, `CHAR(length)`, `TEXT`
  - Dates & Times: `DATE`, `TIME`, `TIMESTAMP`, `DATETIME`
  - Booleans: `BOOLEAN`
* Idempotent operations: `CREATE TABLE IF NOT EXISTS` and `DROP TABLE IF EXISTS`.
* Defining Primary Keys and column constraints inline.

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. COMPLETE PRODUCTION DDL TABLE SCHEMA
-- ==============================================================================

CREATE TABLE IF NOT EXISTS students (
    student_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(150) NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    enrollment_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 2. VIEWING TABLE STRUCTURE
-- ==============================================================================

-- In MySQL: Inspect column data types, keys, and nullability
DESCRIBE students;

-- In ANSI SQL: Query information_schema catalog
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'students';

-- ==============================================================================
-- 3. DROPPING TABLES SAFELY
-- ==============================================================================

-- Permanently drop the table if it exists
DROP TABLE IF EXISTS temp_student_imports;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **`DECIMAL` vs `FLOAT`**: Textbooks often use `FLOAT` or `DOUBLE` for financial data. In production, this causes catastrophic floating-point rounding errors (e.g. `0.1 + 0.2 = 0.30000000000000004`). Always use `DECIMAL(precision, scale)` (such as `DECIMAL(12, 2)`) for money and transactions to ensure exact mathematical precision.
* **`BIGINT` vs `INT` for Primary Keys**: A standard 4-byte signed `INT` tops out at 2,147,483,647 (2.14 billion rows). Fast-growing systems (events, clickstreams, audit logs) that use `INT` for primary keys will crash when IDs overflow. Always declare auto-increment IDs as `BIGINT` (8 bytes, up to 9 quintillion).
* **`VARCHAR(255)` Myth**: Many tutorials blindly set every string to `VARCHAR(255)`. In modern databases (like MySQL InnoDB and PostgreSQL), `VARCHAR(n)` only consumes storage for the actual characters stored plus 1 or 2 bytes of length prefix. However, setting overly large column widths causes in-memory temporary tables to allocate excessive RAM during sorts.

> [!WARNING]
> **Production Gotcha**: Dropping a table that is referenced by a Foreign Key in another table will be blocked with a foreign key constraint violation error. You must either drop the referencing child table first or drop the foreign key constraint.

---

## 4. Exam & Technical Interview Gotchas

1. **`CHAR` vs `VARCHAR`**:
   - `CHAR(n)` is fixed-length: values shorter than n are right-padded with spaces. Ideal for fixed-length codes (e.g. `country_code CHAR(2)`, SHA-256 hashes `CHAR(64)`).
   - `VARCHAR(n)` is variable-length: stores only the actual characters + 1-2 length bytes.
2. **`DROP TABLE` vs `TRUNCATE TABLE` vs `DELETE FROM`**:
   - `DROP TABLE`: Removes table definition + all data + indexes + triggers from the catalog.
   - `TRUNCATE TABLE`: Retains table definition and structure, but wipes all rows by deallocating storage pages. Resets auto-increment IDs.
   - `DELETE FROM`: DML row-by-row removal; logs individual row deletions and can be rolled back.
3. **`TIMESTAMP` vs `DATETIME`**:
   - `TIMESTAMP`: Stored as UTC seconds since Unix Epoch (1970); converts automatically to session timezone on retrieval. Maximum year: 2038 (on 32-bit representations).
   - `DATETIME`: Stores raw date and time as written, independent of server timezone.

---

## 5. Mythos Mentorship Bridge

Learn production schema design, data modeling, and automated database migration pipelines in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_create_drop_table)**.
"""

        elif slug == "sql-alter-truncate-table":
            return """
## 1. Academic Definition & Objectives

As software applications evolve, database structures must adapt without destroying existing historical data. The `ALTER TABLE` DDL statement provides mechanisms to modify the schema of an existing relation.

Core operations include:
* Adding new columns (`ADD COLUMN`).
* Removing obsolete columns (`DROP COLUMN`).
* Changing column data types or constraints (`MODIFY / ALTER COLUMN`).
* Renaming columns or tables (`RENAME`).
* Wiping all data rows while keeping schema intact (`TRUNCATE TABLE`).

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. EVOLVING EXISTING TABLE SCHEMAS WITH ALTER TABLE
-- ==============================================================================

-- Add a new column with default value
ALTER TABLE students 
ADD COLUMN linkedin_profile VARCHAR(255) NULL;

-- Modify existing column data type (expanding width)
ALTER TABLE students 
MODIFY COLUMN phone VARCHAR(30) NOT NULL;

-- Drop an unwanted column
ALTER TABLE students 
DROP COLUMN status;

-- Add a new index for faster lookups
ALTER TABLE students 
ADD INDEX idx_students_phone (phone);

-- ==============================================================================
-- 2. TRUNCATE TABLE: INSTANT ROW PURGING
-- ==============================================================================

-- Truncate resets the table to zero rows while preserving structure
TRUNCATE TABLE temp_student_imports;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **Exclusive Metadata Table Locks**: In production databases with millions of rows, running `ALTER TABLE students ADD COLUMN ...` can acquire an exclusive table lock (`AccessExclusiveLock` in PostgreSQL or `Metadata Lock` in MySQL). While locked, all incoming `SELECT`, `INSERT`, and `UPDATE` queries queue up and timeout, causing a total application outage!
* **Online DDL Tools**: High-traffic systems use online schema migration tools like `gh-ost` (GitHub's Online Schema Transmogrifier) or `pt-online-schema-change` which create ghost tables, mirror live writes via binlogs/triggers, and swap tables in milliseconds without locking.
* **Why `TRUNCATE` is O(1) Lightning Fast**: `DELETE FROM table;` reads each row individually, writes undo/redo log records, and updates index trees (O(N) operations). `TRUNCATE TABLE` bypasses row scanning and simply deallocates the underlying data extents and pages on disk, returning in milliseconds regardless of table size.

> [!WARNING]
> **Production Gotcha**: In MySQL, `TRUNCATE` cannot be rolled back even inside a `START TRANSACTION` block because DDL statements issue an implicit commit! In PostgreSQL, `TRUNCATE` is transaction-safe and can be rolled back.

---

## 4. Exam & Technical Interview Gotchas

1. **The Classic 3-Way Comparison Table (Memorize for Viva & Written Exams)**:

| Feature | `DELETE` | `TRUNCATE` | `DROP` |
| :--- | :--- | :--- | :--- |
| **Category** | DML | DDL | DDL |
| **`WHERE` Clause?** | Yes (optional) | No (all rows wiped) | No |
| **Performance** | Slow (O(N) row-by-row) | Fast (O(1) page wipe) | Instantaneous |
| **Rollback in Txn** | Yes (all engines) | Engine-dependent | Engine-dependent |
| **Auto-Increment** | Preserved | Reset to seed (1) | Destroyed |
| **Table Structure** | Remains | Remains | Destroyed |
| **Fires Triggers?** | Yes (`BEFORE/AFTER DELETE`) | No | No |

2. **Dropping Column Constraints**: You cannot simply drop a column if a foreign key or index depends on it; you must drop the foreign key constraint first.

---

## 5. Mythos Mentorship Bridge

Learn zero-downtime database migration strategies used by high-scale tech firms in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_alter_truncate_table)**.
"""

        elif slug == "sql-select-distinct":
            return """
## 1. Academic Definition & Objectives

The `SELECT` statement implements the fundamental relational algebra **Projection Operator**, extracting specified attributes from a relation.

`SELECT DISTINCT` applies deduplication on the projected tuple set, returning only unique combinations of values.

Key Competencies:
* Projecting specific columns vs wildcard (`SELECT *`).
* Calculating derived expressions and constants.
* Applying column aliases (`AS`).
* Deduplicating rows with `DISTINCT`.

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. RELATIONAL PROJECTION (SELECT)
-- ==============================================================================

-- Explicit projection: Only retrieve the attributes needed by your application
SELECT 
    student_id, 
    first_name, 
    last_name, 
    email 
FROM students;

-- Calculated columns with aliases
SELECT 
    first_name,
    last_name,
    enrollment_fee,
    enrollment_fee * 0.18 AS gst_tax_amount,
    enrollment_fee * 1.18 AS total_payable
FROM students;

-- ==============================================================================
-- 2. DEDUPLICATION (SELECT DISTINCT)
-- ==============================================================================

-- Get unique cities where our enrolled students live
SELECT DISTINCT city 
FROM students;

-- DISTINCT across multiple columns: evaluates uniqueness on the combination
SELECT DISTINCT track, status 
FROM courses;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Anti-Pattern of `SELECT *`**: Never write `SELECT *` in production backend code:
  1. **Network Overhead**: Transmits unused columns (like heavy JSON, TEXT, or audit metadata) over the network.
  2. **Breaks Index-Only Covering Scans**: An index containing `(status, email)` can answer `SELECT email FROM users WHERE status = 'active'` entirely from RAM cache. Using `SELECT *` forces the engine to perform expensive disk lookups for every matching row.
  3. **Fragile Schemas**: Adding a column to a table alters the tuple layout and breaks positional API deserializers.
* **Cost of `DISTINCT`**: To evaluate `DISTINCT`, the database engine must sort the result set in memory or build an in-memory hash table. On large result sets, this causes heavy CPU spikes and spills temporary sort runs to disk (`temporary tables on disk`).

> [!NOTE]
> **Production Tip**: If you find yourself writing `SELECT DISTINCT` to fix duplicate rows in a query with multiple `JOIN`s, your join predicate is probably missing a key condition! Fix the join condition instead of masking it with `DISTINCT`.

---

## 4. Exam & Technical Interview Gotchas

1. **How does `DISTINCT` handle `NULL` values?**: In SQL standard, all `NULL` values are treated as duplicate entries under `DISTINCT`. If a column contains 10 rows with `NULL`, `SELECT DISTINCT` returns exactly one `NULL` row.
2. **`DISTINCT` Scope**: Many junior developers mistakenly think `SELECT DISTINCT col1, col2` only deduplicates `col1`. In SQL, `DISTINCT` applies to the **entire row tuple** `(col1, col2)` combined!
3. **Execution Order**: `SELECT` is evaluated **after** `FROM`, `WHERE`, `GROUP BY`, and `HAVING`, but **before** `ORDER BY` and `LIMIT`.

---

## 5. Mythos Mentorship Bridge

Learn to write high-efficiency, index-friendly analytical SQL queries in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_select_distinct)**.
"""

        elif slug == "sql-where-clause":
            return """
## 1. Academic Definition & Objectives

The `WHERE` clause implements the relational algebra **Selection Operator**, filtering tuples from a relation based on a specified boolean predicate. Only tuples for which the predicate evaluates to `TRUE` are returned.

Key Competencies:
* Comparison operators: `=`, `<>`, `!=`, `>`, `<`, `>=`, `<=`.
* Text string comparisons (enclosed in single quotes `'value'`) vs numerical comparisons.
* Date filtering syntax.
* Understanding SQL's Three-Valued Logic (TRUE, FALSE, UNKNOWN).

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. BASIC RELATIONAL SELECTION
-- ==============================================================================

-- Equality on strings (case-insensitive in default MySQL collations)
SELECT student_id, first_name, email
FROM students
WHERE status = 'enrolled';

-- Numerical comparison
SELECT student_id, first_name, enrollment_fee
FROM students
WHERE enrollment_fee >= 5000.00;

-- Inequality operators (<> is standard ANSI; != is also supported)
SELECT course_id, course_name, track
FROM courses
WHERE track <> 'Archived';

-- Date comparisons (Standard ISO format: YYYY-MM-DD)
SELECT student_id, full_name, created_at
FROM students
WHERE created_at >= '2026-01-01';
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **SARGable Queries (Search Argument Able)**: For a database engine to use an index on a column, the query must be **SARGable**. Wrapping a column inside a function prevents index usage and triggers catastrophic full table scans:
  ```sql
  -- BAD (Non-SARGable): Disables index on created_at, scans 5 million rows!
  SELECT * FROM orders WHERE YEAR(created_at) = 2026;

  -- GOOD (SARGable): High-speed B-Tree index range scan!
  SELECT * FROM orders 
  WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';
  ```
* **Implicit Type Coercion Trap**: If `phone` is defined as `VARCHAR(20)` and you query `WHERE phone = 9876543210` (as an integer without quotes), MySQL implicitly converts every single stored string to an integer before comparing, causing a full table scan and ignoring the index! Always quote string parameters: `WHERE phone = '9876543210'`.

> [!WARNING]
> **Production Gotcha**: Never test for NULL values with `= NULL` (e.g. `WHERE email = NULL`). In SQL, comparing anything to NULL using `=` evaluates to `UNKNOWN` (falsy), returning zero rows. You must strictly use `IS NULL` or `IS NOT NULL`.

---

## 4. Exam & Technical Interview Gotchas

1. **Standard Inequality Operator**: While `!=` is widely supported, `<>` is the official ISO/ANSI SQL standard operator for inequality.
2. **Three-Valued Logic**: In SQL, conditional predicates evaluate to one of three states:
   - `TRUE` (included in result)
   - `FALSE` (excluded)
   - `UNKNOWN` (excluded)
3. **Execution Order**: `WHERE` filters rows **before** any grouping or aggregation takes place. You cannot use aggregate functions (`SUM`, `AVG`, `COUNT`) inside a `WHERE` clause.

---

## 5. Mythos Mentorship Bridge

Learn query execution planning and indexing strategies in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_where_clause)**.
"""

        elif slug == "sql-insert-into":
            return """
## 1. Academic Definition & Objectives

The `INSERT INTO` statement is the primary DML command used to add new tuples (rows) into an existing database table.

Syntactic variations include:
* Inserting with explicit column declarations (recommended standard).
* Inserting into all table columns positionally.
* Batch inserting multiple rows in a single atomic SQL statement.
* Inserting the result of a subquery (`INSERT INTO ... SELECT`).

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. EXPLICIT COLUMN INSERTION (PRODUCTION BEST PRACTICE)
-- ==============================================================================

-- Explicitly naming columns protects your code if table schema changes later
INSERT INTO students (first_name, last_name, email, phone, status)
VALUES ('Vikram', 'Malhotra', 'vikram@example.com', '9811223344', 'new');

-- ==============================================================================
-- 2. BULK MULTI-ROW INSERTION
-- ==============================================================================

-- Inserting multiple records in a single round-trip is 50x faster than single inserts
INSERT INTO courses (course_id, course_name, track)
VALUES 
    (10, 'Advanced SQL Query Tuning', 'Data Analytics'),
    (11, 'Meta Ads Manager Scaling', 'Digital Marketing'),
    (12, 'Power BI DAX Architectures', 'Data Analytics');

-- ==============================================================================
-- 3. INSERTING INTO ... SELECT
-- ==============================================================================

-- Copying data from a staging table into production
INSERT INTO alumni_archive (student_id, full_name, completion_date)
SELECT student_id, CONCAT(first_name, ' ', last_name), CURRENT_DATE
FROM students
WHERE status = 'graduated';
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Round-Trip Latency Penalty**: Executing 1,000 separate `INSERT INTO ...` statements inside an application `for` loop incurs 1,000 network round-trips and 1,000 separate disk sync operations (fsync). Combining them into one batch insert (`INSERT INTO ... VALUES (...), (...), (...)`) or wrapping them in a single transaction (`BEGIN ... COMMIT`) reduces execution time from 30 seconds to 100 milliseconds.
* **Idempotent Inserts / Upserts**: In production APIs, duplicate webhook deliveries or retried requests will fail with `Duplicate entry '...' for key 'PRIMARY'`. Modern databases provide Upsert patterns:
  - MySQL: `INSERT INTO ... ON DUPLICATE KEY UPDATE updated_at = NOW();`
  - PostgreSQL / SQLite: `INSERT INTO ... ON CONFLICT (id) DO UPDATE SET ...;`

> [!NOTE]
> **Production Tip**: For multi-million row data ingestion, bypass standard SQL `INSERT` statements entirely and use native bulk loaders like MySQL's `LOAD DATA INFILE` or PostgreSQL's `COPY` command.

---

## 4. Exam & Technical Interview Gotchas

1. **Default Column Values**: If an inserted row omits a column:
   - If the column has a `DEFAULT` or allows `NULL`, the database populates it automatically.
   - If the column is `NOT NULL` without a default value, the database raises an error (`Field 'phone' doesn't have a default value`).
2. **Retrieving the Auto-Generated Key**: How do you know what ID was assigned to an auto-increment column?
   - MySQL: `SELECT LAST_INSERT_ID();`
   - PostgreSQL: Append `RETURNING student_id;` to the `INSERT` statement.
3. **Transaction Rollback on Failed Batch**: If row 95 of a 100-row bulk insert violates a constraint, the entire statement fails and none of the 100 rows are inserted.

---

## 5. Mythos Mentorship Bridge

Learn high-speed data ingestion and ETL pipeline architecture in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_insert_into)**.
"""

        elif slug == "sql-update":
            return """
## 1. Academic Definition & Objectives

The `UPDATE` statement is the DML command used to mutate one or more existing records within a table. It modifies column values based on conditions specified in an optional `WHERE` clause.

Key Competencies:
* Updating single or multiple columns in a single statement.
* The critical importance of the `WHERE` clause.
* Performing arithmetic updates (e.g. `salary = salary * 1.10`).
* Safe update modes in database servers.

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. TARGETED RECORD UPDATES
-- ==============================================================================

-- Update single column for a specific student
UPDATE students 
SET status = 'enrolled'
WHERE student_id = 101;

-- Update multiple columns simultaneously
UPDATE students
SET 
    email = 'priya.new@example.com',
    phone = '9876500000',
    updated_at = CURRENT_TIMESTAMP
WHERE student_id = 102;

-- ==============================================================================
-- 2. COMPUTED ARITHMETIC UPDATES
-- ==============================================================================

-- Give a 10% fee discount to all students in the weekend batch
UPDATE students
SET enrollment_fee = enrollment_fee * 0.90
WHERE status = 'early_bird';
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Nightmare of `UPDATE` Without `WHERE`**: Omitting the `WHERE` clause will update **every single row** in the table! In production, this can accidentally overwrite all user emails or set all bank balances to zero.
* **MySQL Safe Updates (`SQL_SAFE_UPDATES`)**: Production databases and workbench clients enable safe update mode:
  ```sql
  SET SQL_SAFE_UPDATES = 1;
  ```
  In this mode, any `UPDATE` or `DELETE` that does not use a key column (like a `PRIMARY KEY`) in its `WHERE` clause is blocked with `Error Code: 1175. You are using safe update mode...`.
* **Atomic Transactions**: In mission-critical systems, always wrap manual updates in transactions so you can inspect the affected row count before making changes permanent:
  ```sql
  START TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE account_id = 42;
  -- Verify affected row count and balance:
  SELECT balance FROM accounts WHERE account_id = 42;
  -- If correct: COMMIT; Otherwise: ROLLBACK;
  ```

> [!WARNING]
> **Production Gotcha**: An `UPDATE` query acquires exclusive row-level locks on all matching rows. If two transactions update the same rows in opposite orders (Txn 1 updates A then B; Txn 2 updates B then A), a **Deadlock** occurs and the database aborts one transaction.

---

## 4. Exam & Technical Interview Gotchas

1. **Affected Rows vs Found Rows**: In MySQL, if an `UPDATE` query matches a row where the new value is identical to the current value, MySQL reports `Rows matched: 1  Changed: 0`.
2. **What if condition matches zero rows?**: The query succeeds with `Query OK, 0 rows affected`. It does NOT raise an error.
3. **Updating with a Subquery**: You can update values based on calculations from another table:
   ```sql
   UPDATE employees e
   SET e.department_name = (SELECT d.name FROM departments d WHERE d.id = e.dept_id)
   WHERE e.dept_id IS NOT NULL;
   ```

---

## 5. Mythos Mentorship Bridge

Master transaction management, concurrency locks, and enterprise database safeguards in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_update)**.
"""

        elif slug == "sql-delete":
            return """
## 1. Academic Definition & Objectives

The `DELETE` statement is the DML command used to remove existing rows (tuples) from a table based on conditions specified in an optional `WHERE` clause.

Key Competencies:
* Removing specific rows matching a predicate.
* Removing all rows vs `TRUNCATE TABLE`.
* Referential integrity and `CASCADE DELETE` actions.
* Soft deletion vs Hard physical deletion patterns.

---

## 2. Core Concepts & Implementation Blueprint

```sql
-- ==============================================================================
-- 1. TARGETED ROW DELETION
-- ==============================================================================

-- Delete a specific record by primary key
DELETE FROM students 
WHERE student_id = 999;

-- Delete records matching conditional criteria
DELETE FROM students
WHERE status = 'unverified' AND created_at < '2025-01-01';

-- ==============================================================================
-- 2. DELETING ALL ROWS (DML)
-- ==============================================================================

-- Wipes all rows while logging each deletion in transaction log
DELETE FROM temp_logs;
```

---

## 3. The Production Reality ("What Textbooks Skip")

* **The Soft Delete Pattern**: In enterprise applications (financial services, SaaS platforms, healthcare), data is **almost never physically deleted** with `DELETE FROM`. Instead, companies use **Soft Deletion**:
  ```sql
  -- Add a deleted_at timestamp column
  ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;

  -- "Delete" a user by marking the timestamp
  UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE user_id = 42;

  -- Active query filter
  SELECT * FROM users WHERE deleted_at IS NULL;
  ```
  Soft deletion preserves audit trails, allows 1-click user recovery, and prevents foreign key cascading deletions from corrupting historical invoices.
* **Table Bloat in MVCC Databases**: In PostgreSQL, running `DELETE FROM large_table` does not free disk space back to the operating system! It marks dead tuples in data blocks that must later be cleaned up by the `VACUUM` process.

> [!WARNING]
> **Production Gotcha**: If a parent table has `ON DELETE CASCADE` configured on its foreign keys, deleting a single record from the parent table can silently wipe thousands of child records across connected tables. Always check table constraint definitions before executing deletions.

---

## 4. Exam & Technical Interview Gotchas

1. **`DELETE` vs `TRUNCATE` (High-Frequency Exam Question)**:
   - `DELETE` is a DML statement that can filter rows with `WHERE`, activates `DELETE` triggers, and logs every row removal.
   - `TRUNCATE` is a DDL statement that deallocates storage pages, does not accept a `WHERE` clause, does not fire triggers, and resets auto-increment sequences.
2. **Can you rollback a `DELETE`?**: Yes! A `DELETE` statement executed inside an active transaction (`START TRANSACTION; DELETE FROM ...; ROLLBACK;`) can be completely undone.
3. **Foreign Key Restraints**: If child rows reference a parent row with `ON DELETE RESTRICT` (the default), deleting the parent row will fail with a foreign key violation error.

---

## 5. Mythos Mentorship Bridge

Learn database disaster recovery, audit log architecture, and high-concurrency data engineering in the **[MYTHOS Live Weekend Cohort](/register?source=library_sql_delete)**.
"""

    return None



def _generate_topic_outline_document(subject: str, slug: str, topic_meta: Dict[str, Any]) -> ParsedDocument:
    """
    Synthesizes a structured topic syllabus guide when a custom .md file has not yet been authored.
    Uses specialized rich code blueprints for foundational topics or falls back to the 5-part blueprint.
    """
    subject_info = SUBJECTS.get(subject, {})
    title = topic_meta.get("title", slug.replace("-", " ").title())
    category = topic_meta.get("category", "Core Curriculum")
    vertical = topic_meta.get("vertical", "notes")
    reading_time = topic_meta.get("reading_time", "8 min read")

    # Check for specialized educational blueprint
    specialized_body = _get_specialized_topic_content(subject, slug, title)
    if specialized_body:
        body = specialized_body
    else:
        body = f"""
## 1. Academic Definition & Objectives

This module explores **{title}** within the **{subject_info.get('title', subject.upper())}** engineering curriculum.

In computer science examinations and senior technical interviews, mastering this topic requires understanding:
* The formal architectural definition and memory/resource implications.
* Standard syntax patterns and edge cases.
* Key algorithmic trade-offs (Time vs. Space complexity).

> [!NOTE]
> **Curriculum Status**: This topic is an active part of the MYTHOS {subject_info.get('short_title', subject.upper())} curriculum. Full deep-dive lab files and code demonstrations are continuously reviewed by our academic council.

---

## 2. Core Concepts & Implementation Blueprint

```text
{subject.upper()} ARCHITECTURE PIPELINE:
[ High-Level Code / Query ] ──► [ Lexer & Parser ] ──► [ Execution Engine ] ──► [ Memory & System ]
```

### Essential Competencies
1. **Fundamental Operations**: Syntax, declaration, and state lifecycle.
2. **Resource Management**: How the runtime allocates memory, handles scope, and cleans up references.
3. **Common Patterns**: Idiomatic industry practices vs. deprecated legacy methods.

---

## 3. The Production Reality ("What Textbooks Skip")

Most college textbooks and introductory tutorials focus only on basic syntax in isolation. In production systems:

* **Concurrency & Load**: How this component behaves under concurrent read/write pressure.
* **Failure Modes**: Memory leaks, unindexed table scans, blocking I/O, or connection starvation.
* **Monitoring & Observability**: How senior engineers profile, log, and diagnose bottlenecks in production.

> [!WARNING]
> **Production Gotcha**: Never assume default configuration parameters in production. Default pool sizes, timeout limits, and memory limits are engineered for local toys, not enterprise scale.

---

## 4. Exam & Technical Interview Gotchas

When examiners or technical interviewers test candidates on **{title}**, they focus on these trap areas:

1. **Edge Case Handling**: How the system evaluates boundary conditions (null values, empty collections, zero division).
2. **Complexity Bounds**: What is the worst-case vs. average-case runtime complexity?
3. **Failure Recovery**: What happens when an unhandled exception or crash occurs during execution?

---

## 5. Mythos Mentorship Bridge

Reading theory helps you pass written exams; executing controlled live builds with senior mentors prepares you for high-paying engineering roles.

Ready to build production-grade systems live? **[Apply for our selective Weekend Mentorship Cohort](/register?source=library_{subject}_{slug})**.
"""

    preprocessed_body = _preprocess_github_alerts(body)
    md = _build_markdown_parser()
    html_content = md.convert(preprocessed_body)
    toc_tokens = getattr(md, "toc_tokens", [])
    toc_html = getattr(md, "toc", "")

    doc_meta = DocumentMetadata(
        title=title,
        slug=slug,
        subject=subject,
        vertical=vertical,
        category=category,
        order=int(topic_meta.get("order", 999)),
        tier="free",
        price_inr=0,
        reading_time=reading_time,
        description=f"Master {title}: Exam definitions, implementation architecture, production reality, and interview gotchas.",
        tags=[subject_info.get("short_title", subject), category, "Study Guide"],
        last_updated="Active Curriculum",
        file_path=None,
        mtime=0.0,
    )

    return ParsedDocument(
        metadata=doc_meta,
        html_content=html_content,
        toc_tokens=toc_tokens,
        toc_html=toc_html,
        raw_content=body,
    )


def get_document(subject: str, slug: str) -> Optional[ParsedDocument]:
    """
    Retrieves a parsed document by subject and slug.
    First checks for on-disk authored Markdown file.
    If not found on disk, synthesizes a structured topic guide from the catalog.
    """
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        return None

    # 1. Search for custom on-disk .md file
    subject_dir = CONTENT_DIR / subject_lower
    target_file = None
    if subject_dir.exists():
        for file_path in subject_dir.glob("*.md"):
            if file_path.stem == slug:
                target_file = file_path
                break
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                    if post.metadata.get("slug") == slug:
                        target_file = file_path
                        break
            except Exception:
                continue

    if target_file and target_file.is_file():
        mtime = target_file.stat().st_mtime
        cache_key = (subject_lower, slug)
        if cache_key in _DOCUMENT_CACHE:
            cached_mtime, cached_doc = _DOCUMENT_CACHE[cache_key]
            if cached_mtime == mtime:
                return cached_doc
        parsed = parse_markdown_file(target_file)
        _DOCUMENT_CACHE[cache_key] = (mtime, parsed)
        return parsed

    # 2. Check catalog topics if no on-disk file exists
    subject_info = SUBJECTS[subject_lower]
    topics = subject_info.get("topics", [])
    for t in topics:
        if t.get("slug") == slug:
            return _generate_topic_outline_document(subject_lower, slug, t)

    return None


def list_documents_for_subject(
    subject: str, vertical: Optional[str] = None
) -> List[DocumentMetadata]:
    """
    Lists all documents for a given subject. Combines:
    1. Authored markdown files from disk (`app/content/{subject}/*.md`).
    2. Curated topics defined in SUBJECTS[subject]["topics"].
    """
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        return []

    docs: List[DocumentMetadata] = []
    seen_slugs = set()

    # 1. First add custom on-disk authored files
    subject_dir = CONTENT_DIR / subject_lower
    if subject_dir.exists():
        for file_path in subject_dir.glob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                meta = post.metadata or {}
                slug = meta.get("slug") or file_path.stem
                doc_vertical = meta.get("vertical", "notes")
                if vertical and doc_vertical != vertical:
                    continue

                order = int(meta.get("order", 999))
                title = meta.get("title") or slug.replace("-", " ").title()
                category = meta.get("category", "General")
                tier = meta.get("tier", "free")
                price_inr = int(meta.get("price_inr", 0))
                tags = meta.get("tags") or []
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split(",") if t.strip()]

                words = len(post.content.split())
                reading_time = meta.get("reading_time") or _calculate_reading_time(words)
                description = meta.get("description", "")

                doc_meta = DocumentMetadata(
                    title=title,
                    slug=slug,
                    subject=subject_lower,
                    vertical=doc_vertical,
                    category=category,
                    order=order,
                    tier=tier,
                    price_inr=price_inr,
                    reading_time=reading_time,
                    description=description,
                    tags=tags,
                    last_updated=str(meta.get("last_updated", "")),
                    file_path=str(file_path),
                    mtime=file_path.stat().st_mtime,
                )
                docs.append(doc_meta)
                seen_slugs.add(slug)
            except Exception:
                continue

    # 2. Add catalog topics that do not yet have a custom on-disk file
    subject_info = SUBJECTS[subject_lower]
    for idx, t in enumerate(subject_info.get("topics", [])):
        t_slug = t.get("slug")
        if t_slug in seen_slugs:
            continue
        t_vertical = t.get("vertical", "notes")
        if vertical and t_vertical != vertical:
            continue

        doc_meta = DocumentMetadata(
            title=t.get("title", t_slug.replace("-", " ").title()),
            slug=t_slug,
            subject=subject_lower,
            vertical=t_vertical,
            category=t.get("category", "Core Curriculum"),
            order=idx + 1,
            tier="free",
            price_inr=0,
            reading_time=t.get("reading_time", "8 min read"),
            description=f"Structured topic study guide for {t.get('title')}.",
            tags=[subject_info.get("short_title", subject_lower), t.get("category", "Curriculum")],
            last_updated="Curated",
            file_path=None,
            mtime=0.0,
        )
        docs.append(doc_meta)
        seen_slugs.add(t_slug)

    # Sort by curriculum sequence order, then by title
    docs.sort(key=lambda d: (d.order, d.title))
    return docs


def get_subject_grouped_by_category(
    subject: str, vertical: Optional[str] = None
) -> Dict[str, List[DocumentMetadata]]:
    """Groups documents by their category preserving chronological curriculum order."""
    docs = list_documents_for_subject(subject, vertical)
    grouped: Dict[str, List[DocumentMetadata]] = {}
    for doc in docs:
        grouped.setdefault(doc.category, []).append(doc)
    return grouped


def get_adjacent_topics_from_list(
    docs: List[DocumentMetadata], current_slug: str
) -> tuple[Optional[DocumentMetadata], Optional[DocumentMetadata]]:
    """Finds previous and next topics within an explicit list of documents."""
    if not docs:
        return None, None

    for idx, doc in enumerate(docs):
        if doc.slug == current_slug:
            prev_doc = docs[idx - 1] if idx > 0 else None
            next_doc = docs[idx + 1] if idx < len(docs) - 1 else None
            return prev_doc, next_doc

    return None, None


def get_adjacent_topics(
    subject: str, current_slug: str, vertical: Optional[str] = None
) -> tuple[Optional[DocumentMetadata], Optional[DocumentMetadata]]:
    """
    Finds the adjacent previous and next topics in curriculum order.
    Returns (prev_topic, next_topic).
    """
    docs = list_documents_for_subject(subject, vertical)
    return get_adjacent_topics_from_list(docs, current_slug)


def get_subject_videos(subject: str) -> List[Dict[str, Any]]:
    """
    Returns structured masterclass video lecture modules for the Video Lectures panel.
    Zero upfront pricing: transparent duration and curriculum takeaway breakdown.
    """
    subject_lower = subject.lower().strip()
    info = SUBJECTS.get(subject_lower, {})
    title = info.get("short_title", subject.title())

    videos_db: Dict[str, List[Dict[str, Any]]] = {
        "python": [
            {
                "title": "CPython Execution Engine & Bytecode Disassembly",
                "duration": "54 min",
                "level": "Intermediate",
                "badge": "Core Architecture",
                "description": "Step-by-step trace of how the CPython compiler turns source code into AST, bytecode opcodes, and frame execution in the evaluation loop.",
                "takeaways": [
                    "Visualizing stack frames and local namespace",
                    "Using the 'dis' module to profile opcode performance",
                    "Differences between Python 3.10 and 3.12 specializing adaptive interpreter",
                ],
            },
            {
                "title": "Object-Oriented Architecture & Dunder Protocol",
                "duration": "48 min",
                "level": "Foundational to Advanced",
                "badge": "OOP Masterclass",
                "description": "Deep dive into building idiomatic, robust classes with __repr__, __eq__, __hash__, and slot optimizations.",
                "takeaways": [
                    "Class namespace vs instance __dict__",
                    "Designing immutability with dataclasses(frozen=True)",
                    "__slots__ memory benchmarks for 1M+ objects",
                ],
            },
            {
                "title": "High-Throughput Concurrency: Asyncio vs ThreadPool vs Multiprocessing",
                "duration": "62 min",
                "level": "Production Systems",
                "badge": "Systems Concurrency",
                "description": "Hands-on architectural walkthrough comparing event loops, OS threads under GIL constraints, and shared-memory processes for CPU vs I/O bound pipelines.",
                "takeaways": [
                    "Architecting non-blocking HTTP and DB collectors with aiohttp & asyncpg",
                    "How the GIL release mechanism operates during syscalls",
                    "Avoiding blocking event-loop pitfalls in production",
                ],
            },
            {
                "title": "Production Python Code Review & Antipattern Refactoring",
                "duration": "45 min",
                "level": "Industry Best Practices",
                "badge": "Code Review Lab",
                "description": "Live refactoring of messy college scripts into modular, type-checked, tested, and linted packages ready for CI/CD.",
                "takeaways": [
                    "Static analysis with Ruff, Black, and Mypy",
                    "Packaging with pyproject.toml & Poetry",
                    "Dependency injection and testable function design",
                ],
            },
        ],
        "sql": [
            {
                "title": "Query Execution Engine: Reading EXPLAIN ANALYZE Like a DBA",
                "duration": "58 min",
                "level": "Intermediate to Advanced",
                "badge": "DB Internals",
                "description": "Visualizing query optimizer execution trees, sequential scans, index scans, bitmap heap scans, and sort-merge joins.",
                "takeaways": [
                    "Identifying catastrophic Cartesian products and spilled sorts",
                    "Analyzing actual time vs estimated cost metrics",
                    "How PostgreSQL autovacuum statistics influence query plans",
                ],
            },
            {
                "title": "Window Functions & Analytical Reporting Masterclass",
                "duration": "46 min",
                "level": "Analytical SQL",
                "badge": "Core SQL",
                "description": "Comprehensive tutorial on running totals, moving averages, MoM revenue metrics, and cohort retention using window frames.",
                "takeaways": [
                    "ROWS BETWEEN vs RANGE BETWEEN semantics",
                    "Optimizing PARTITION BY performance with compound indexes",
                    "Writing clean CTE pipelines for BI dashboards",
                ],
            },
            {
                "title": "B-Tree Index Internals, Bloat & Defragmentation",
                "duration": "50 min",
                "level": "Database Systems",
                "badge": "Storage Architecture",
                "description": "Understanding leaf nodes, root pages, high watermarks, and fill-factor tuning for write-heavy tables.",
                "takeaways": [
                    "Why unindexed foreign keys cause table-level locks",
                    "Covering indexes (INCLUDE clause) to eliminate heap lookups",
                    "Monitoring index bloat and running concurrent rebuilds",
                ],
            },
        ],
    }

    if subject_lower in videos_db:
        return videos_db[subject_lower]

    return [
        {
            "title": f"{title} Core Architecture & Systems Walkthrough",
            "duration": "50 min",
            "level": "Foundational",
            "badge": "Core Architecture",
            "description": f"Comprehensive architectural overview of {title}, execution mechanics, memory lifecycle, and production design patterns.",
            "takeaways": [
                f"Core mental models for mastering {title}",
                "Textbook syntax vs enterprise production standards",
                "Common rookie bugs and diagnostic procedures",
            ],
        },
        {
            "title": f"Production Performance & Optimization in {title}",
            "duration": "45 min",
            "level": "Advanced",
            "badge": "Performance Lab",
            "description": f"Profiling, benchmarking, and identifying performance bottlenecks when scaling {title} under heavy workloads.",
            "takeaways": [
                "Profiling CPU and memory usage under load",
                "Concurrency, resource locking, and I/O optimization",
                "Monitoring metrics in production environments",
            ],
        },
        {
            "title": f"{title} Technical Interview & Viva Live Problem Solving",
            "duration": "40 min",
            "level": "Interview Prep",
            "badge": "Viva & Interview",
            "description": f"Live walkthrough of high-frequency interview traps, architectural whiteboard scenarios, and tricky viva questions in {title}.",
            "takeaways": [
                "Deconstructing senior interview questions",
                "Edge cases, complexity trade-offs, and failure recovery",
                "Live demonstration of optimal answers",
            ],
        },
    ]


def get_subject_summary(subject: str) -> Optional[Dict[str, Any]]:
    """Returns subject details and vertical resource counts."""
    subject_lower = subject.lower().strip()
    info = SUBJECTS.get(subject_lower)
    if not info:
        return None

    docs = list_documents_for_subject(subject_lower)
    vertical_counts: Dict[str, int] = {v: 0 for v in VERTICALS}
    for doc in docs:
        if doc.vertical in vertical_counts:
            vertical_counts[doc.vertical] += 1

    return {
        **info,
        "total_resources": len(docs),
        "counts": vertical_counts,
        "documents": docs,
    }


def get_all_subjects_summary() -> List[Dict[str, Any]]:
    """Returns overview list of all subjects with their resource counts."""
    summaries = []
    for slug in SUBJECTS:
        summary = get_subject_summary(slug)
        if summary:
            summaries.append(summary)
    return summaries
