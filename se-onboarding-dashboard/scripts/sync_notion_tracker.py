#!/usr/bin/env python3
"""Refresh the static SE onboarding tracker snapshot from Notion.

Usage:
  NOTION_TOKEN=... python3 scripts/sync_notion_tracker.py

The token must stay local/server-side. Do not place it in the public dashboard.
"""

from __future__ import annotations

import json
import os
import pathlib
import urllib.error
import urllib.request


NOTION_VERSION = "2022-06-28"
TRACKER_DATABASE_ID = os.environ.get(
    "NOTION_TRACKER_DATABASE_ID",
    "37ca59b7e7b2815c86d1f8a033b623d5",
)
OUTPUT_PATH = pathlib.Path(__file__).resolve().parents[1] / "data" / "notion-tracker-snapshot.json"


def notion_request(path: str, body: dict | None = None, method: str = "POST") -> dict:
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise SystemExit("Set NOTION_TOKEN before running this script.")

    data = None if body is None else json.dumps(body).encode("utf-8")
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


def text_fragments(prop: dict, key: str) -> str:
    return "".join(item.get("plain_text", "") for item in prop.get(key, []))


def title_from(props: dict) -> str:
    for prop in props.values():
        if prop.get("type") == "title":
            return text_fragments(prop, "title")
    return ""


def property_value(props: dict, name: str):
    prop = props.get(name, {})
    prop_type = prop.get("type")

    if prop_type == "select":
        selected = prop.get("select")
        return selected.get("name") if selected else None
    if prop_type == "checkbox":
        return prop.get("checkbox", False)
    if prop_type == "date":
        date = prop.get("date")
        return date.get("start") if date else None
    if prop_type == "rich_text":
        return text_fragments(prop, "rich_text")
    if prop_type == "url":
        return prop.get("url")
    if prop_type == "number":
        return prop.get("number")
    return None


def main() -> None:
    result = notion_request(
        f"/databases/{TRACKER_DATABASE_ID}/query",
        {
            "page_size": 100,
            "sorts": [{"property": "Sort Order", "direction": "ascending"}],
        },
    )

    items = []
    for page in result.get("results", []):
        props = page.get("properties", {})
        items.append(
            {
                "id": page.get("id"),
                "name": title_from(props),
                "phase": property_value(props, "Phase"),
                "status": property_value(props, "Status"),
                "tonyApproval": property_value(props, "Tony Approval"),
                "approvalDate": property_value(props, "Approval Date"),
                "dueDate": property_value(props, "Due Date"),
                "employee": property_value(props, "Employee"),
                "notes": property_value(props, "Notes"),
                "evidenceUrl": property_value(props, "Evidence URL"),
                "url": page.get("url"),
                "sortOrder": property_value(props, "Sort Order"),
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "source": "Notion SE Onboarding Tracker",
                "trackerUrl": f"https://app.notion.com/p/{TRACKER_DATABASE_ID}",
                "items": items,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH} with {len(items)} items.")


if __name__ == "__main__":
    main()
