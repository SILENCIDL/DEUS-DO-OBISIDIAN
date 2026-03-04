/**
 * tag-index.js
 * Centralised DataviewJS module: builds an index of all tags with counts.
 *
 * Usage:
 *   ```dataviewjs
 *   await dv.view("scripts/dataview/tag-index", { sortBy: "count" })
 *   ```
 *
 * @param {object} args
 * @param {"count"|"name"} [args.sortBy="count"] - Sort column
 */

const sortBy = input?.sortBy ?? "count";

// Build tag → [files] map
const tagMap = new Map();

for (const page of dv.pages()) {
  const tags = page.file.tags ?? [];
  for (const tag of tags) {
    if (!tagMap.has(tag)) tagMap.set(tag, []);
    tagMap.get(tag).push(page.file.link);
  }
}

// Convert to rows
let rows = [...tagMap.entries()].map(([tag, files]) => [
  tag,
  files.length,
  files,
]);

if (sortBy === "name") {
  rows.sort((a, b) => a[0].localeCompare(b[0]));
} else {
  rows.sort((a, b) => b[1] - a[1]);
}

dv.header(3, `🏷️ Tag Index (${tagMap.size} tags)`);
dv.table(["Tag", "Count", "Notes"], rows);
