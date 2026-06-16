#!/usr/bin/env python3
"""Sync a full SE onboarding dashboard payload into Notion.

Usage:
  python3 scripts/sync_notion_payload.py --dry-run payload.json
  python3 scripts/sync_notion_payload.py --json-summary -

The token must stay server-side. The script accepts either NOTION_TOKEN or
NOTION_API_KEY and is intended to be called by the OpenClaw sync route.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any


NOTION_VERSION = "2022-06-28"
STATUS_OPTIONS = {"Not Started", "In Progress", "Approved"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PAGE_ID_RE = re.compile(
    r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
    re.IGNORECASE,
)

TRACKER_DATABASE_ID = os.environ.get(
    "NOTION_TRACKER_DATABASE_ID",
    "37ca59b7-e7b2-815c-86d1-f8a033b623d5",
)
ACCESS_DATABASE_ID = os.environ.get(
    "NOTION_ACCESS_DATABASE_ID",
    "381a59b7-e7b2-819f-94c1-e90421d414a8",
)
CALL_REVIEW_DATABASE_ID = os.environ.get(
    "NOTION_CALL_REVIEW_DATABASE_ID",
    "381a59b7-e7b2-8158-bdfa-fe3ceb27f0c6",
)
SCORECARD_DATABASE_ID = os.environ.get(
    "NOTION_SCORECARD_DATABASE_ID",
    "381a59b7-e7b2-8100-8650-f5cfa1f3d9bc",
)
RUBRIC_DATABASE_ID = os.environ.get(
    "NOTION_RUBRIC_DATABASE_ID",
    "381a59b7-e7b2-81f1-94c9-f3d98bafe6ca",
)


class SyncError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync SE onboarding dashboard payload into Notion.")
    parser.add_argument("json_file", help="Payload JSON file, or '-' for stdin")
    parser.add_argument("--dry-run", action="store_true", help="Validate and plan without writing")
    parser.add_argument("--json-summary", action="store_true", help="Print machine-readable summary JSON")
    return parser.parse_args()


def read_payload(path: str) -> dict[str, Any]:
    try:
        raw = sys.stdin.read() if path == "-" else pathlib.Path(path).read_text(encoding="utf-8")
        payload = json.loads(raw)
    except FileNotFoundError as error:
        raise SyncError(f"JSON file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise SyncError(f"Invalid JSON: {error}") from error

    if not isinstance(payload, dict):
        raise SyncError("Invalid payload: top-level JSON value must be an object.")
    if payload.get("source") != "SE Onboarding Dashboard":
        raise SyncError("Invalid payload: source must be 'SE Onboarding Dashboard'.")
    return payload


def notion_token() -> str:
    token = (os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_API_KEY") or "").strip()
    if not token:
        raise SyncError("Notion token is not configured on the server.")
    return token


def notion_request(path: str, body: dict[str, Any] | None = None, method: str = "POST") -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(f"https://api.notion.com/v1{path}", data=data, method=method)
    request.add_header("Authorization", f"Bearer {notion_token()}")
    request.add_header("Notion-Version", NOTION_VERSION)
    request.add_header("Content-Type", "application/json")

    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < 3:
                retry_after = error.headers.get("Retry-After")
                time.sleep(float(retry_after or "1"))
                continue
            message = error.read().decode("utf-8")
            raise SyncError(f"Notion API error {error.code}: {message}") from error
        except urllib.error.URLError as error:
            raise SyncError(f"Could not reach Notion API: {error.reason}") from error

    raise SyncError("Notion API rate limit did not clear.")


def notion_text(value: str) -> dict[str, Any]:
    return {"rich_text": [{"text": {"content": value}}] if value else []}


def notion_title(value: str) -> dict[str, Any]:
    return {"title": [{"text": {"content": value}}]}


def notion_date(value: str | None) -> dict[str, Any]:
    return {"date": {"start": value} if value else None}


def notion_select(value: str | None) -> dict[str, Any]:
    return {"select": {"name": value} if value else None}


def iso_minute(value: str | None) -> str | None:
    if not value:
        return None
    trimmed = str(value).strip()
    if not trimmed:
        return None
    if trimmed.endswith("Z"):
        trimmed = trimmed[:-1] + "+00:00"
    return trimmed


def iso_date(value: str | None) -> str:
    normalized = iso_minute(value) or ""
    return normalized[:10] if len(normalized) >= 10 else ""


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SyncError(f"Invalid payload: {label} must be an object.")
    return value


def list_value(value: Any, label: str) -> list[Any]:
    if value in (None, []):
        return []
    if not isinstance(value, list):
        raise SyncError(f"Invalid payload: {label} must be a list.")
    return value


def validate_page_id(page_id: str, title: str) -> str:
    page_id = str(page_id or "").strip()
    if not PAGE_ID_RE.fullmatch(page_id):
        raise SyncError(f"Invalid Notion pageId for {title}: {page_id!r}.")
    return page_id


def validate_date(value: str, label: str) -> str:
    value = str(value or "").strip()
    if value and not DATE_RE.fullmatch(value):
        raise SyncError(f"Invalid {label}: {value!r}. Use YYYY-MM-DD.")
    return value


def title_equals_filter(title: str) -> dict[str, Any]:
    return {"filter": {"property": "Name", "title": {"equals": title}}, "page_size": 1}


def find_page_by_title(database_id: str, title: str) -> str | None:
    result = notion_request(f"/databases/{database_id}/query", title_equals_filter(title))
    results = result.get("results", [])
    if not results:
        return None
    return results[0].get("id")


def patch_page(page_id: str, properties: dict[str, Any], dry_run: bool, counters: dict[str, int]) -> None:
    if dry_run:
        counters["planned_updates"] += 1
        return
    notion_request(f"/pages/{page_id}", {"properties": properties}, method="PATCH")
    counters["updated"] += 1


def create_page(database_id: str, properties: dict[str, Any], dry_run: bool, counters: dict[str, int]) -> None:
    if dry_run:
        counters["planned_creates"] += 1
        return
    notion_request("/pages", {"parent": {"database_id": database_id}, "properties": properties})
    counters["created"] += 1


def upsert_by_title(
    database_id: str,
    title: str,
    properties: dict[str, Any],
    dry_run: bool,
    counters: dict[str, int],
) -> None:
    page_id = find_page_by_title(database_id, title)
    if page_id:
        patch_page(page_id, properties, dry_run, counters)
    else:
        create_page(database_id, properties, dry_run, counters)


def profile(payload: dict[str, Any]) -> dict[str, str]:
    raw_profile = require_object(payload.get("onboardingProfile") or {}, "onboardingProfile")
    return {
        "rep": str(raw_profile.get("rep") or "").strip(),
        "startDate": validate_date(str(raw_profile.get("startDate") or "").strip(), "startDate"),
    }


def sync_milestones(payload: dict[str, Any], employee: str, dry_run: bool, counters: dict[str, int]) -> None:
    updates: dict[str, dict[str, Any]] = {}
    for item in list_value(payload.get("milestonePlan"), "milestonePlan"):
        if not isinstance(item, dict):
            raise SyncError("Invalid payload: milestonePlan entries must be objects.")
        title = str(item.get("title") or item.get("key") or "Milestone").strip()
        page_id = validate_page_id(str(item.get("pageId") or ""), title)
        status = str(item.get("status") or "").strip()
        due_date = validate_date(str(item.get("dueDate") or "").strip(), f"dueDate for {title}")
        if status and status not in STATUS_OPTIONS:
            raise SyncError(f"Unsupported status for {title}: {status!r}.")
        updates[page_id] = {
            "title": title,
            "employee": str(item.get("employee") or employee).strip(),
            "dueDate": due_date,
            "status": status,
        }

    for change in list_value(payload.get("milestoneStatusChanges"), "milestoneStatusChanges"):
        if not isinstance(change, dict):
            raise SyncError("Invalid payload: milestoneStatusChanges entries must be objects.")
        title = str(change.get("title") or "Milestone").strip()
        page_id = validate_page_id(str(change.get("pageId") or ""), title)
        status = str(change.get("to") or "").strip()
        if status not in STATUS_OPTIONS:
            raise SyncError(f"Unsupported status for {title}: {status!r}.")
        update = updates.setdefault(page_id, {"title": title})
        update["status"] = status
        if change.get("employee"):
            update["employee"] = str(change.get("employee") or "").strip()
        if change.get("dueDate"):
            update["dueDate"] = validate_date(str(change.get("dueDate") or ""), f"dueDate for {title}")

    for page_id, update in updates.items():
        properties: dict[str, Any] = {}
        if update.get("status"):
            properties["Status"] = notion_select(update["status"])
            properties["Tony Approval"] = {"checkbox": update["status"] == "Approved"}
        if "employee" in update:
            properties["Employee"] = notion_text(update.get("employee") or "")
        if "dueDate" in update:
            properties["Due Date"] = notion_date(update.get("dueDate") or None)
        if properties:
            patch_page(page_id, properties, dry_run, counters)


def sync_access(payload: dict[str, Any], employee: str, start_date: str, generated_at: str | None, dry_run: bool, counters: dict[str, int]) -> None:
    for item in list_value(payload.get("accessVerification"), "accessVerification"):
        if not isinstance(item, dict):
            raise SyncError("Invalid payload: accessVerification entries must be objects.")
        group = str(item.get("group") or "").strip()
        access_item = str(item.get("item") or "").strip()
        if not employee or not group or not access_item:
            raise SyncError("Invalid access verification row: employee, group, and item are required.")
        title = f"{employee} - {access_item}"
        properties = {
            "Name": notion_title(title),
            "Employee": notion_text(employee),
            "Group": notion_select(group),
            "Item": notion_text(access_item),
            "Verified": {"checkbox": bool(item.get("verified"))},
            "Start Date": notion_date(start_date or None),
            "Generated At": notion_date(generated_at),
            "Source": notion_text(str(payload.get("source") or "")),
        }
        upsert_by_title(ACCESS_DATABASE_ID, title, properties, dry_run, counters)


def sync_call_review(payload: dict[str, Any], employee: str, generated_at: str | None, dry_run: bool, counters: dict[str, int]) -> None:
    review = payload.get("callReview")
    if not review:
        return
    review = require_object(review, "callReview")
    reviewed_at = iso_minute(str(review.get("reviewedAt") or "")) or generated_at
    reviewed_date = iso_date(reviewed_at)
    call_type = str(review.get("callType") or "").strip()
    review_scope = str(review.get("reviewScope") or "").strip()
    title = f"{employee} - {call_type or 'Call Review'} - {reviewed_date or 'undated'}"

    properties = {
        "Name": notion_title(title),
        "Employee": notion_text(employee),
        "Generated At": notion_date(generated_at),
        "Reviewed At": notion_date(reviewed_at),
        "Call Type": notion_select(call_type or None),
        "Review Scope": notion_select(review_scope or None),
        "Evidence URL": {"url": str(review.get("evidenceUrl") or "").strip() or None},
        "Reviewer Notes": notion_text(str(review.get("reviewerNotes") or "")),
        "Transcript Characters": {"number": int(review.get("transcriptCharacters") or 0)},
        "Average Score": {"number": float(review.get("averageScore") or 0)},
        "Coaching Focus": {
            "multi_select": [{"name": str(item)} for item in list_value(review.get("coachingFocus"), "callReview.coachingFocus") if str(item)]
        },
    }
    upsert_by_title(CALL_REVIEW_DATABASE_ID, title, properties, dry_run, counters)

    for score in list_value(review.get("scores"), "callReview.scores"):
        if not isinstance(score, dict):
            raise SyncError("Invalid payload: callReview.scores entries must be objects.")
        area = str(score.get("name") or "").strip()
        if not area:
            raise SyncError("Invalid rubric score row: name is required.")
        rubric_title = f"{employee} - {area} - {reviewed_date or 'undated'}"
        rubric_properties = {
            "Name": notion_title(rubric_title),
            "Employee": notion_text(employee),
            "Generated At": notion_date(generated_at),
            "Reviewed At": notion_date(reviewed_at),
            "Call Type": notion_select(call_type or None),
            "Review Scope": notion_select(review_scope or None),
            "Rubric Area": notion_text(area),
            "Score": {"number": float(score.get("score") or 0)},
            "Hits": notion_text(", ".join(str(item) for item in list_value(score.get("hits"), "score.hits"))),
            "Missing Signals": notion_text(", ".join(str(item) for item in list_value(score.get("missingSignals"), "score.missingSignals"))),
        }
        upsert_by_title(RUBRIC_DATABASE_ID, rubric_title, rubric_properties, dry_run, counters)

    for segment in list_value(review.get("segmentReviews"), "callReview.segmentReviews"):
        if not isinstance(segment, dict):
            raise SyncError("Invalid payload: callReview.segmentReviews entries must be objects.")
        name = str(segment.get("name") or "").strip()
        step = int(segment.get("step") or 0)
        if not name or step <= 0:
            raise SyncError("Invalid scorecard row: name and positive step are required.")
        scorecard_title = f"{employee} - {step}. {name}"
        final_score = segment.get("finalScore")
        scorecard_properties = {
            "Name": notion_title(scorecard_title),
            "Employee": notion_text(employee),
            "Generated At": notion_date(generated_at),
            "Reviewed At": notion_date(reviewed_at),
            "Review Scope": notion_select(review_scope or None),
            "Segment Key": notion_text(str(segment.get("key") or "")),
            "Type": notion_select(str(segment.get("type") or "").strip() or None),
            "Step": {"number": step},
            "Description": notion_text(str(segment.get("description") or "")),
            "Initial Score": {"number": float(segment.get("initialScore") or 0)},
            "Initial Notes": notion_text(str(segment.get("initialNotes") or "")),
            "Final Score": {"number": None if final_score in (None, "") else float(final_score)},
            "Final Notes": notion_text(str(segment.get("finalNotes") or "")),
            "Approved": {"checkbox": bool(segment.get("approved"))},
        }
        upsert_by_title(SCORECARD_DATABASE_ID, scorecard_title, scorecard_properties, dry_run, counters)


def sync_payload(payload: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    user_profile = profile(payload)
    employee = user_profile["rep"]
    if not employee:
        raise SyncError("Employee/rep is required before syncing to Notion.")

    generated_at = iso_minute(str(payload.get("generatedAt") or ""))
    counters = {
        "planned_updates": 0,
        "planned_creates": 0,
        "updated": 0,
        "created": 0,
    }

    sync_milestones(payload, employee, dry_run, counters)
    sync_access(payload, employee, user_profile["startDate"], generated_at, dry_run, counters)
    sync_call_review(payload, employee, generated_at, dry_run, counters)

    total = counters["updated"] + counters["created"] + counters["planned_updates"] + counters["planned_creates"]
    return {
        "ok": True,
        "dryRun": dry_run,
        "employee": employee,
        "total": total,
        **counters,
    }


def main() -> int:
    args = parse_args()
    try:
        summary = sync_payload(read_payload(args.json_file), args.dry_run)
    except SyncError as error:
        if args.json_summary:
            print(json.dumps({"ok": False, "error": str(error)}))
        else:
            print(str(error), file=sys.stderr)
        return 1

    if args.json_summary:
        print(json.dumps(summary))
    else:
        action = "Validated" if args.dry_run else "Synced"
        print(f"{action} {summary['total']} Notion row/page operation(s) for {summary['employee']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
