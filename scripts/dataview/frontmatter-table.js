/**
 * frontmatter-table.js
 * Centralised DataviewJS module: renders a table from YAML frontmatter fields.
 *
 * Usage:
 *   ```dataviewjs
 *   await dv.view("scripts/dataview/frontmatter-table", {
 *     folder: "notes/projects",
 *     fields: ["status", "priority", "due"],
 *     filter: { status: "active" }
 *   })
 *   ```
 *
 * @param {object} args
 * @param {string}   [args.folder=""]        - Vault-relative folder to query
 * @param {string[]} [args.fields=[]]        - Frontmatter keys to display
 * @param {object}   [args.filter={}]        - Key/value pairs to filter by
 */

const folder  = input?.folder  ?? "";
const fields  = input?.fields  ?? [];
const filter  = input?.filter  ?? {};

let pages = folder ? dv.pages(`"${folder}"`) : dv.pages();

// Apply frontmatter filters
for (const [key, value] of Object.entries(filter)) {
  pages = pages.filter((p) => p[key] === value);
}

if (pages.length === 0) {
  dv.paragraph("⚠️ No notes matched the query.");
  return;
}

const headers = ["Note", ...fields];
const rows = pages.map((p) => [
  p.file.link,
  ...fields.map((f) => p[f] ?? "—"),
]);

dv.header(3, `📋 Notes (${pages.length})`);
dv.table(headers, rows);
