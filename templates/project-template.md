---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
modified: <% tp.date.now("YYYY-MM-DD") %>
type: project
status: planning
priority: medium
due: ""
owner: ""
tags: [project]
aliases: []
---

# <% tp.file.title %>

## Objective

> One-sentence description of the project goal.

## Scope

- **In scope:**
- **Out of scope:**

## Milestones

| Milestone | Due Date | Status |
|-----------|----------|--------|
|           |          | 🔲 todo |

## Notes

```dataviewjs
await dv.view("scripts/dataview/frontmatter-table", {
  folder: "notes/projects",
  fields: ["status", "priority", "due"],
  filter: {}
})
```

## Resources

## Log

- <% tp.date.now("YYYY-MM-DD") %> — Project created.
