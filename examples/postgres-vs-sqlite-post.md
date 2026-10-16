# Example: `write a blog post comparing Postgres and SQLite for a small SaaS`

Unedited output. Claude Code 2.1, model `claude-opus-5-5`, run headless in an empty directory with
only this skill installed and no MCP servers:

```bash
claude -p "/deepen write a blog post comparing Postgres and SQLite for a small SaaS" --setting-sources project --strict-mcp-config
```

---

**1. What would a top professional do that you didn't ask for?**
- Make the comparison about the deployment the SaaS actually runs on (one VPS, serverless, multiple app instances). Most of the decision follows from that, not from feature lists.
- Run a benchmark on the writer's own hardware instead of quoting other people's numbers. Concurrent writes are where SQLite's single-writer lock matters.
- Cover running each database day to day: backups and point-in-time restore, migrations, and what it takes to move off SQLite later.

**2. Rawest material to start from**
- The official docs: sqlite.org "Appropriate Uses For SQLite", "Write-Ahead Logging" and "SQLite Is Serverless", plus the PostgreSQL 17 docs on MVCC, connection limits and `pg_dump`/WAL archiving.
- Litestream and LiteFS docs and changelogs, and current managed-Postgres pricing pages (Neon, Supabase, RDS), checked on the date of writing.
- Raw benchmark output (latency per query, p50/p99, errors such as `SQLITE_BUSY`) logged to CSV, not summary charts from other blogs.

**3. Methods and tools**
- `pgbench` for Postgres, and a small script against SQLite in WAL mode with `busy_timeout` set, both running the same SaaS-style mix: mostly reads, some writes, 1–50 concurrent clients.
- `EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE` on two or three typical queries (tenant-scoped list, aggregate report).
- WebSearch/WebFetch to check prices and current versions. Every claim gets an inline link.

**4. Outside checks that can pass or fail**
- Every factual claim links to a primary source, and the link resolves.
- The benchmark script and raw CSV are published, and someone else can rerun them and get numbers within the same order of magnitude.
- Each recommendation (for example "SQLite fits up to N writes/sec on one node") either matches the benchmark data or is cut.

```
Write a blog post comparing Postgres and SQLite for a small SaaS (1 team, <10k users).
Frame the choice by deployment shape: single VPS, multiple app instances, serverless.
Base claims on primary sources only: sqlite.org (Appropriate Uses, WAL, locking),
PostgreSQL 17 docs (MVCC, connections, backup/PITR), Litestream/LiteFS docs, and
managed-Postgres pricing pages checked today; link each claim inline.
Run a small reproducible benchmark on one machine: SQLite (WAL, busy_timeout) vs
Postgres (pgbench or the same script), a read-heavy SaaS query mix at 1/10/50 clients;
record p50/p99 latency, throughput and SQLITE_BUSY/errors to CSV.
Cover operations: backups and restore, migrations, and the cost of moving SQLite->Postgres.
End with a decision rule tied to measured thresholds; drop any claim the data doesn't support.
Include the benchmark script and raw CSV so readers can rerun it.
```

Want me to run this prompt?
