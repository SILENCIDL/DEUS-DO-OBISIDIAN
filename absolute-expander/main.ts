import { MarkdownView, Notice, Plugin } from "obsidian";
import { buildContext } from "./ContextBuilder";
import { generateExpansions } from "./AIBridge";
import {
  AbsoluteExpanderSettings,
  AbsoluteExpanderSettingTab,
  DEFAULT_SETTINGS,
} from "./Settings";

export default class AbsoluteExpanderPlugin extends Plugin {
  settings!: AbsoluteExpanderSettings;

  override async onload(): Promise<void> {
    await this.loadSettings();
    this.addSettingTab(new AbsoluteExpanderSettingTab(this.app, this));

    this.addCommand({
      id: "construir-contexto",
      name: "Construir Contexto da Nota Ativa",
      editorCallback: (editor, view) => {
        if (!(view instanceof MarkdownView) || !view.file) {
          new Notice("Absolute Expander: abra uma nota Markdown primeiro.");
          return;
        }
        const payload = buildContext(this.app, editor, view.file);
        if (!payload) return;

        new Notice(
          `Contexto capturado: ${payload.backlinks.length} backlinks · ` +
            `${payload.outlinks.length} outlinks · ${payload.tags.length} tags`
        );
        console.debug("[AbsoluteExpander] ContextPayload:", payload);
      },
    });

    this.addCommand({
      id: "expandir-texto",
      name: "Expandir Texto Selecionado",
      editorCallback: async (editor, view) => {
        if (!(view instanceof MarkdownView) || !view.file) {
          new Notice("Absolute Expander: abra uma nota Markdown primeiro.");
          return;
        }
        const payload = buildContext(this.app, editor, view.file);
        if (!payload) return;

        new Notice("Absolute Expander: gerando expansões…");
        const variations = await generateExpansions(payload, this.settings);

        if (variations.length > 0) {
          console.log("[AbsoluteExpander] Variações geradas:", variations);
          variations.forEach((v, i) => {
            const labels = ["TÉCNICA", "CRIATIVA", "SINTÉTICA"];
            console.log(`[AbsoluteExpander] ${labels[i]}:`, v);
          });
          new Notice(
            `Absolute Expander: ${variations.filter(Boolean).length} variações prontas — veja o console (Ctrl+Shift+I).`
          );
        }
      },
    });
  }

  override onunload(): void {}

  async loadSettings(): Promise<void> {
    this.settings = Object.assign(
      {},
      DEFAULT_SETTINGS,
      (await this.loadData()) as Partial<AbsoluteExpanderSettings>
    );
  }

  async saveSettings(): Promise<void> {
    await this.saveData(this.settings);
  }
}
