# Process Parity Register

**Rev.io PSA build to-do list**  
**Evidence reviewed:** 24 November 2026

> Build what removes the migration blockers.

A prioritized build to-do list for capabilities most likely to block or materially end a migration.

## At a glance

- **2** critical commercial and finance foundations
- **14** clearly defined build needs

## Where to start

**Start with two foundations:**

1. Pricing rules across quotes, orders, agreements, and billing
2. GL rules for revenue, COGS, class, and accounting fields

Shared commercial and accounting rule engines reduce manual controls across the lifecycle.

## Build register

Only concrete, clearly defined process gaps likely to block or materially end a migration from HaloPSA, ConnectWise PSA/Manage, or Autotask PSA.

**Evidence note:** A roadmap release label is not production proof or a commitment to deliver. Every listed capability is an approved build need; evidence documents scope and current state.

## 1. Pricing rules across quotes, orders, agreements, and billing

**Category:** Commercial

**What we need to build:** One pricing service for quotes, orders, agreements, change orders, renewals, and billing. Rules must support customer, contract, item, manufacturer, and category pricing; quantity tiers; volume discounts; target margins; minimum and maximum prices; clear rule priority; rules for when discounts can be combined; currencies; and start and end dates.

**Why it blocks deals:** Migrating customers will reject manual repricing that increases quote time, creates renewal inconsistency, and exposes gross margin on every transaction.

**Where Rev.io stands today:** Planned. Pricing Rules is Backlog/Not Started. Pricing Enhancements Core and Tiered Pricing / Volume Pricing are Viking 3 with PRD Complete but Not Started/At Risk; older duplicate rows remain unresolved.

**Incumbent benchmark:** Autotask documents price lists, customer-specific pricing, work-type modifiers, multi-currency, and volume/tier pricing. Halo documents margin-triggered approvals. ConnectWise provides established quoting and procurement workflows.

**What done looks like:** Configure reusable rule sets; resolve rule conflicts consistently; calculate from a cost record with a date and time; support tier and volume math; enforce margin floors; simulate before publication; explain each calculated price; record approved overrides; apply identical logic in all named transaction types; and preserve historical price calculations after rules change.

## 2. GL rules for revenue, COGS, class, and accounting fields

**Category:** Finance

**What we need to build:** Accounting rules with start and end dates and a clear priority order that assign revenue account, COGS account, class, department, division, location, and project dimensions per invoice or cost line from customer, item/service, contract, site, project, and transaction context.

**Why it blocks deals:** Multi-entity and project-accounting customers cannot replace duplicate catalog items and manual post-sync corrections with another manual control. A weak mapping model undermines financial accuracy and close confidence.

**Where Rev.io stands today:** Planned. Context-Based GL Account Assignment per Invoice Line is Viking 3 Backlog/Not Started; QBO v2 – Per-line GL and class from the rules engine, Simple COGS journal entries, and Complex cost sync are Viking 4/Not Started. Existing product/default mapping does not close this contextual requirement.

**Incumbent benchmark:** ConnectWise documents GL mapping and accounting export. Autotask uses connected accounting systems for financial posting. Halo documents account-code and tax mapping through its accounting integrations.

**What done looks like:** Create ordered rules with AND/OR conditions, effective dates, fallbacks, and conflict detection; simulate a line before posting; show the winning rule; require reasoned overrides; version and audit rules; send consistent accounting fields to each supported connector; block invalid mappings; and correct and retry failed postings without creating duplicates.

## 3. Complete QuickBooks Online sync and accounting controls

**Category:** Finance

**What we need to build:** Certified QBO v2 synchronization for products/configuration, many-to-one mappings, controlled record creation, payments and reversals, purchase orders, per-line dimensions, COGS, exception handling, and reconciliation.

**Why it blocks deals:** QBO customers will not accept parallel manual entry for cash application, POs, mappings, or cost recognition. A connector that cannot match records and retry safely becomes a financial-control blocker.

**Where Rev.io stands today:** Incomplete/planned. Products & config parity is Viking 3/Not Started; Payment sync was In Progress; many-to-one product mapping, automatic creation or approval, and purchase orders are Viking 4/Not Started. Per-line GL/class and COGS dependencies are also Not Started.

**Incumbent benchmark:** ConnectWise and Halo document accounting integrations with QuickBooks. Autotask exports operational and billing data to connected accounting systems.

**What done looks like:** Publish and pass a clear list of what data moves to and from QuickBooks; map products many-to-one; choose auto-create versus approval; sync payments, voids, refunds, and reversals; sync POs; send per-line dimensions and COGS; provide unique transaction IDs; surface actionable exceptions; retry without creating duplicates; and reconcile Rev.io totals and record IDs to QBO by accounting period.

## 4. Role-based cost visibility across the platform

**Category:** Security

**What we need to build:** A platform-wide role permission that controls whether a user can see cost, margin, markup, profit, and any value calculated from cost. The same permission must apply across quotes, tickets, projects, products, purchasing, inventory, agreements, reports, dashboards, search, exports, APIs, notifications, print views, and mobile experiences.

**Why it blocks deals:** Many service organizations do not want technicians, subcontractors, or other limited-access users to see internal costs or profit margins. If cost is hidden in one area but exposed somewhere else, sensitive commercial information can leak and the customer cannot safely give people the access they need to do their jobs.

**Where Rev.io stands today:** Planned but incomplete. The live roadmap has two Subcontractor Role rows: one in Backlog and one assigned to Viking 2; both are Not Started, At Risk, and PRD Complete. They call for hiding cost when a subcontractor adds products to a ticket. A separate Subcontractor Login item is also Backlog/Not Started and says cost should be hidden by default. None of these rows proves one platform-wide cost visibility permission across every screen, report, export, and API.

**Incumbent benchmark:** Autotask documents security-level controls over the visibility of charges, expenses, contract costs, and project costs. This makes role-based protection of internal financial information an established PSA expectation.

**What done looks like:** Add a role permission for viewing cost-sensitive information. When it is off, hide cost, margin, markup, profit, and all values calculated from cost everywhere in the platform, including user screens, reports, dashboards, search results, exports, APIs, notifications, print views, and mobile. Keep customer price and revenue visible when the role is allowed to see them. Do not send hidden values to the browser or API response where they could still be found. Apply the rule to technicians, subcontractors, customer users, impersonation, and delegated access. Record every permission change with the person and date, and provide a test checklist covering every product area.

## 5. Complete change orders for tickets and projects

**Category:** Commercial

**What we need to build:** A complete change-order process initiated from either a ticket or project that can add, remove, or modify scope, quantities, labor, materials, dates, price, cost, margin, tax, and billing treatment; route internal approval; obtain customer approval/e-signature; keep every version; and update delivery, purchasing, invoicing, accounting export, and the original commercial baseline without losing the link to the original quote or project.

**Why it blocks deals:** Incumbent migrations fail when active work cannot retain its signed baseline and approved changes. Without this control, scope disputes, margin leakage, duplicate billing, audit gaps, and accounting reconciliation become implementation risks the buyer cannot accept.

**Where Rev.io stands today:** Planned/incomplete. Roadmap rows show Project Change Request / Change Orders – Add Scope at Viking 4/Discovery, Remove Scope at Viking 4/Not Started, Customer Signature at Viking 4/Not Started, and Invoice as Quoted at Viking 4 Backlog/Not Started. The evidence does not show an equivalent ticket-originated commercial process or end-to-end accounting continuity.

**Incumbent benchmark:** ConnectWise, Autotask, and Halo provide established project, billing, and procurement foundations used to control project scope and financial changes. Halo ITIL Change Management is distinct from commercial change orders.

**What done looks like:** From a ticket and from a project, create a change against a locked original; add/remove/change lines and narrative scope; calculate price, cost, margin, tax, schedule, PO, and billing impacts; preview impacts; run configurable internal approval; capture customer signature with timestamp and signed artifact; reject/revise/resubmit; apply only the approved version; update forecast, purchasing, billing schedule, invoice grouping, and accounting payload once; show old/new values and actor/time in an exportable audit trail; reverse or replace with a newer version without deleting history.

## 6. Reliable quote-to-project, order, agreement, and purchasing conversion

**Category:** Commercial

**What we need to build:** A reliable, repeatable process that turns an accepted quote into the selected project, phases and tasks, tickets, agreements and services, sales or order records, purchasing needs, assets, and billing schedule. Every created record must stay linked to its original quote line and keep the original quantities, prices, costs, discounts, taxes, descriptions, attachments, and billing terms.

**Why it blocks deals:** Buyers moving from mature PSAs will not accept rekeying sold work or reconciling disconnected delivery records. Lost line relationships lead directly to missed purchasing, incorrect billing, and failed cutover testing.

**Where Rev.io stands today:** Partial/planned. Quote to Planner to Project to Order is Viking 4/Discovery; the conversion portion of Quote Approval Routing is still active work. PSA Quote Creation and Distributor Order Submission were in development in the source evidence. No production proof establishes the complete object and field mapping.

**Incumbent benchmark:** Autotask activates Proposal Projects and can create contract, project, or ticket charges from quoted products. Halo documents sales-order-line-to-project creation. ConnectWise documents project handoff and quote-to-order routing.

**What done looks like:** Configure line-to-destination rules; preview generated objects; convert once with safe retries that do not create duplicates; create project structure from templates; branch recurring, one-time, labor, material, and asset lines correctly; preserve IDs, descriptions, quantities, price, cost, discount, tax, options, attachments, and billing terms; create purchasing demand where required; expose exceptions; and show where every quote line went after conversion.

## 7. Carry the signed SOW into projects, tickets, and orders

**Category:** Delivery

**What we need to build:** Structured SOW sections, assumptions, exclusions, deliverables, milestones, acceptance terms, attachments, and revisions that become a locked signed source and remain traceable in projects, tickets, orders, and subsequent change orders.

**Why it blocks deals:** A buyer cannot migrate project delivery if the authoritative scope becomes a PDF attachment with no governed relationship to execution. Disputes, technician ambiguity, and unprovable change control outweigh switching value.

**Where Rev.io stands today:** Planned. Scope of Work Transfer from Quote to Ticket/Project/Order is Viking 4 Backlog/Not Started; Attach Supporting Documents to Customer Proposals is Backlog/Not Started. The evidence does not establish structured baseline carry-forward.

**Incumbent benchmark:** Halo documents project-sales templates containing SOW, terms, and project tasks. Autotask supports proposal-project activation. ConnectWise documents project handoff from sold work.

**What done looks like:** Author structured scope; version it; approve and sign a fixed version; securely store the signed document; carry configured sections and attachments to each destination; display source and replacement links; prevent silent edits to accepted scope; link every approved change to affected baseline sections; and export a complete baseline/change timeline.

## 8. Form management by ticket and issue type

**Category:** Service

**What we need to build:** An administrator-managed form builder that assigns different intake forms to ticket types, issue types, service requests, and portal request options. Each form can control sections, questions, field types, required fields, conditional visibility, validation, help text, attachments, and field-to-ticket mapping for both internal users and external customer-portal submitters.

**Why it blocks deals:** Generic ticket intake forces technicians and dispatchers to chase missing information, increases triage time, and makes the customer portal feel materially weaker than mature PSA service catalogs. Clients migrating from structured request processes will not accept losing issue-specific intake for onboarding, access requests, incidents, changes, purchasing, and other repeatable requests.

**Where Rev.io stands today:** Absent/not proven. The reviewed product evidence shows ticket types, custom fields, portal ticket submission, and reusable ticket/service concepts, but it does not establish a delivered administrator-managed form builder with type-specific layouts and conditional questions. No exact delivered roadmap item proving this boundary was found in the reviewed evidence.

**Incumbent benchmark:** Halo documents service-request and portal experiences organized around request types and configurable forms. ConnectWise and Autotask support structured ticket categorization and custom-field-driven intake.

**What done looks like:** Create and version forms without code; bind a form to one or more ticket/issue/request types; support text, choice, date, number, checkbox, customer/contact/site/asset/service selectors, and file uploads; make questions required or conditionally visible; validate input before submission; use the same definition internally and in the customer portal with permission-aware fields; map answers to ticket fields and structured form responses; set the resulting ticket type and other configured defaults; preserve the submitted version and answers in the ticket audit history; and report/filter on captured values.

## 9. SLA policy assignment by ticket type

**Category:** Service

**What we need to build:** Assign a different SLA policy based on Ticket Type—not only by customer—with explicit precedence among instance default, customer, agreement/contract, ticket type, and authorized ticket-level override.

**Why it blocks deals:** One customer may have materially different response and resolution commitments for incidents, service requests, projects, access requests, and after-hours emergencies. Forcing one customer-level SLA makes contractual reporting inaccurate or requires manual priority manipulation and parallel operational processes.

**Where Rev.io stands today:** Planned/not available. Current SLA policy assignment is customer-level, with targets varying by priority. The roadmap item Ticketing - Expand SLAs specifically proposes SLAs by ticket type and is Viking 4/Not Started. Instance Default SLA with Customer Override is also Backlog/Not Started and does not itself provide ticket-type selection.

**Incumbent benchmark:** Halo explicitly documents SLA defaults by ticket type with additional override layers. ConnectWise and Autotask support configurable SLA and workflow behavior.

**What done looks like:** Select a default SLA policy on every active Ticket Type; define and display the precedence chain; show the effective policy and source on the ticket; apply the correct response/resolution targets, business hours, pause conditions, and escalation thresholds; recalculate consistently when Ticket Type changes while preserving elapsed-time history; restrict manual overrides by permission and require a reason; retain an audit trail of every policy/source change; and report SLA performance by Ticket Type and effective policy.

## 10. Configurable internal quote approval policy

**Category:** Governance

**What we need to build:** Internal approval rules that keep version history and can be triggered by amount, margin, discount, product/type, customer, term, and risk, with sequential or parallel stages, role/group resolution, delegation, escalation, rejection/rework, expiry, and a decision history that cannot be edited.

**Why it blocks deals:** Signature alone does not satisfy company approval limits. Buyers cannot move commercial governance to a system that permits unauthorized discounts or cannot evidence who approved a low-margin deal.

**Where Rev.io stands today:** Partial/planned. Quote Approval Routing was In Progress/Viking 3/PRD Complete; its documented scope did not prove the complete policy model. Separate threshold/approval work remained backlog.

**Incumbent benchmark:** ConnectWise documents peer review, management approval, customer signature, and contract-approval controls. Halo documents internal and margin-triggered approvals. Autotask documents customer electronic approval.

**What done looks like:** Build conditions without code; support combined AND/OR rules; choose approvers by role and limit; run approval steps that run in order or at the same time; delegate with dates; escalate on SLA; capture comments and attachments; reject to a named revision; require approval again when governed fields change; prevent downstream execution until final approval; and export the full decision trail.

## 11. Configurable time approval and one queue for unbilled work

**Category:** Revenue Ops

**What we need to build:** A configurable approval step for time entries, paired with one billing-review queue for unlinked labor, parts, expenses, shipping, reopened work, and work added after the final invoice. Each company can require approval for all time, require it only for selected workers, work types, contracts, or customers, or turn approval off and bill eligible time directly.

**Why it blocks deals:** Service firms need different levels of control. Some require time approval for payroll, quality, or contract compliance; others need approved work to move to billing immediately. A forced approval step delays invoices, while having no approval option at all weakens control for companies that need it.

**Where Rev.io stands today:** Partial/planned. Pending Invoicing Queue for Closed Tickets with Unbilled Items is Backlog/Not Started; Ticketing – Modify Send to Billing Functionality is Viking 4/Not Started. The evidence does not show flexible approval rules plus one complete queue for all unbilled work.

**Incumbent benchmark:** ConnectWise and Autotask document configurable time and expense review and approval. Halo documents timesheet approval and billable-time review.

**What done looks like:** Let administrators turn time approval off, require it for all time, or apply it only when rules match a worker, role, work type, contract, customer, or other selected condition. When approval is off, eligible billable time can move directly to billing. When approval is required, users can submit, approve, reject, correct, and lock time with the person, date, and reason recorded. Collect every unbilled charge type in one queue; show its source, age, amount, customer, owner, and blocking reason; let authorized users assign, resolve, write off, or defer items; check again after reopened work; and match every resolved item to its invoice result.

## 12. Agreement rollover, renewals, coverage, and license matching

**Category:** Recurring Revenue

**What we need to build:** Agreement policies for block-hour rollover/expiry, renewal and notice windows, automatic service coverage selection, and vendor subscription quantity/cost matching with reviewed differences and updates with clear start dates.

**Why it blocks deals:** MSP migrations fail when recurring revenue, covered work, and vendor license counts cannot be trusted. Unbilled seats and incorrect renewals directly erode margin and customer confidence.

**Where Rev.io stands today:** Partial/planned. Block-hour rollover has duplicate Not Started/At Risk rows; Agreement Workflows remained In Progress; Automated Renewal Workflows for Agreement Changes is Backlog/Not Started; Pax8, Ingram Micro CSP, and TD Synnex Stellr One tier/usage parity rows are Viking 4/Not Started.

**Incumbent benchmark:** Autotask documents contract lifecycle and compliance controls. ConnectWise and Halo document recurring agreements, contract billing, and service coverage.

**What done looks like:** Configure rollover/expiry by agreement; calculate balances the same way every time; track renewal and notice dates; trigger owner workflows; select coverage consistently for a ticket; import vendor quantities and costs; match to customer/service lines; queue unmatched and changed records; require approval before create/update/cancel; apply effective dates; and audit each connector run and billing result.

## 13. Physical inventory counts and variance review

**Category:** Inventory

**What we need to build:** Controlled cycle/full counts by location with count sheets or barcode capture, blind-count options, variance review, approval, adjustments, serial and lot tracking where applicable, reservations, valuation impact, and audit.

**Why it blocks deals:** Product-heavy service organizations cannot cut over from mature stock controls if opening quantities and ongoing counts must be maintained in spreadsheets. Inventory and project-cost errors become immediate balance-sheet and fulfillment risks.

**Where Rev.io stands today:** Planned. Inventory – Physical Inventory appears in duplicate Viking 4 Backlog/Not Started rows with inconsistent maturity; no production count/reconciliation proof is present.

**Incumbent benchmark:** Autotask documents inventory locations, transfers, allocations, purchasing, and receiving. ConnectWise documents procurement and inventory operations. Halo documents stock locations, purchasing, receipt, and allocation.

**What done looks like:** Freeze or snapshot count scope; generate blind or expected count sessions; scan or enter item/serial quantities by location; support recounts; calculate variances; require approval above thresholds; post traceable adjustments once; preserve reservation integrity; update valuation/export consistently; and produce before/after and actor/time audit reports.

## 14. RMA, replacements, vendor credits, and serial tracking

**Category:** Inventory

**What we need to build:** A dedicated customer/vendor RMA lifecycle linking the original sale, asset/serial, ticket/project, return authorization, inbound/outbound shipment, replacement/loaner, vendor return, credit, inventory movement, and accounting effect.

**Why it blocks deals:** Hardware-service customers cannot migrate open returns into generic tickets without losing serial custody, vendor recovery, customer replacement status, or credits. That leakage is concrete and measurable.

**Where Rev.io stands today:** Incomplete. The process-history evidence records serialized-equipment intake, duplicate prevention, repair/RMA lifecycle, vendor credits, secondary serial IDs, counts, and labels as unresolved needs. The prior register found no single current roadmap row that proves a complete RMA boundary.

**Incumbent benchmark:** ConnectWise and Autotask provide established procurement and inventory operations. Halo provides purchase-order and stock workflows for receiving, allocation, and returns.

**What done looks like:** Create an RMA from the original transaction or asset; validate serial and duplicate requests; issue authorization and labels; track custody/status; receive and inspect returns; create replacement or loaner movement; create linked vendor RMA; record expected and received vendor credit; update stock and asset state; carry costs/credits to billing and accounting exactly once; and report aging, exceptions, and full movement history.

---

**Evidence note:** Roadmap labels are directional evidence—not production proof or a commitment to deliver. The “What done looks like” section defines completion for each required capability.
