# Rev.io PSA ↔ Salesforce Integration

**Setup and User Guide**  
**Version:** 2.0  
**Updated:** May 28, 2026  
**Audience:** Customer admins, Rev.io implementation teams, and support teams

---

## 1. Overview

The Rev.io PSA ↔ Salesforce integration keeps customer, contact, opportunity, and operational visibility data aligned between Salesforce and Rev.io PSA.

Salesforce remains the system of record for CRM activity. Rev.io PSA remains the operational system for service delivery, ticketing, billing context, and customer management.

### What the Integration Does

- Syncs **Salesforce Accounts** to **Rev.io PSA Customers**
- Syncs **Salesforce Contacts** to **Rev.io PSA Contacts**
- Creates or updates **Rev.io PSA Opportunities** from qualifying Salesforce Opportunities
- Writes Rev.io record IDs back to Salesforce so future syncs update existing records instead of creating duplicates
- Enriches Salesforce Accounts with open PSA ticket visibility

### Setup Ownership

Some configuration is handled by the customer, and some is handled by Rev.io.

| Area | Owner | Notes |
|---|---|---|
| Salesforce custom fields | Customer Salesforce admin | Required before activation |
| Salesforce credentials | Customer Salesforce admin | Entered during integration setup |
| PSA user/API connection | Rev.io / implementation team | Provisioned inside the client integration instance |
| Sync filters and behavior | Customer admin with Rev.io guidance | Configured in the setup wizard |
| Validation and go-live testing | Customer + Rev.io | Run through the test plan before production use |

> Important: In the client-facing setup wizard, customers should not need to enter PSA User/API information. Rev.io provisions the PSA connection inside the customer's integration instance.

---

## 2. Before You Start

### Access Needed

- Salesforce admin access
- Permission to create Salesforce custom fields
- Permission to reset or retrieve a Salesforce security token
- Access to the Rev.io integration activation page or marketplace entry
- Confirmation from Rev.io that the PSA connection has been provisioned for the customer's instance

### Estimated Setup Time

Plan for **30-45 minutes** for setup and basic validation.

More time may be needed if Salesforce field-level security, profile permissions, or account type filters need internal approval.

### Recommended Prep

Before starting, decide:

- Which Salesforce Account Type values should sync
- Which Salesforce Opportunity stage should create PSA Opportunities
- Whether Opportunity sync should be enabled at launch
- Who owns Salesforce credential rotation
- Who should receive support/escalation notices

---

## 3. Salesforce Field Setup

The integration uses Salesforce custom fields to store Rev.io IDs and PSA visibility data. These fields allow the integration to safely update existing records after the first sync.

### How to Create a Custom Field

1. In Salesforce, go to **Setup**.
2. Open **Object Manager**.
3. Select the object: **Account**, **Contact**, or **Opportunity**.
4. Go to **Fields & Relationships**.
5. Select **New**.
6. Choose the field type shown below.
7. Enter the exact field label and API name.
8. Set field-level security so the integration user can read and write the field.
9. Add the field to relevant page layouts if users should see it.
10. Save.

### Account Fields

| Field Label | API Name | Type | Length | Required | Purpose |
|---|---|---|---:|---|---|
| Rev.io ID | `Rev_io_ID__c` | Text | 50 | Yes | Stores the Rev.io PSA Customer ID |
| Open PSA Tickets | `Open_PSA_Tickets__c` | Long Text Area | 32768 | Recommended | Stores a readable summary of open PSA tickets |

### Contact Fields

| Field Label | API Name | Type | Length | Required | Purpose |
|---|---|---|---:|---|---|
| Rev.io Contact ID | `Rev_io_Contact_ID__c` | Text | 20 | Yes for Contact sync | Stores the Rev.io PSA Contact ID |

### Opportunity Fields

| Field Label | API Name | Type | Length | Required | Purpose |
|---|---|---|---:|---|---|
| Rev.io ID | `Rev_io_ID__c` | Text | 50 | Yes for Opportunity sync | Stores the Rev.io PSA Opportunity ID |
| PSA Client Code | `PSA_Client_Code__c` | Text | 50 | Optional | Stores or overrides a PSA client code |
| PSA Bill Profile ID | `PSA_Bill_Profile_Id__c` | Text | 20 | Optional | Links an Opportunity to a PSA billing profile |

### Field Setup Notes

- The API names must match exactly.
- `Open_PSA_Tickets__c` should be a Long Text Area, not a standard Text field.
- The Salesforce user used by the integration must have read/write access to each required field.
- If Opportunity sync is not enabled, Opportunity fields can be added later.

---

## 4. Salesforce Credential Setup

The integration connects to Salesforce using the credentials entered in the setup wizard.

### Information Needed

| Setting | Example | Notes |
|---|---|---|
| Salesforce Instance URL | `https://yourcompany.my.salesforce.com` | Use the exact production or sandbox URL |
| Salesforce Username | `integration.user@company.com` | Dedicated integration user recommended |
| Salesforce Password | Stored securely in the wizard | Follow customer password policies |
| Salesforce Security Token | Token from Salesforce user settings | Required for username/password auth |

### Reset a Salesforce Security Token

1. Log in to Salesforce as the integration user.
2. Select the profile avatar.
3. Open **Settings**.
4. Under **My Personal Information**, select **Reset My Security Token**.
5. Select **Reset Security Token**.
6. Copy the token from the Salesforce email.

> Security tokens reset when the Salesforce password changes. If the password is rotated, update the integration credentials with the new token.

### Dedicated Integration User

Rev.io recommends a dedicated Salesforce integration user instead of an individual employee account. This reduces the chance of sync interruptions caused by employee role changes, MFA policy changes, or password resets.

---

## 5. Activate and Configure the Integration

Open the Rev.io integration activation page or the Rev.io Integration Marketplace entry for the Salesforce integration. The wizard may vary slightly by customer environment, but the setup should follow this structure.

### Page 1: Salesforce Connection

Enter and test the Salesforce connection.

| Field | Description |
|---|---|
| Salesforce Instance URL | Production or sandbox Salesforce URL |
| Username | Salesforce integration user username |
| Password | Salesforce integration user password |
| Security Token | Salesforce token for the same user |

Expected result: the wizard validates the Salesforce connection and allows you to continue.

### PSA Connection Handling

The PSA User/API connection is provisioned by Rev.io inside the customer's integration instance.

Customers should not need to provide:

- PSA username
- PSA password
- PSA API key
- PSA user API details

If the wizard asks for PSA API credentials, stop and confirm the customer is using the correct integration instance.

### Page 2: Sync Settings

Configure the core sync behavior.

| Setting | Recommended Starting Value | Description |
|---|---|---|
| Account Type Filter | Customer-specific | Only sync Salesforce Accounts with matching Type values. Leave blank only if all accounts should sync. |
| Opportunity Stage Filter | `Closed Won` | Only sync Opportunities once they reach the selected stage. |
| Sync Schedule | Every 12 hours | Scheduled sync safety net. Real-time triggers may also run between scheduled jobs. |
| Batch Size | Default | Number of records processed per run. Increase only with Rev.io guidance. |
| Bill Profile ID | Blank unless instructed | Optional default PSA billing profile behavior. |
| Debug Mode | Off | Enable only during troubleshooting. |

### Page 3: Opportunity Sync

Use this page if Salesforce Opportunities should create Rev.io PSA Opportunities.

| Setting | Description |
|---|---|
| Trigger Stages | Salesforce stages that should create or update PSA Opportunities |
| Default PSA Stage | PSA stage assigned when a new Opportunity is created |
| Default PSA Type | PSA Opportunity type assigned on creation |
| Default PSA Status | PSA status assigned on creation |
| Stage Map | Maps Salesforce stages to PSA stage values |
| Status Map | Maps Salesforce stages to PSA status values |

Recommended launch pattern: start with `Closed Won` only, validate results, then expand if the customer's workflow requires earlier-stage syncing.

### Page 4: Review and Enable

Before enabling:

- Confirm Salesforce connection test passes.
- Confirm PSA connection has been provisioned by Rev.io.
- Confirm required Salesforce fields exist.
- Confirm field-level security allows the integration user to read/write required fields.
- Confirm filters are intentionally scoped.
- Run the validation test plan below.

---

## 6. How the Sync Works

### Account to Customer Sync

| Salesforce | Rev.io PSA | Direction |
|---|---|---|
| Account Name | Customer Name | Salesforce to PSA |
| Billing Street | Billing Address | Salesforce to PSA |
| Billing City | Billing City | Salesforce to PSA |
| Billing State | Billing State | Salesforce to PSA |
| Billing Postal Code | Billing ZIP | Salesforce to PSA |
| Billing Country | Billing Country | Salesforce to PSA |
| Phone | Phone | Salesforce to PSA |
| Website | Website | Salesforce to PSA |
| `Rev_io_ID__c` | PSA Customer ID | Written back to Salesforce |
| `Open_PSA_Tickets__c` | Open ticket summary | PSA to Salesforce |

On first sync, the integration creates the PSA Customer and writes the new PSA ID to `Rev_io_ID__c`. On later syncs, that ID is used to update the existing PSA Customer.

### Contact to Contact Sync

| Salesforce | Rev.io PSA | Direction |
|---|---|---|
| First Name | First Name | Salesforce to PSA |
| Last Name | Last Name | Salesforce to PSA |
| Email | Email | Salesforce to PSA |
| Phone | Phone | Salesforce to PSA |
| Title | Title | Salesforce to PSA |
| Related Account | Parent Customer | Salesforce to PSA |
| `Rev_io_Contact_ID__c` | PSA Contact ID | Written back to Salesforce |

Contacts should sync after their parent Account has a Rev.io ID. If the Account has not synced yet, the Contact may be skipped until the Account is linked.

### Opportunity to Opportunity Sync

| Salesforce | Rev.io PSA | Direction |
|---|---|---|
| Opportunity Name | Opportunity Name | Salesforce to PSA |
| Account | Customer | Salesforce to PSA |
| Amount | Value / Estimate | Salesforce to PSA |
| Stage | Stage / Status via mapping | Salesforce to PSA |
| Close Date | Expected Close Date | Salesforce to PSA |
| `Rev_io_ID__c` | PSA Opportunity ID | Written back to Salesforce |
| `PSA_Client_Code__c` | Client Code | Salesforce to PSA |
| `PSA_Bill_Profile_Id__c` | Bill Profile ID | Salesforce to PSA |

Opportunity sync is usually gated by stage so draft or early-stage deals do not create operational work too early.

### Open PSA Ticket Visibility

The integration can summarize open PSA tickets on the Salesforce Account. This gives sales and account teams visibility into active service issues without requiring them to leave Salesforce.

The summary is written to `Open_PSA_Tickets__c`.

---

## 7. User Guide

### For Sales Users

Use Salesforce normally.

- Keep Account names, phone numbers, websites, and billing addresses current.
- Make sure Contacts are related to the correct Account.
- Move Opportunities through the agreed sales stages.
- Do not edit Rev.io ID fields manually.
- Review the Open PSA Tickets field before customer calls when available.

### For Salesforce Admins

Monitor the integration user and field permissions.

- Keep the integration user's password and token current.
- Avoid removing field-level access to required fields.
- Coordinate changes to Account Type or Opportunity Stage values with Rev.io before changing filters.
- Notify Rev.io before renaming picklist values used in sync filters or mappings.

### For PSA Users

Use Rev.io PSA as the operational system.

- Treat synced Customers and Contacts as linked records from Salesforce.
- Avoid creating duplicate Customers manually when a Salesforce Account should sync.
- Use PSA tickets, opportunities, and billing workflows as normal.
- Escalate duplicate or stale-link issues before manually clearing IDs.

### Fields Users Should Not Edit

These are system-link fields and should be treated as read-only by end users:

- Account: `Rev_io_ID__c`
- Account: `Open_PSA_Tickets__c`
- Contact: `Rev_io_Contact_ID__c`
- Opportunity: `Rev_io_ID__c`
- Opportunity: `PSA_Bill_Profile_Id__c`, unless Rev.io has instructed the customer to maintain it manually

---

## 8. Validation Test Plan

Run these tests before go-live.

### Test 1: Account Creation

1. Create or select a Salesforce Account that matches the Account Type Filter.
2. Populate name, phone, website, and billing address.
3. Run the sync or wait for the configured trigger.
4. Confirm a matching Customer appears in Rev.io PSA.
5. Confirm Salesforce Account `Rev_io_ID__c` is populated.

Pass criteria: one PSA Customer is created and linked back to Salesforce.

### Test 2: Account Update

1. Update the Salesforce Account phone or website.
2. Run the sync.
3. Confirm the existing PSA Customer is updated.

Pass criteria: the existing PSA Customer updates and no duplicate customer is created.

### Test 3: Contact Sync

1. Add a Contact to a synced Salesforce Account.
2. Populate name, email, phone, and title.
3. Run the sync.
4. Confirm the Contact appears under the correct PSA Customer.
5. Confirm `Rev_io_Contact_ID__c` is populated in Salesforce.

Pass criteria: the Contact is linked to the correct PSA Customer.

### Test 4: Opportunity Sync

1. Create a Salesforce Opportunity under a synced Account.
2. Move it to the configured trigger stage.
3. Run the sync or trigger the webhook.
4. Confirm the Opportunity appears in PSA with the expected stage, status, type, and customer.
5. Confirm Salesforce Opportunity `Rev_io_ID__c` is populated.

Pass criteria: one PSA Opportunity is created and linked back to Salesforce.

### Test 5: Ticket Visibility

1. Confirm the Salesforce Account is linked to a PSA Customer.
2. Confirm the PSA Customer has open tickets.
3. Run the sync.
4. Review `Open_PSA_Tickets__c` on the Salesforce Account.

Pass criteria: the Salesforce Account shows a readable summary of open PSA tickets.

---

## 9. Troubleshooting

### Accounts Are Not Syncing

Check:

- Does the Account match the configured Account Type Filter?
- Does the integration user have access to the Account?
- Does `Rev_io_ID__c` exist on the Account object?
- Does the integration user have read/write access to `Rev_io_ID__c`?
- Is the Salesforce connection test successful?

### Contacts Are Not Syncing

Check:

- Is the Contact related to an Account?
- Has the parent Account already synced to PSA?
- Does `Rev_io_Contact_ID__c` exist on the Contact object?
- Does the integration user have access to the Contact and required fields?

### Opportunities Are Not Syncing

Check:

- Is Opportunity sync enabled?
- Does the Opportunity stage match the trigger stage?
- Is the Opportunity related to a synced Account?
- Do the configured PSA stage/type/status values still exist?
- Does `Rev_io_ID__c` exist on the Opportunity object?

### Authentication Errors

Check:

- Salesforce username, password, and security token are correct.
- Salesforce password was not recently changed without updating the token.
- The Salesforce integration user is active.
- The user has API access.
- The customer is using the correct production or sandbox instance URL.

For PSA authentication issues, confirm with Rev.io that the PSA connection has been provisioned correctly in the customer's integration instance.

### Duplicate Customers or Opportunities

Check:

- Was `Rev_io_ID__c` manually cleared in Salesforce?
- Were records manually created in PSA before the first sync?
- Was a sandbox copied or refreshed with stale IDs?
- Did a previous sync fail after creating a PSA record but before writing the ID back to Salesforce?

Do not manually delete records until Rev.io reviews the linked IDs and sync logs.

---

## 10. Go-Live Checklist

- Salesforce fields created with exact API names
- Field-level security granted to the integration user
- Salesforce connection tested successfully
- PSA connection provisioned by Rev.io
- Account Type Filter confirmed
- Opportunity trigger stage confirmed
- Opportunity mappings reviewed
- Debug Mode off for production
- Validation test plan completed
- Support owner identified
- Credential rotation owner identified

---

## 11. Support Handoff Notes

When escalating an issue, include:

- Customer name
- Salesforce org type: sandbox or production
- Salesforce Account, Contact, or Opportunity record URL
- Rev.io PSA Customer, Contact, or Opportunity ID if known
- Approximate time the sync was expected to run
- Screenshot or copy of the integration error if available
- Whether the issue affects one record or many records

Support should avoid asking customers for PSA API credentials unless Rev.io has confirmed that this customer's integration instance was not provisioned correctly.

