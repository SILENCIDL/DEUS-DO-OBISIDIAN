/**
 * capture-macro.js
 * QuickAdd macro: collect structured data from the user and create a note.
 *
 * Registered in QuickAdd → Macros → "New Note Macro".
 * Invoked via: app.plugins.plugins.quickadd.api
 *
 * The macro calls requestInputs() to gather multiple fields silently, then
 * injects them as YAML frontmatter into a new note. A MacroAbortError is
 * thrown (and caught) if the user dismisses any prompt.
 */

module.exports = async (params) => {
  const { quickAddApi: api, app } = params;

  let inputs;

  try {
    // Collect multiple fields in one modal sequence
    inputs = await api.inputPrompt(
      "Note title",
      "Enter the note title",
      ""
    );

    if (!inputs) throw new Error("MacroAbortError");

    const title  = inputs;
    const status = await api.suggester(
      ["draft", "active", "done", "archived"],
      ["draft", "active", "done", "archived"],
      false,
      "Select status"
    ) ?? "draft";

    const tags = await api.inputPrompt(
      "Tags (comma-separated)",
      "e.g. concept, reference",
      ""
    ) ?? "";

    const tagList = tags
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean)
      .map((t) => `"${t}"`)
      .join(", ");

    const today = window.moment().format("YYYY-MM-DD");

    // Build frontmatter-first note content
    const content = `---
title: "${title}"
created: ${today}
modified: ${today}
type: note
status: ${status}
tags: [${tagList}]
aliases: []
---

# ${title}

`;

    // Create the note at an absolute vault path
    const fileName = `notes/inbox/${title}.md`;
    await app.vault.create(fileName, content);

    // Open the newly created note
    const file = app.vault.getAbstractFileByPath(fileName);
    if (file) {
      await app.workspace.getLeaf(false).openFile(file);
    }

    new Notice(`✅ Created: ${title}`);
  } catch (err) {
    // MacroAbortError is expected when the user cancels — handle silently
    if (
      err.message === "MacroAbortError" ||
      err.name === "MacroAbortError"
    ) {
      new Notice("ℹ️ Note creation cancelled.");
      return;
    }
    // Re-throw unexpected errors
    console.error("[capture-macro] Unexpected error:", err);
    new Notice(`❌ Error: ${err.message}`);
  }
};
