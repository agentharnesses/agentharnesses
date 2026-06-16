#!/usr/bin/env python3
"""Read a CSV or Excel file and print contents as JSON."""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: read_spreadsheet.py <filepath>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        import pandas as pd
        if path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        print(json.dumps(df.to_dict(orient="records"), default=str, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
