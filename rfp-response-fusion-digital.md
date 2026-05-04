# Rev.io PSA — RFP Response: Fusion Digital
**Prepared for:** Alyse / Fusion Digital
**Prepared by:** [Tony / Your Name]
**Date:** May 2026
**Deadline:** May 15, 2026

> **Internal Note (remove before sending):** Items marked 🔴 NEED VERIFICATION require confirmation from the Rev.io product/sales team before this response is sent. Items marked ✅ are confirmed from platform walkthrough and documentation.

---

## 1. Sales Commission Reporting

Thank you for raising this — we want to be transparent rather than oversell.

**Current State:** Rev.io PSA does not currently include a native, dedicated commission reporting module. The platform does include a **Sales Rep field** on every customer record, and **Profit by Technician** reporting is available in the Analytics dashboards. However, a structured commission calculation engine (split commissions, gross-profit-based, invoice-date vs. payment-date logic) is not available as a built-in feature today.

**What exists today that could be leveraged:**
- Sales Rep attribution on customer and opportunity records
- Revenue Analysis and Profit by Technician dashboards
- SQL Lab (direct database queries) within the Analytics module, which could support custom commission extracts for users comfortable with SQL
- Data export (CSV/Excel/PDF) from any list view for offline calculation

**On your specific sub-questions:**
- Commission by sales rep: ✅ Sales Rep attribution exists; formal commission calculation: 🔴 not natively available
- Split commissions: 🔴 Not natively supported
- Gross-profit-based commissions: 🔴 Not natively supported
- Reporting by order/invoice/project: 🔴 Not a dedicated module; partial data available via exports
- Invoice-date vs. payment-date logic: 🔴 Not natively supported in a commission context

🔴 **VERIFY WITH REV.IO:** Confirm roadmap ETA and whether this is committed or subject to movement. This appears to be a known gap and your account team should provide a candid answer on timeline.

---

## 2. Current-State vs. Roadmap Classification

| Capability | Status | Native / Config / Workaround | Notes |
|---|---|---|---|
| Commission reporting | Not supported today | — | See Section 1 above |
| Assemblies / finished goods | Not supported natively | Workaround available | See Section 8 — Packages feature is the nearest equivalent |
| RMA processing | Not supported natively | Workaround available | See Section 9 |
| SPA expiration tracking / renewal management | Not supported natively | Workaround available | Custom Fields + Recurring Schedules + Workflow automation can approximate this |
| Report scheduling | 🔴 Needs verification | — | Analytics dashboards and SQL Lab are available; scheduled delivery not confirmed |
| Warranty workflows | Partially available | Native (manual) | Manufacturer Warranty Exp date field on asset records; automated alerts via Workflow engine possible |
| Change orders | 🔴 Needs verification | — | Quote versioning exists; formal "change order" workflow not confirmed |
| Vendor delivery tracking | Not confirmed in platform | 🔴 Needs verification | Purchase Orders exist; delivery tracking status not confirmed |

🔴 **VERIFY WITH REV.IO:** ETAs for any "not supported" items, and whether workarounds are formally supported or ad hoc.

---

## 3. Pricing / Contract Terms

🔴 **This section requires direct input from your Rev.io account executive.** We are not in a position to speak to committed pricing terms, price increase caps, or multi-year contract lock-in on their behalf.

However, we would recommend asking Rev.io specifically:
- Whether price increases are **capped at 7%** or whether they **reserve the right up to 7%** (these are meaningfully different)
- Whether a signed multi-year agreement locks in per-license pricing for the full term
- Whether the prior Tigerpaw multi-year experience (with in-term increases) reflects Rev.io PSA's current contract structure or a legacy billing entity

---

## 4. QuickBooks Online Integration

🔴 **This requires direct confirmation from Rev.io.** A QuickBooks Online integration was not observed in the platform walkthrough, and it does not appear in the current integrations library.

We recommend asking Rev.io's team to provide a specific, written list of what syncs in each direction with QBO today, covering your exact list:
- Invoices ↔ QBO
- Vendor bills
- Payments
- Products/items
- GL coding
- Costs / COGS
- Customer PO data
- Partial invoicing / milestone billing

Do not accept a general "yes we integrate with QBO" — request a field-by-field sync map.

---

## 5. Tigerpaw Migration

🔴 **This requires direct input from Rev.io's implementation/migration team.** We don't have authoritative visibility into the current state of Tigerpaw migration tooling.

**What we know from the platform:**
- Customer records, contacts, and address structures in Rev.io PSA are comprehensive and well-structured for data import
- Bulk import tools exist for products (CSV-based bulk import/update)
- The platform supports custom field configuration per module, which may be needed to preserve Tigerpaw-specific data structures

**Questions to press Rev.io on:**
- What specifically migrates via automated tooling (customers, tickets, assets, products, contracts, invoice history)?
- What requires manual rebuild (configurations, templates, macros, bill profiles)?
- When is automated Tigerpaw migration tooling available — and is that a committed date?
- For data tied to features not yet available in Rev.io (e.g., RMA records), will that data be held for future import?

---

## 6. MSP Functions / Acronis / N-able

**Current State:**

Rev.io PSA includes **pre-built integrations** for both Acronis and N-able (as well as NinjaOne) in the Integrations Library. These are listed under the **RMM** category. The Acronis integration was observed in the demo environment with a "Connected" status on a customer's Integrations tab.

**On your specific questions:**

**Q: Do you need to use Acronis to access MSP functions?**
🔴 Needs verification — however, based on what's visible in the platform, the MSP-related capabilities (ticketing, asset tracking, scheduling, time logging, billing) are native to Rev.io PSA itself and not dependent on any single RMM vendor. The Acronis integration appears to be a data sync connector, not a prerequisite for MSP functionality.

**Q: Are MSP functions natively built in through Acronis?**
The core MSP service delivery functions (ticketing, SLA management, dispatch, time tracking, billing) are native to Rev.io PSA. Acronis connectivity appears to provide asset/device data and potentially monitoring alerts into the PSA, not the other way around.

**Q: What would we lose using N-able instead of Acronis?**
🔴 Needs verification — both N-able and Acronis appear in the integrations library. The depth of each integration (which data flows in which direction) needs to be confirmed by the Rev.io technical team. It is possible N-able's integration is earlier-stage than Acronis.

**Q: Exact timeline for N-able integration and specific functions?**
🔴 Needs verification — press Rev.io for a specific function list (does it sync devices? tickets? alerts? monitoring data?) and a confirmed availability date.

---

## 7. Integrations

### Microsoft Teams
**Current State:** ✅ Microsoft Teams is a **confirmed, available integration** in the Workflow Automation engine. Workflow reactions can send notifications directly to Teams channels. This means Teams alerts can be triggered by SLA breaches, ticket status changes, new ticket creation, and other workflow events.

What it is **not** (as far as currently confirmed): a bidirectional ticketing integration (i.e., creating tickets from Teams). It is notification/alert delivery.

### IT Glue
🔴 **This is a gap we need to be transparent about.** IT Glue was not observed in the Rev.io PSA integrations library. The documentation integration we observed was **Hudu**, not IT Glue. If your team saw IT Glue referenced on Rev.io's website, that may reflect a planned/roadmap item. We recommend pressing Rev.io for written confirmation of the current state and a specific availability date if it is on the roadmap.

### D-Tools
🔴 Similarly, D-Tools was not confirmed in the integrations library we reviewed. If it appeared on Rev.io's website, it should be verified as either available now or roadmap. Request a written confirmation and specific integration functionality list.

---

## 8. Inventory / Procurement / Order Flow

### Assemblies (selling a single SKU with 4–5 component SKUs)
**Current State:** Rev.io PSA does not currently support assemblies in the traditional BOM (bill of materials) sense. However, the platform offers **Packages** — bundled product groupings that can be configured with multiple line items, display options (Bundled or Itemized on quote/invoice), and associated bill profiles. This is the nearest native equivalent today.

**Practical workaround today:** Use a Package to represent the "assembly" SKU. Configure it with the component products as line items. When using Itemized display, each component shows separately on the quote/ticket; Bundled display shows as a single line. Inventory deduction per component would need to be managed separately. This is an approximation — not a true assembly with automatic component-level inventory consumption.

### Ship-to Information on PO (carry-over from ticket)
🔴 **Needs verification.** Purchase Order functionality exists in the platform, but whether ship-to information from a service ticket automatically populates the corresponding vendor PO was not confirmed in the walkthrough. This is a common pain point in legacy PSA platforms — we recommend pressing Rev.io for a specific answer and whether this is on the roadmap.

### Warranty Information in the Product Catalog
✅ **Available today.** The Asset record in Rev.io PSA includes a dedicated **Manufacturer Info** section with the following warranty-relevant fields:
- Manufacturer
- Manufacturer Part Number
- **Manufacturer Warranty Exp** (expiration date)
- Purchase Provider
- Purchase Order Number
- Purchase Date
- Last Service Date / Next Service Date

Note: This is at the **asset level** (individual serialized item), not the product catalog level. If you need warranty expiration tracked at the catalog/SKU level rather than the asset level, that distinction should be clarified with Rev.io.

### SPA Expiration Tracking / Renewal Management (Workaround)
While not natively supported as a dedicated module, a practical workaround can be built using:
1. **Custom Fields** on the Customer or Asset record — add SPA Expiration Date and SPA Type fields
2. **Workflow Automation** — create a workflow triggered by a date condition that fires X days before expiration and sends an email/Teams notification to the account manager
3. **Recurring Schedules** — create a recurring ticket for renewal follow-up tied to the expiration date
4. **Tags** — use system tags to flag accounts with active SPAs for quick filtering

This is a functional workaround, not a formal SPA management module. For high SPA volume, it may require discipline to maintain.

---

## 9. RMA Processing

**Current State:** A dedicated RMA (Return Merchandise Authorization) module was not observed in the Rev.io PSA platform during the walkthrough. This appears to be a gap relative to Tigerpaw's current capabilities.

**Recommended workaround today:**
1. Create a **ticket** of type "Service Call" or a custom type (e.g., "RMA") to track the return process
2. Use the **Parts & Labor** tab to track the returned item and replacement
3. Use **Serial Number** tracking in Inventory to update the asset record with the new serial number
4. Use **Inventory Adjustment** to remove the returned unit and add the replacement
5. **Manufacturer Warranty Exp** on the asset record can be manually updated to reflect the replacement item's warranty

**On your specific question re: updating asset serial number while maintaining warranty continuity:**
The asset record supports manual updates to Serial Number, Manufacturer Warranty Exp, and related fields. History of the original asset (tickets, notes, purchase info) would remain on the record. However, there is no automated "RMA replacement" workflow that handles this in one step — it would require manual record updates.

🔴 **Verify with Rev.io:** Whether RMA is on the roadmap and expected ETA.

---

## 10. Mobile / Barcode Scanning

**Current Mobile App:**
Rev.io PSA includes a mobile application with the following confirmed capabilities:
- GPS tracking for field technicians
- Geofencing (500ft radius) with automatic arrival/departure note creation
- Travel timer (automatic)
- Auto-notes on arrival/departure

🔴 **On barcode scanning:** This was not confirmed as available in the current mobile app. Recommend pressing Rev.io on whether it is planned, in development, or available in any form today — and requesting a specific ETA if in development.

🔴 **On "PSA Field Service" app:** We are not certain whether the app you've been using ("PSA Field Service") is the same application as the current Rev.io PSA mobile offering, or a legacy/separate product. Please clarify with Rev.io which mobile app is the current primary offering and whether PSA Field Service is being sunset, maintained, or merged.

---

## 11. Security / Permissions (RBAC)

✅ **RBAC (Role-Based Access Control) is natively available in Rev.io PSA today.**

**How it works:**
- **4 user roles** are available in the current platform
- Each role has a **granular permission matrix** with 15+ permission categories covering all major modules
- Permissions are configured via **individual checkboxes** per feature area — not just broad module-level on/off toggles
- There is a dedicated **Revii Data Analytics Mode** toggle per role, controlling access to the AI analytics interface
- **User Groups** allow technicians to be organized into groups (e.g., Tier 1, Tier 2) for ticket routing and dispatch filtering
- **105+ user records** are supported (confirmed in demo environment)

Examples of permission categories controllable per role include: customer management, billing, inventory, ticketing, scheduling, projects, admin functions, analytics, and more.

---

## 12. CommerceHub

✅ **CommerceHub is available today.** Here is what the module provides currently:

**Partners Directory:**
- A curated directory of technology partners and vendors accessible within the platform
- Grid and list view with search, sort, and category filtering
- 9 current demo partners spanning: Telecommunications, Financial Services, Cloud Solutions, AI Solutions, Marketing Services, Consulting

**Partner Profile Pages:**
- Detailed profile per partner with product/service listings
- Contact Partner functionality
- Products & Services section showing available offerings with descriptions and pricing notes

**Current Partners in Demo Environment:**
AT&T Partner Exchange, Atlantech Online, Cyber Trends, Documo, GreatAmerica Financial Services, MSP Hub, The Business Growers, TurboDocx, VoIP.ms

**What CommerceHub does NOT appear to support today (based on walkthrough):**
- Distributor product lookup / pricing catalog (e.g., real-time pricing from Ingram Micro, TD SYNNEX, etc.)
- Direct purchasing workflow from within the platform
- Live pricing visibility from distributors

🔴 **Verify with Rev.io:** Whether distributor/procurement catalog functionality is on the roadmap and when.

---

## 13. Demo Environment / Access Questions

**Q: Where do Acronis/MSP functions live?**
✅ Navigate to any Customer record → **Integrations tab** (within the Overview section). The Acronis integration is visible there with connection status. The MSP service delivery functions (ticketing, asset management, SLA, dispatch) are distributed throughout the core modules — they are not in a separate "MSP" section. The platform is MSP-native across its entire service delivery workflow.

**Q: Reporting and dashboards not accessible — permissions issue?**
✅ Yes, this is almost certainly a permissions issue. The Analytics module (powered by Apache Superset) includes 10+ published dashboards. Access is role-dependent. Request that your demo environment user be granted Analytics access. The module includes: Service Dashboard, Revenue Analysis, Profit by Technician, Inventory Levels, Inventory Valuation, Inventory Aging, Stock Movement, Tax Details, and more.

**Q: Demo environment with sample data?**
✅ The standard Rev.io PSA demo environment already includes substantial sample/example data — 200+ customers, 115+ products, 498+ time entries, 1,121+ inventory transactions, 10 projects, and 30+ opportunities. If your access was to a blank environment, that is unusual — request access to the standard demo tenant (psasalesdemo.psarev.io).

**Q: Distributor/product lookup — where does it live?**
The **Commerce Hub** module contains the Partners directory. However, live distributor catalog lookup (e.g., searching Ingram pricing in real time) does not appear to be available today. 🔴 Verify with Rev.io.

**Q: Warranty information when adding a product to catalog?**
Warranty information is tracked at the **asset (serialized item) level**, not at the product catalog level. When you add a product to the catalog, there is no warranty field on the product record itself. When that product is deployed to a customer and becomes an asset, the asset record includes Manufacturer Warranty Exp, Purchase Date, and related fields.

**Q: What is a "Package"?**
A Package in Rev.io PSA is a bundled product grouping — it allows you to combine multiple products (recurring services, one-time items, equipment) into a single named bundle. Packages can be configured with:
- Bill Profile assignment
- Rate Deck Group (for VoIP/metered services)
- Provider restrictions
- Display setting: Bundled (shows as one line) or Itemized (shows each component)

Packages are most commonly used for service bundles — e.g., a "Managed Services Starter" package that includes a recurring software license, a router, and a professional services line item.

**Q: What are macros and how are they used?**
✅ Macros are pre-configured ticket templates that allow technicians to create fully populated tickets with a single click. Two types exist:
- **New Ticket Macros (7 in demo):** Pre-fill ticket type, status, priority, description, tech group, and work requested when creating a ticket. Examples: Access Control Installation, Emergency On-Site, Network Down, New Security System Installation, Password Reset, UCaaS Deployment, VPN Access Issue.
- **Activity Macros (9 in demo):** Pre-fill common activity entries on existing tickets.

Macros are configured in Admin → System Settings → Macros.

**Q: Customer portal access/experience?**
✅ The Customer Portal is a self-service web interface available to your customers. Current capabilities:
- View and pay invoices online
- Update payment methods (cards/bank accounts)
- Submit new service tickets directly to your queue
- View open tickets with status, severity, and type visible
- See public notes on active tickets

Portal access is configured per customer and feature toggles (Invoices, Tickets, Contacts) can be enabled/disabled individually in Admin.

---

## 14. Customer References

🔴 **Tony — please provide 2–3 reference customers here.** Ideally matching one or more of:
- Migrated from Tigerpaw or legacy Rev.io environments
- Hybrid IT + service + project operations
- Hardware procurement / inventory complexity
- MSP operations

---

## Summary: Items Requiring Rev.io Verification Before Sending

Before this response goes to Alyse, the following items need direct confirmation from your Rev.io account executive or product team:

| # | Item | Question |
|---|---|---|
| 1 | Commission reporting | Roadmap ETA, committed or subject to change? |
| 2 | Assemblies | Packages a confirmed workaround? Any roadmap for true BOM? |
| 2 | Report scheduling | Available today or roadmap? |
| 2 | Change orders | Formal support or workaround? |
| 2 | Vendor delivery tracking | Available on POs today? |
| 3 | Pricing / contract terms | All pricing questions need AE input |
| 4 | QuickBooks Online | Current sync capabilities, field by field |
| 5 | Tigerpaw migration | What migrates, what doesn't, ETA for tooling |
| 6 | N-able vs Acronis | Depth comparison, N-able integration ETA |
| 7 | IT Glue | Current state — available or roadmap? |
| 7 | D-Tools | Current state — available or roadmap? |
| 8 | Ship-to on PO | Does ticket ship-to carry to PO? |
| 9 | RMA | Roadmap and ETA |
| 10 | Barcode scanning | Status and ETA |
| 10 | PSA Field Service app | Relationship to current Rev.io mobile app |
| 12 | CommerceHub / distributor lookup | Real-time pricing/catalog roadmap |
| 14 | References | Tony to provide 2–3 customer names |
