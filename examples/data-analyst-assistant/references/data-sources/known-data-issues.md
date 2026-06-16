---
description: Known data quality issues and workarounds to apply when querying.
---

# Known Data Issues

## Duplicate Events (pre-2023)

Events recorded before 2023-01-01 may contain duplicates due to a logging bug. Deduplicate using the minimum `id` per `(user_id, event_type, occurred_at)`:

```sql
SELECT MIN(id) AS id, user_id, event_type, occurred_at
FROM events
WHERE occurred_at < '2023-01-01'
GROUP BY user_id, event_type, occurred_at
```

## Missing `paid_at` on Older Invoices

Invoices created before 2022-06-01 may have `paid_at = NULL` even if paid. Cross-reference `amount_cents > 0` as a proxy for payment when `paid_at` is missing for that cohort.

## Plan Field Casing

The `users.plan` column was stored inconsistently before 2023 (`Free`, `PRO`, etc.). Normalize with `LOWER(plan)` in all queries.
