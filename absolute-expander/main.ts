import { MarkdownView, Notice, Plugin } from "obsidian";
import { buildContext } from "./ContextBuilder";
import { generateExpansions } from "./AIBridge";
import { ExpansionModal } from "./ExpansionModal";
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

    // -----------------------------------------------------------------------
    // Comando: inspecionar contexto da nota (debug / diagnóstico)
    // -----------------------------------------------------------------------
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

    // -----------------------------------------------------------------------
    // Comando principal: expandir texto selecionado via IA
    // -----------------------------------------------------------------------
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

        // Notice persistente (timeout 0) — fechado manualmente após resposta.
        const loadingNotice = new Notice("⏳ Analisando contexto absoluto…", 0);

        try {
          const variations = await generateExpansions(payload, this.settings);

          loadingNotice.hide();

          if (!variations.length) return; // AIBridge já exibiu o erro

          const hasContent = variations.some((v) => v.trim().length > 0);
          if (!hasContent) {
            new Notice(
              "Absolute Expander: a IA não retornou variações válidas. Tente novamente."
            );
            return;
          }

          new ExpansionModal(this.app, editor, variations).open();
        } catch {
          loadingNotice.hide();
          // erros já tratados pelo AIBridge; nenhuma ação adicional necessária
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
