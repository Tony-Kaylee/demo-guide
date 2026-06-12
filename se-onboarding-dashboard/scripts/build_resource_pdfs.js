const fs = require("fs");
const path = require("path");
const PDFDocument = require("pdfkit");

const root = path.resolve(__dirname, "..");
const sourcePath = path.join(root, "resources", "revio-psa-se-onboarding-plan.md");
const outDir = path.join(root, "resources", "pdfs");
const source = fs.readFileSync(sourcePath, "utf8");

const colors = {
  ink: "#162033",
  muted: "#5f6f87",
  brand: "#0f3b66",
  accent: "#0f766e",
  rule: "#dce4ef",
  panel: "#f5f8fc",
  white: "#ffffff"
};

const page = {
  left: 54,
  right: 54,
  contentWidth: 504
};

const docs = [
  {
    file: "se-onboarding-full-plan.pdf",
    title: "Rev.io PSA SE Onboarding Plan",
    subtitle: "60-day ramp, approval gates, demo path, product depth, buyer scenarios, and certification",
    sections: [source]
  },
  {
    file: "se-onboarding-core-demo-path.pdf",
    title: "Core Demo Path",
    subtitle: "Primary quote-to-cash story, talk track, practice path, and Revii moments",
    sections: [
      extract("### Days 15-21 - Guided Click Path", "### Days 22-30 - Core Demo Repetition"),
      extract("### Days 22-30 - Core Demo Repetition", "### Days 31-38 - Operational Deep Dives"),
      extract("## Standard End-to-End Demo Talk Track", "## Revii Usage Guide"),
      extract("## Revii Usage Guide", "## Known Positioning Notes")
    ]
  },
  {
    file: "se-onboarding-product-depth-topics.pdf",
    title: "Product Depth Topics",
    subtitle: "Module-level prep for product confidence and second-half ramp depth",
    sections: [
      extract("## Deep Dive Tracks", "## Buyer-Specific Scenario Tracks"),
      extract("## Known Positioning Notes", "## Final Capstone")
    ]
  },
  {
    file: "se-onboarding-buyer-scenarios.pdf",
    title: "Buyer Scenarios",
    subtitle: "Vertical branches, discovery emphasis, likely questions, and practice expectations",
    sections: [
      extract("### Days 47-54 - Buyer Scenarios and Discovery Branching", "### Days 55-60 - Certification and Lead-Demo Approval"),
      extract("## Buyer-Specific Scenario Tracks", "## Standard End-to-End Demo Talk Track")
    ]
  },
  {
    file: "se-onboarding-certification-prep.pdf",
    title: "Certification Prep",
    subtitle: "Final approval requirements, scoring rubric, capstone prompt, and pass standard",
    sections: [
      extract("### Days 55-60 - Certification and Lead-Demo Approval", "## Deep Dive Tracks"),
      extract("## Final Capstone", null)
    ]
  }
];

fs.mkdirSync(outDir, { recursive: true });
docs.forEach(buildPdf);

function extract(start, end) {
  const startIndex = source.indexOf(start);
  if (startIndex === -1) {
    throw new Error(`Missing section start: ${start}`);
  }
  const endIndex = end ? source.indexOf(end, startIndex + start.length) : source.length;
  if (end && endIndex === -1) {
    throw new Error(`Missing section end: ${end}`);
  }
  return source.slice(startIndex, endIndex).trim();
}

function buildPdf(config) {
  const doc = new PDFDocument({
    size: "LETTER",
    margins: { top: 54, bottom: 54, left: 54, right: 54 },
    info: {
      Title: config.title,
      Author: "Rev.io Solutions Engineering"
    }
  });
  const output = path.join(outDir, config.file);
  doc.pipe(fs.createWriteStream(output));

  cover(doc, config);
  config.sections.join("\n\n").split(/\r?\n/).forEach(line => renderLine(doc, line));
  footer(doc);
  doc.end();
  console.log(`Wrote ${path.relative(process.cwd(), output)}`);
}

function cover(doc, config) {
  doc.rect(0, 0, doc.page.width, 118).fill(colors.brand);
  doc.fillColor(colors.white).font("Helvetica-Bold").fontSize(22).text(config.title, 54, 38, {
    width: doc.page.width - 108
  });
  doc.font("Helvetica").fontSize(10).fillColor("#d7e6f8").text(config.subtitle, 54, 72, {
    width: doc.page.width - 108,
    lineGap: 2
  });
  doc.y = 148;
}

function footer(doc) {
  const range = doc.bufferedPageRange();
  for (let i = range.start; i < range.start + range.count; i += 1) {
    doc.switchToPage(i);
    doc.font("Helvetica").fontSize(8).fillColor(colors.muted).text(
      `Rev.io PSA SE Onboarding - ${i + 1}`,
      54,
      doc.page.height - 38,
      { width: doc.page.width - 108, align: "right" }
    );
  }
}

function renderLine(doc, rawLine) {
  const line = rawLine.trim();
  doc.x = page.left;
  if (!line) {
    doc.moveDown(0.35);
    return;
  }
  ensureSpace(doc, 34);

  if (line.startsWith("# ")) {
    heading(doc, line.slice(2), 19);
  } else if (line.startsWith("## ")) {
    heading(doc, line.slice(3), 15, true);
  } else if (line.startsWith("### ")) {
    heading(doc, line.slice(4), 13);
  } else if (line.startsWith("#### ")) {
    heading(doc, line.slice(5), 11);
  } else if (/^\d+\.\s/.test(line)) {
    paragraph(doc, line, { indent: 16, continued: false });
  } else if (line.startsWith("- ")) {
    bullet(doc, line.slice(2));
  } else if (line.endsWith(":") && line.length < 80) {
    label(doc, line);
  } else {
    paragraph(doc, line);
  }
}

function heading(doc, text, size, rule = false) {
  doc.moveDown(0.5);
  doc.font("Helvetica-Bold").fontSize(size).fillColor(colors.brand).text(text, page.left, doc.y, {
    width: page.contentWidth,
    lineGap: 2
  });
  if (rule) {
    const y = doc.y + 5;
    doc.moveTo(page.left, y).lineTo(doc.page.width - page.right, y).strokeColor(colors.rule).lineWidth(0.7).stroke();
    doc.y = y + 8;
  }
}

function label(doc, text) {
  doc.moveDown(0.15);
  doc.font("Helvetica-Bold").fontSize(10).fillColor(colors.accent).text(text, page.left, doc.y, {
    width: page.contentWidth,
    lineGap: 2
  });
}

function paragraph(doc, text, options = {}) {
  doc.font("Helvetica").fontSize(10).fillColor(colors.ink).text(text, page.left, doc.y, {
    width: page.contentWidth,
    lineGap: 3,
    ...options
  });
}

function bullet(doc, text) {
  const x = page.left;
  const y = doc.y;
  doc.circle(x + 3, y + 6, 2).fill(colors.accent);
  doc.font("Helvetica").fontSize(10).fillColor(colors.ink).text(text, x + 14, y, {
    width: page.contentWidth - 14,
    lineGap: 3
  });
  doc.x = page.left;
}

function ensureSpace(doc, height) {
  if (doc.y + height > doc.page.height - 62) {
    doc.addPage();
  }
}
