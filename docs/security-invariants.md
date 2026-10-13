# Development security boundary

The current API uses an in-memory development store. It has no production-grade persistence or durable tenant isolation. The earlier invariant table referred to test and implementation files that were not present in the repository; see `SECURITY_HARDENING_REPORT.md`.

The tracked tests in `backend/api/tests/` cover anonymous denial on protected routes, strict registration payloads, stale/forged JWT claims, login, process-local throttling, explicit 501 responses for scaffold writes, and tamper detection for the process-local per-tenant audit chain. These are bounded properties of this development implementation.

All entity, alert, case and report routes require authentication at the router boundary. Mutating case routes require the corresponding role permission; unfinished writes and exports return 501. The published read handlers still return empty scaffold results and do not establish real data-layer tenant isolation. Registration creates a new tenant per account and never accepts role or tenant from the client. There is no public path to provision elevated roles or additional tenant members.

The audit chain contains only server-derived opaque actor/resource IDs, action names and timestamps. It is application-level tamper evidence, not immutable or independent storage. Production use requires a durable data layer with tenant-scoped queries, independent audit persistence, and tests against those real paths.
