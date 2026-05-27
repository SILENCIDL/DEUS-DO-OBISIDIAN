import { MarkdownView, Notice, Plugin, TFile } from "obsidian";
import { buildContext } from "./ContextBuilder";
import { generateRecursiveExpansions } from "./AIBridge";
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
      id: "expansao-recursiva",
      name: "Executar Expansão Recursiva (Temas -> Subtemas)",
      editorCallback: async (editor, view) => {
        if (!(view instanceof MarkdownView) || !view.file) return;
        
        await this.runRecursiveExpansion(view.file, 0);
      },
    });
  }

  async runRecursiveExpansion(file: TFile, depth: number) {
    if (depth >= this.settings.maxDepth) {
      new Notice(`Profundidade máxima atingida (${depth})`);
      return;
    }

    new Notice(`Expandindo: ${file.basename} (Nível ${depth})`);

    // Simulando o editor para notas que podem não estar abertas
    const content = await this.app.vault.read(file);
    const payload = {
        selectedText: content || "Tema vazio",
        activeFile: file.path,
        backlinks: [],
        outlinks: [],
        tags: []
    };

    const { raw, subthemes } = await generateRecursiveExpansions(payload, this.settings);
    
    if (!raw) return;

    // 1. Atualiza a nota atual com os subtemas
    await this.app.vault.append(file, "\n\n## Subtemas Gerados\n" + raw);

    // 2. Cria novas notas para cada subtema e expande recursivamente
    for (const sub of subthemes.slice(0, this.settings.maxSubthemes)) {
        const path = `${sub}.md`;
        let subFile = this.app.vault.getAbstractFileByPath(path);
        
        if (!subFile) {
            try {
                subFile = await this.app.vault.create(path, `# ${sub}\n\nOrigem: [[${file.basename}]]`);
            } catch (e) {
                console.error(`Erro ao criar nota ${sub}:`, e);
                continue;
            }
        }

        if (subFile instanceof TFile) {
            // Chamada recursiva para o próximo nível
            await this.runRecursiveExpansion(subFile, depth + 1);
        }
    }
  }

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
