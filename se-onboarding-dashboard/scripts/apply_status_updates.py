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
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
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


def validate_page_id(page_id: str, title: str) -> bool:
    if not page_id:
        print(f"Skipped {title}: missing Notion pageId. Refresh the snapshot with the updated sync script.")
        return False
    if not PAGE_ID_RE.fullmatch(page_id):
        print(f"Skipped {title}: invalid Notion pageId {page_id!r}.")
        return False
    return True


def exported_changes(payload: dict) -> list:
    if "changes" in payload:
        return payload.get("changes", [])
    return payload.get("milestoneStatusChanges", [])


def validate_changes(payload: dict) -> list[dict]:
    changes = exported_changes(payload)
    if not isinstance(changes, list):
        raise SystemExit("Invalid export: changes or milestoneStatusChanges must be a list.")

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

        if not validate_page_id(page_id, title):
            skipped += 1
            continue
        if status not in STATUS_OPTIONS:
            print(f"Skipped {title}: unsupported status {status!r}.")
            skipped += 1
            continue

        valid_changes.append(
            {
                "pageId": page_id,
                "status": status,
                "title": title,
                "employee": str(change.get("employee") or "").strip(),
                "dueDate": str(change.get("dueDate") or "").strip(),
            }
        )

    if skipped:
        print(f"Skipped {skipped} invalid change(s).")
    return valid_changes


def validate_plan(payload: dict) -> list[dict]:
    plan = payload.get("milestonePlan", [])
    if plan in (None, []):
        return []
    if not isinstance(plan, list):
        raise SystemExit("Invalid export: milestonePlan must be a list.")

    valid_items = []
    skipped = 0
    for index, item in enumerate(plan, start=1):
        if not isinstance(item, dict):
            print(f"Skipped plan item #{index}: expected an object.")
            skipped += 1
            continue

        title = str(item.get("title") or item.get("key") or f"plan item #{index}")
        page_id = str(item.get("pageId") or "").strip()
        due_date = str(item.get("dueDate") or "").strip()
        employee = str(item.get("employee") or "").strip()
        status = str(item.get("status") or "").strip()

        if not validate_page_id(page_id, title):
            skipped += 1
            continue
        if due_date and not DATE_RE.fullmatch(due_date):
            print(f"Skipped {title}: invalid dueDate {due_date!r}. Use YYYY-MM-DD.")
            skipped += 1
            continue
        if status and status not in STATUS_OPTIONS:
            print(f"Skipped {title}: unsupported status {status!r}.")
            skipped += 1
            continue

        valid_items.append(
            {
                "pageId": page_id,
                "title": title,
                "employee": employee,
                "dueDate": due_date,
                "status": status,
            }
        )

    if skipped:
        print(f"Skipped {skipped} invalid plan item(s).")
    return valid_items


def merge_updates(changes: list[dict], plan: list[dict]) -> list[dict]:
    updates: dict[str, dict] = {}
    for item in plan:
        updates[item["pageId"]] = {
            "pageId": item["pageId"],
            "title": item["title"],
            "employee": item.get("employee", ""),
            "dueDate": item.get("dueDate", ""),
            "status": item.get("status", ""),
        }

    for change in changes:
        update = updates.setdefault(
            change["pageId"],
            {"pageId": change["pageId"], "title": change["title"]},
        )
        update["title"] = change["title"] or update.get("title", change["pageId"])
        update["status"] = change["status"]
        if change.get("employee"):
            update["employee"] = change["employee"]
        if change.get("dueDate"):
            update["dueDate"] = change["dueDate"]

    return list(updates.values())


def update_body(update: dict) -> dict:
    properties = {}
    status = update.get("status")
    employee = update.get("employee")
    due_date = update.get("dueDate")

    if status:
        properties["Status"] = {"select": {"name": status}}
        properties["Tony Approval"] = {"checkbox": status == "Approved"}
    if employee is not None:
        properties["Employee"] = {"rich_text": [{"text": {"content": employee}}] if employee else []}
    if due_date is not None:
        properties["Due Date"] = {"date": {"start": due_date} if due_date else None}

    return {"properties": properties}


def main() -> None:
    args = parse_args()
    payload = load_payload(pathlib.Path(args.json_file))
    changes = validate_changes(payload)
    plan = validate_plan(payload)
    updates = merge_updates(changes, plan)
    if not updates:
        print("No changes to apply.")
        return

    if args.dry_run:
        for update in updates:
            parts = []
            if update.get("status"):
                parts.append(f"status={update['status']}")
            if update.get("employee") is not None:
                parts.append(f"employee={update.get('employee') or '(blank)'}")
            if update.get("dueDate") is not None:
                parts.append(f"dueDate={update.get('dueDate') or '(blank)'}")
            print(f"Would update {update['title']}: {', '.join(parts)}")
        print(f"Validated {len(updates)} Notion update(s). No Notion changes made.")
        return

    applied = 0
    for update in updates:
        page_id = update["pageId"]
        title = update["title"]

        notion_request(f"/pages/{page_id}", update_body(update))
        applied += 1
        print(f"Updated {title}")

    print(f"Applied {applied} Notion update(s).")


if __name__ == "__main__":
    main()
