# SE Onboarding Dashboard

Static onboarding workspace for ramping a new Rev.io PSA Solutions Engineer.

Files:

- `index.html` - interactive onboarding dashboard and curriculum navigator
- `resources/revio-psa-se-onboarding-plan.md` - detailed written onboarding plan
- `data/notion-tracker-snapshot.json` - static snapshot of the Notion approval tracker
- `scripts/sync_notion_tracker.py` - local/server-side Notion snapshot refresh script

Open `index.html` directly in a browser. No build step is required.

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

Do not put the Notion token in the public HTML or client-side JavaScript.
