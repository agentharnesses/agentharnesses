#!/usr/bin/env python3
"""Run a read-only SQL query and print results as JSON."""
import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: run_query.py <sql>", file=sys.stderr)
        sys.exit(1)

    sql = sys.argv[1]

    # Reject any non-SELECT statements as a safety check.
    if not sql.strip().upper().startswith("SELECT"):
        print("Error: only SELECT statements are permitted.", file=sys.stderr)
        sys.exit(1)

    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        print(json.dumps(rows, default=str, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
