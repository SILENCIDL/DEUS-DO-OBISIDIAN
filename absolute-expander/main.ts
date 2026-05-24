// main.ts — Absolute Expander — Fase 1: Esqueleto e Fundação
import { Notice, Plugin } from "obsidian";

export default class AbsoluteExpanderPlugin extends Plugin {
  override async onload(): Promise<void> {
    this.addCommand({
      id: "testar-expansao",
      name: "Testar Expansão",
      callback: () => {
        new Notice("Absolute Expander ativado e pronto para evoluir!");
      },
    });
  }

  override onunload(): void {
    // cleanup será adicionado nas fases seguintes
  }
}
