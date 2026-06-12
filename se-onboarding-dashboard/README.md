# SE Onboarding Dashboard

Static onboarding workspace for ramping a new Rev.io PSA Solutions Engineer.

Files:

- `index.html` - interactive onboarding dashboard and curriculum navigator
- `resources/revio-psa-se-onboarding-plan.md` - detailed written onboarding plan
- `resources/pdfs/` - generated PDF versions of the training plan and resource sections
- `data/notion-tracker-snapshot.json` - static snapshot of the Notion approval tracker
- `scripts/sync_notion_tracker.py` - local/server-side Notion snapshot refresh script
- `scripts/apply_status_updates.py` - server-side Notion status update script for exported dashboard changes
- `scripts/build_resource_pdfs.js` - PDF resource builder

Open `index.html` directly in a browser. No build step is required.

## Call Reviews

Use pasted transcript text or upload a `.txt`, `.md`, `.vtt`, or `.srt` transcript file for first-pass scoring. Add a transcript or recording URL only as an evidence link; the static dashboard does not upload, store, or transcribe recordings. Choose whether the transcript grades the full demo flow, the complete scorecard, or one selected demo/deep-dive segment. Grade the transcript to populate initial rubric scores and initial notes, then enter Tony's final score, notes, and approval flag manually. Use `Sync to Notion` to export one server-side sync payload containing milestone status changes and the current review scorecard.

Refresh the linked PDF resources from the markdown source with:

```bash
node se-onboarding-dashboard/scripts/build_resource_pdfs.js
```

## Notion Integration

The official onboarding progress tracker lives under the Notion `Solutions Engineer` page:

- Tracker database: https://app.notion.com/p/37ca59b7e7b2815c86d1f8a033b623d5
- Core demo resource: https://app.notion.com/p/SE-Onboarding-Core-Demo-Path-37ca59b7e7b28167a471f52fed26965f
- Product depth resource: https://app.notion.com/p/SE-Onboarding-Product-Depth-Topics-37ca59b7e7b2816791e2c624f571c682
- Buyer scenarios resource: https://app.notion.com/p/SE-Onboarding-Buyer-Scenarios-37ca59b7e7b281c0b63fe7fef0b11f9d
- Certification prep resource: https://app.notion.com/p/SE-Onboarding-Certification-Prep-37ca59b7e7b2814a8372fad8bac855ff

The dashboard reads the static JSON snapshot when hosted. Refresh it locally with:

```bash
NOTION_TOKEN=... python3 se-onboarding-dashboard/scripts/sync_notion_tracker.py
```

The dashboard can export pending milestone status changes as JSON. Apply those changes to Notion server-side with:

```bash
python3 se-onboarding-dashboard/scripts/apply_status_updates.py --dry-run se-onboarding-status-updates.json
NOTION_TOKEN=... python3 se-onboarding-dashboard/scripts/apply_status_updates.py se-onboarding-status-updates.json
```

Run the dry run first to validate page IDs and status values without calling Notion. Do not put the Notion token in the public HTML or client-side JavaScript.
