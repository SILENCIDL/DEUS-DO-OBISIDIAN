import { App, Editor, Notice, TFile } from "obsidian";

export interface ContextPayload {
  selectedText: string;
  activeFile: string;
  backlinks: string[];
  outlinks: string[];
  tags: string[];
}

function getSelection(editor: Editor): string | null {
  const sel = editor.getSelection();
  if (!sel.trim()) {
    new Notice("Absolute Expander: selecione um texto antes de expandir.");
    return null;
  }
  return sel;
}

// Itera resolvedLinks uma única vez para evitar O(n²) em vaults grandes.
// resolvedLinks[source][target] = count — precisamos da direção inversa.
function getBacklinks(app: App, file: TFile): string[] {
  const resolved = app.metadataCache.resolvedLinks;
  const target = file.path;
  const backlinks: string[] = [];

  for (const [sourcePath, links] of Object.entries(resolved)) {
    if (sourcePath !== target && target in links) {
      backlinks.push(sourcePath);
    }
  }

  return backlinks;
}

function getOutlinks(app: App, file: TFile): string[] {
  const links = app.metadataCache.resolvedLinks[file.path];
  return links ? Object.keys(links) : [];
}

function getTags(app: App, file: TFile): string[] {
  const cache = app.metadataCache.getFileCache(file);
  if (!cache) return [];

  const inlineTags = cache.tags?.map((t) => t.tag) ?? [];

  const raw = cache.frontmatter?.["tags"];
  const frontmatterTags: string[] = Array.isArray(raw)
    ? (raw as unknown[]).map(String)
    : typeof raw === "string"
    ? [raw]
    : [];

  return [...new Set([...inlineTags, ...frontmatterTags])];
}

export function buildContext(
  app: App,
  editor: Editor,
  file: TFile
): ContextPayload | null {
  const selectedText = getSelection(editor);
  if (!selectedText) return null;

  return {
    selectedText,
    activeFile: file.path,
    backlinks: getBacklinks(app, file),
    outlinks: getOutlinks(app, file),
    tags: getTags(app, file),
  };
}
