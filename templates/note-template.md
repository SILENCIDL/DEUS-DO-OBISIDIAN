---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
modified: <% tp.date.now("YYYY-MM-DD") %>
type: note
status: draft
tags: []
aliases: []
---

# <% tp.file.title %>

## Context

> Brief context or motivation for this note.

## Content

## Related

<%*
// Use MetadataCache to find connected notes at template render time
const resolvedLinks = app.metadataCache.resolvedLinks;
const unresolvedLinks = app.metadataCache.unresolvedLinks;

// Build backlink candidates from nearby notes
const currentPath = tp.file.path(true);
const connected = [];

for (const [sourcePath, targets] of Object.entries(resolvedLinks)) {
  if (targets[currentPath] !== undefined) {
    connected.push(`[[${sourcePath}]]`);
  }
}

if (connected.length > 0) {
  tR += connected.map(l => `- ${l}`).join("\n");
} else {
  tR += "_No connected notes yet._";
}
%>

## References

