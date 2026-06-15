---
description: Definitions and descriptions for all database tables and columns used in the product database.
---

# Data Dictionary

## Table: `users`

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `email` | text | User's email address |
| `created_at` | timestamp | When the account was created |
| `plan` | text | Subscription plan: `free`, `pro`, `enterprise` |

## Table: `events`

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `user_id` | integer | Foreign key to `users.id` |
| `event_type` | text | Name of the event (e.g. `login`, `export`, `invite`) |
| `occurred_at` | timestamp | When the event happened |

## Table: `invoices`

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `user_id` | integer | Foreign key to `users.id` |
| `amount_cents` | integer | Invoice amount in cents |
| `paid_at` | timestamp | When the invoice was paid; null if unpaid |
