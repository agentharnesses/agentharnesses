---
description: Official definitions for key business metrics used across reports.
---

# KPI Definitions

## Monthly Active Users (MAU)

Users with at least one event in the calendar month. Counted as distinct `user_id` values.

## Monthly Recurring Revenue (MRR)

Sum of `amount_cents` from invoices with a non-null `paid_at` within the month, divided by 100. Excludes one-time charges tagged `event_type = 'one-time'`.

## Churn Rate

```
churn_rate = users who did not renew / users active at start of period
```

Measured monthly. A user is considered churned if they have no invoice in the current month but had one the prior month.

## Activation Rate

Percentage of new signups (`users.created_at` in period) who triggered an `invite` or `export` event within 7 days of signup.
