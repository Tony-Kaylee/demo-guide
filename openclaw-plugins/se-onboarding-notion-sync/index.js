import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const routePath = "/plugins/se-onboarding/notion-sync";
const notionVersion = "2022-06-28";
const statusOptions = new Set(["Not Started", "In Progress", "Approved"]);
const defaultAllowedOrigins = [
  "https://tony-kaylee.github.io",
  "https://kaylee-revio.msappproxy.net",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
  "http://localhost:8080",
  "http://127.0.0.1:8080"
];

const databaseIds = {
  access: process.env.NOTION_ACCESS_DATABASE_ID || "381a59b7-e7b2-819f-94c1-e90421d414a8",
  callReview: process.env.NOTION_CALL_REVIEW_DATABASE_ID || "381a59b7-e7b2-8158-bdfa-fe3ceb27f0c6",
  scorecard: process.env.NOTION_SCORECARD_DATABASE_ID || "381a59b7-e7b2-8100-8650-f5cfa1f3d9bc",
  rubric: process.env.NOTION_RUBRIC_DATABASE_ID || "381a59b7-e7b2-81f1-94c9-f3d98bafe6ca"
};

function allowedOrigins() {
  return (process.env.SE_ONBOARDING_SYNC_ALLOWED_ORIGINS || defaultAllowedOrigins.join(","))
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);
}

function notionToken() {
  return (process.env.NOTION_TOKEN || process.env.NOTION_API_KEY || "").trim();
}

function readBody(req, maxBytes = 1024 * 1024) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (chunk) => {
      size += chunk.length;
      if (size > maxBytes) {
        reject(new Error("Request body is too large."));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function sendJson(res, statusCode, body, origin = null) {
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Vary", "Origin");
  if (origin) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Credentials", "true");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, x-openclaw-webhook-secret, x-se-onboarding-dry-run");
  }
  if (statusCode === 204) {
    res.end();
    return;
  }
  res.end(JSON.stringify(body));
}

function secretMatches(req) {
  const expected = (process.env.SE_ONBOARDING_SYNC_SECRET || "").trim();
  if (!expected) return true;
  const auth = String(req.headers.authorization || "");
  const bearer = auth.toLowerCase().startsWith("bearer ") ? auth.slice(7).trim() : "";
  const headerSecret = String(req.headers["x-openclaw-webhook-secret"] || "").trim();
  return bearer === expected || headerSecret === expected;
}

function text(value) {
  return { rich_text: value ? [{ text: { content: String(value) } }] : [] };
}

function title(value) {
  return { title: [{ text: { content: String(value) } }] };
}

function date(value) {
  return { date: value ? { start: value } : null };
}

function select(value) {
  return { select: value ? { name: String(value) } : null };
}

function list(value, label) {
  if (value == null) return [];
  if (!Array.isArray(value)) throw new Error(`${label} must be a list.`);
  return value;
}

function object(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label} must be an object.`);
  return value;
}

function iso(value) {
  const raw = String(value || "").trim();
  if (!raw) return null;
  return raw.endsWith("Z") ? `${raw.slice(0, -1)}+00:00` : raw;
}

function isoDate(value) {
  const normalized = iso(value);
  return normalized ? normalized.slice(0, 10) : "";
}

function validDate(value, label) {
  const raw = String(value || "").trim();
  if (raw && !/^\d{4}-\d{2}-\d{2}$/.test(raw)) throw new Error(`${label} must use YYYY-MM-DD.`);
  return raw;
}

function validPageId(value, label) {
  const raw = String(value || "").trim();
  if (!/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i.test(raw)) {
    throw new Error(`${label} has an invalid Notion page ID.`);
  }
  return raw;
}

async function notion(path, body = null, method = "POST") {
  const token = notionToken();
  if (!token) throw new Error("Notion token is not configured on the server.");
  const response = await fetch(`https://api.notion.com/v1${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      "Notion-Version": notionVersion,
      "Content-Type": "application/json"
    },
    body: body == null ? undefined : JSON.stringify(body)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(`Notion API error ${response.status}: ${data.message || response.statusText}`);
  return data;
}

async function findPageByTitle(databaseId, pageTitle) {
  const result = await notion(`/databases/${databaseId}/query`, {
    filter: { property: "Name", title: { equals: pageTitle } },
    page_size: 1
  });
  return result.results?.[0]?.id || null;
}

async function patchPage(pageId, properties, dryRun, counters) {
  if (dryRun) {
    counters.plannedUpdates += 1;
    return;
  }
  await notion(`/pages/${pageId}`, { properties }, "PATCH");
  counters.updated += 1;
}

async function createPage(databaseId, properties, dryRun, counters) {
  if (dryRun) {
    counters.plannedCreates += 1;
    return;
  }
  await notion("/pages", { parent: { database_id: databaseId }, properties });
  counters.created += 1;
}

async function upsert(databaseId, pageTitle, properties, dryRun, counters) {
  const pageId = await findPageByTitle(databaseId, pageTitle);
  if (pageId) await patchPage(pageId, properties, dryRun, counters);
  else await createPage(databaseId, properties, dryRun, counters);
}

async function syncMilestones(payload, employee, dryRun, counters) {
  const updates = new Map();
  for (const item of list(payload.milestonePlan, "milestonePlan")) {
    const row = object(item, "milestonePlan row");
    const rowTitle = String(row.title || row.key || "Milestone").trim();
    const pageId = validPageId(row.pageId, rowTitle);
    const status = String(row.status || "").trim();
    if (status && !statusOptions.has(status)) throw new Error(`Unsupported status for ${rowTitle}: ${status}`);
    updates.set(pageId, {
      title: rowTitle,
      employee: String(row.employee || employee).trim(),
      dueDate: validDate(row.dueDate, `${rowTitle} dueDate`),
      status
    });
  }
  for (const item of list(payload.milestoneStatusChanges, "milestoneStatusChanges")) {
    const row = object(item, "milestoneStatusChanges row");
    const rowTitle = String(row.title || "Milestone").trim();
    const pageId = validPageId(row.pageId, rowTitle);
    const status = String(row.to || "").trim();
    if (!statusOptions.has(status)) throw new Error(`Unsupported status for ${rowTitle}: ${status}`);
    const update = updates.get(pageId) || { title: rowTitle };
    update.status = status;
    if (row.employee) update.employee = String(row.employee).trim();
    if (row.dueDate) update.dueDate = validDate(row.dueDate, `${rowTitle} dueDate`);
    updates.set(pageId, update);
  }
  for (const [pageId, update] of updates.entries()) {
    const properties = {};
    if (update.status) {
      properties.Status = select(update.status);
      properties["Tony Approval"] = { checkbox: update.status === "Approved" };
    }
    if ("employee" in update) properties.Employee = text(update.employee || "");
    if ("dueDate" in update) properties["Due Date"] = date(update.dueDate || null);
    if (Object.keys(properties).length) await patchPage(pageId, properties, dryRun, counters);
  }
}

async function syncAccess(payload, employee, startDate, generatedAt, dryRun, counters) {
  for (const item of list(payload.accessVerification, "accessVerification")) {
    const row = object(item, "accessVerification row");
    const group = String(row.group || "").trim();
    const accessItem = String(row.item || "").trim();
    if (!employee || !group || !accessItem) throw new Error("Access rows require employee, group, and item.");
    const pageTitle = `${employee} - ${accessItem}`;
    await upsert(databaseIds.access, pageTitle, {
      Name: title(pageTitle),
      Employee: text(employee),
      Group: select(group),
      Item: text(accessItem),
      Verified: { checkbox: Boolean(row.verified) },
      "Start Date": date(startDate || null),
      "Generated At": date(generatedAt),
      Source: text(payload.source || "")
    }, dryRun, counters);
  }
}

async function syncCallReview(payload, employee, generatedAt, dryRun, counters) {
  if (!payload.callReview) return;
  const review = object(payload.callReview, "callReview");
  const reviewedAt = iso(review.reviewedAt) || generatedAt;
  const reviewedDate = isoDate(reviewedAt) || "undated";
  const callType = String(review.callType || "").trim();
  const reviewScope = String(review.reviewScope || "").trim();
  const reviewTitle = `${employee} - ${callType || "Call Review"} - ${reviewedDate}`;
  await upsert(databaseIds.callReview, reviewTitle, {
    Name: title(reviewTitle),
    Employee: text(employee),
    "Generated At": date(generatedAt),
    "Reviewed At": date(reviewedAt),
    "Call Type": select(callType || null),
    "Review Scope": select(reviewScope || null),
    "Evidence URL": { url: String(review.evidenceUrl || "").trim() || null },
    "Reviewer Notes": text(review.reviewerNotes || ""),
    "Transcript Characters": { number: Number(review.transcriptCharacters || 0) },
    "Average Score": { number: Number(review.averageScore || 0) },
    "Coaching Focus": { multi_select: list(review.coachingFocus, "coachingFocus").filter(Boolean).map((name) => ({ name: String(name) })) }
  }, dryRun, counters);

  for (const score of list(review.scores, "scores")) {
    const row = object(score, "score row");
    const area = String(row.name || "").trim();
    if (!area) throw new Error("Rubric score rows require a name.");
    const pageTitle = `${employee} - ${area} - ${reviewedDate}`;
    await upsert(databaseIds.rubric, pageTitle, {
      Name: title(pageTitle),
      Employee: text(employee),
      "Generated At": date(generatedAt),
      "Reviewed At": date(reviewedAt),
      "Call Type": select(callType || null),
      "Review Scope": select(reviewScope || null),
      "Rubric Area": text(area),
      Score: { number: Number(row.score || 0) },
      Hits: text(list(row.hits, "hits").join(", ")),
      "Missing Signals": text(list(row.missingSignals, "missingSignals").join(", "))
    }, dryRun, counters);
  }

  for (const segment of list(review.segmentReviews, "segmentReviews")) {
    const row = object(segment, "segmentReview row");
    const name = String(row.name || "").trim();
    const step = Number(row.step || 0);
    if (!name || step <= 0) throw new Error("Scorecard rows require name and step.");
    const pageTitle = `${employee} - ${step}. ${name}`;
    await upsert(databaseIds.scorecard, pageTitle, {
      Name: title(pageTitle),
      Employee: text(employee),
      "Generated At": date(generatedAt),
      "Reviewed At": date(reviewedAt),
      "Review Scope": select(reviewScope || null),
      "Segment Key": text(row.key || ""),
      Type: select(String(row.type || "").trim() || null),
      Step: { number: step },
      Description: text(row.description || ""),
      "Initial Score": { number: Number(row.initialScore || 0) },
      "Initial Notes": text(row.initialNotes || ""),
      "Final Score": { number: row.finalScore == null || row.finalScore === "" ? null : Number(row.finalScore) },
      "Final Notes": text(row.finalNotes || ""),
      Approved: { checkbox: Boolean(row.approved) }
    }, dryRun, counters);
  }
}

async function syncPayload(payload, dryRun) {
  if (payload.source !== "SE Onboarding Dashboard") throw new Error("Invalid payload source.");
  const onboardingProfile = object(payload.onboardingProfile || {}, "onboardingProfile");
  const employee = String(onboardingProfile.rep || payload.callReview?.rep || "").trim();
  if (!employee) throw new Error("Employee/rep is required before syncing to Notion.");
  const startDate = validDate(onboardingProfile.startDate, "startDate");
  const generatedAt = iso(payload.generatedAt);
  const counters = { plannedUpdates: 0, plannedCreates: 0, updated: 0, created: 0 };
  await syncMilestones(payload, employee, dryRun, counters);
  await syncAccess(payload, employee, startDate, generatedAt, dryRun, counters);
  await syncCallReview(payload, employee, generatedAt, dryRun, counters);
  return {
    ok: true,
    dryRun,
    employee,
    total: counters.plannedUpdates + counters.plannedCreates + counters.updated + counters.created,
    planned_updates: counters.plannedUpdates,
    planned_creates: counters.plannedCreates,
    updated: counters.updated,
    created: counters.created
  };
}

async function handleSync(req, res) {
  const origin = String(req.headers.origin || "");
  const allowed = allowedOrigins();
  const originAllowed = !origin || allowed.includes(origin);

  if (req.method === "OPTIONS") {
    sendJson(res, originAllowed ? 204 : 403, originAllowed ? {} : { ok: false, error: "Origin is not allowed." }, originAllowed ? origin || allowed[0] : null);
    return true;
  }
  if (req.method !== "POST") {
    sendJson(res, 405, { ok: false, error: "Use POST." }, originAllowed ? origin : null);
    return true;
  }
  if (!originAllowed) {
    sendJson(res, 403, { ok: false, error: "Origin is not allowed." });
    return true;
  }
  if (!secretMatches(req)) {
    sendJson(res, 401, { ok: false, error: "Sync secret is invalid." }, origin);
    return true;
  }

  try {
    const payload = JSON.parse(await readBody(req));
    const dryRun = String(req.headers["x-se-onboarding-dry-run"] || "").toLowerCase() === "true";
    const result = await syncPayload(payload, dryRun);
    sendJson(res, 200, result, origin);
  } catch (error) {
    sendJson(res, 400, { ok: false, error: String(error?.message || error) }, origin);
  }
  return true;
}

export default definePluginEntry({
  id: "se-onboarding-notion-sync",
  name: "SE Onboarding Notion Sync",
  description: "Accepts SE onboarding dashboard payloads and syncs them to Notion server-side.",
  register(api) {
    api.registerHttpRoute({
      path: routePath,
      auth: "plugin",
      handler: handleSync
    });
  }
});
