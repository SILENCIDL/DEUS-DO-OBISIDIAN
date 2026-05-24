import { MarkdownView, Notice, Plugin } from "obsidian";
import { buildContext } from "./ContextBuilder";

export default class AbsoluteExpanderPlugin extends Plugin {
  override async onload(): Promise<void> {
    this.addCommand({
      id: "testar-expansao",
      name: "Testar Expansão",
      callback: () => {
        new Notice("Absolute Expander ativado e pronto para evoluir!");
      },
    });

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
          `${payload.outlinks.length} outlinks · ` +
          `${payload.tags.length} tags`
        );
        console.debug("[AbsoluteExpander] ContextPayload:", payload);
      },
    });
  }

  override onunload(): void {}
}
