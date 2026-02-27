/**
 * orphan-detector.js
 * Centralised DataviewJS module: detects notes with no incoming links.
 *
 * Usage inside any note:
 *   ```dataviewjs
 *   await dv.view("scripts/dataview/orphan-detector", { folder: "notes" })
 *   ```
 *
 * @param {object} args - Optional arguments passed via dv.view()
 * @param {string} [args.folder] - Restrict search to a specific folder
 */

const folder = input?.folder ?? "";

// Gather every note that exists in the vault (or a sub-folder)
const allPages = folder
  ? dv.pages(`"${folder}"`)
  : dv.pages();

// Build a set of all files that appear as a resolved link target
const linkedFiles = new Set();
for (const page of allPages) {
  const resolvedLinks =
    app.metadataCache.resolvedLinks[page.file.path] ?? {};
  for (const target of Object.keys(resolvedLinks)) {
    linkedFiles.add(target);
  }
}

// Orphans = notes that never appear as a link target
const orphans = allPages.filter(
  (p) => !linkedFiles.has(p.file.path)
);

if (orphans.length === 0) {
  dv.paragraph("✅ No orphan notes found.");
} else {
  dv.header(3, `🔍 Orphan Notes (${orphans.length})`);
  dv.table(
    ["Note", "Created", "Tags"],
    orphans.map((p) => [
      p.file.link,
      p.file.ctime,
      p.file.tags?.join(", ") ?? "—",
    ])
  );
}
