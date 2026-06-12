#!/usr/bin/env python3
"""Apply exported SE onboarding status changes to the Notion tracker.

Usage:
  python3 scripts/apply_status_updates.py --dry-run se-onboarding-status-updates.json
  NOTION_TOKEN=... python3 scripts/apply_status_updates.py se-onboarding-status-updates.json

The JSON file is created from the dashboard's Export Status Changes button.
Keep the token server-side; never place it in the public dashboard.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request


NOTION_VERSION = "2022-06-28"
STATUS_OPTIONS = {"Not Started", "In Progress", "Approved"}
PAGE_ID_RE = re.compile(
    r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
    re.IGNORECASE,
)


def notion_request(path: str, body: dict, method: str = "PATCH") -> dict:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        raise SystemExit("Set NOTION_TOKEN before running this script.")

    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(f"https://api.notion.com/v1{path}", data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Notion-Version", NOTION_VERSION)
    request.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8")
        raise SystemExit(f"Notion API error {error.code}: {message}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not reach Notion API: {error.reason}") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply exported SE onboarding status changes to the Notion tracker."
    )
    parser.add_argument("json_file", help="JSON file exported from the dashboard")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print planned updates without calling the Notion API",
    )
    return parser.parse_args()


def load_payload(path: pathlib.Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SystemExit(f"JSON file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {path}: {error}") from error

    if not isinstance(payload, dict):
        raise SystemExit("Invalid export: top-level JSON value must be an object.")
    return payload


def validate_changes(payload: dict) -> list[dict]:
    changes = payload.get("changes", [])
    if not isinstance(changes, list):
        raise SystemExit("Invalid export: changes must be a list.")

    valid_changes = []
    skipped = 0
    for index, change in enumerate(changes, start=1):
        if not isinstance(change, dict):
            print(f"Skipped change #{index}: expected an object.")
            skipped += 1
            continue

        page_id = str(change.get("pageId") or "").strip()
        status = str(change.get("to") or "").strip()
        title = str(change.get("title") or page_id or f"change #{index}")

        if not page_id:
            print(f"Skipped {title}: missing Notion pageId. Refresh the snapshot with the updated sync script.")
            skipped += 1
            continue
        if not PAGE_ID_RE.fullmatch(page_id):
            print(f"Skipped {title}: invalid Notion pageId {page_id!r}.")
            skipped += 1
            continue
        if status not in STATUS_OPTIONS:
            print(f"Skipped {title}: unsupported status {status!r}.")
            skipped += 1
            continue

        valid_changes.append({"pageId": page_id, "to": status, "title": title})

    if skipped:
        print(f"Skipped {skipped} invalid change(s).")
    return valid_changes


def update_body(status: str) -> dict:
    return {
        "properties": {
            "Status": {"select": {"name": status}},
            "Tony Approval": {"checkbox": status == "Approved"},
        }
    }


def main() -> None:
    args = parse_args()
    payload = load_payload(pathlib.Path(args.json_file))
    changes = validate_changes(payload)
    if not changes:
        print("No changes to apply.")
        return

    if args.dry_run:
        for change in changes:
            print(f"Would update {change['title']}: {change['to']}")
        print(f"Validated {len(changes)} status update(s). No Notion changes made.")
        return

    applied = 0
    for change in changes:
        page_id = change["pageId"]
        status = change["to"]
        title = change["title"]

        notion_request(f"/pages/{page_id}", update_body(status))
        applied += 1
        print(f"Updated {title}: {status}")

    print(f"Applied {applied} status update(s).")


if __name__ == "__main__":
    main()
