---
description: Common SQL patterns and approved query idioms for this database.
---

# Query Patterns

## Date Ranges

Always filter on `occurred_at` or `created_at` using half-open intervals:

```sql
WHERE occurred_at >= '2024-01-01' AND occurred_at < '2024-02-01'
```

## Counting Active Users

An active user is one who has at least one event in the period:

```sql
SELECT COUNT(DISTINCT user_id) AS active_users
FROM events
WHERE occurred_at >= '2024-01-01' AND occurred_at < '2024-02-01'
```

## Revenue

Sum `amount_cents` from paid invoices and divide by 100 for dollars:

```sql
SELECT SUM(amount_cents) / 100.0 AS revenue_usd
FROM invoices
WHERE paid_at IS NOT NULL
```

## Joining Users to Events

```sql
SELECT u.email, e.event_type, e.occurred_at
FROM events e
JOIN users u ON u.id = e.user_id
```
