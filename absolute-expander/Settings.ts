import { App, PluginSettingTab, Setting } from "obsidian";
import type AbsoluteExpanderPlugin from "./main";

export interface AbsoluteExpanderSettings {
  claudeApiKey: string;
  geminiApiKey: string;
  kimiApiKey: string;
  activeModel: "claude" | "gemini" | "kimi";
  maxDepth: number;
  maxSubthemes: number;
  autoInsert: boolean;
}

export const DEFAULT_SETTINGS: AbsoluteExpanderSettings = {
  claudeApiKey: "",
  geminiApiKey: "",
  kimiApiKey: "",
  activeModel: "claude",
  maxDepth: 15,
  maxSubthemes: 30,
  autoInsert: true,
};

export class AbsoluteExpanderSettingTab extends PluginSettingTab {
  constructor(app: App, private plugin: AbsoluteExpanderPlugin) {
    super(app, plugin);
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Absolute Expander" });

    new Setting(containerEl)
      .setName("Modelo ativo")
      .setDesc("LLM usada para expandir os textos selecionados.")
      .addDropdown((dd) =>
        dd
          .addOption("claude", "Claude (Anthropic)")
          .addOption("gemini", "Gemini (Google)")
          .addOption("kimi", "KimiAI (Moonshot)")
          .setValue(this.plugin.settings.activeModel)
          .onChange(async (value) => {
            this.plugin.settings.activeModel = value as "claude" | "gemini" | "kimi";
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Inserção Automática")
      .setDesc("Se ativado, o plugin insere o conteúdo diretamente na nota sem abrir o modal.")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.autoInsert)
          .onChange(async (value) => {
            this.plugin.settings.autoInsert = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Profundidade Máxima")
      .setDesc("Nível máximo de recursão (Temas -> Subtemas).")
      .addText((text) =>
        text
          .setValue(String(this.plugin.settings.maxDepth))
          .onChange(async (value) => {
            this.plugin.settings.maxDepth = Number(value) || 15;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Máximo de Subtemas")
      .setDesc("Número máximo de subtemas gerados por nível.")
      .addText((text) =>
        text
          .setValue(String(this.plugin.settings.maxSubthemes))
          .onChange(async (value) => {
            this.plugin.settings.maxSubthemes = Number(value) || 30;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Claude API Key")
      .setDesc("Obtenha em console.anthropic.com → API Keys.")
      .addText((text) => {
        text
          .setPlaceholder("sk-ant-...")
          .setValue(this.plugin.settings.claudeApiKey)
          .onChange(async (value) => {
            this.plugin.settings.claudeApiKey = value.trim();
            await this.plugin.saveSettings();
          });
        text.inputEl.setAttribute("type", "password");
        text.inputEl.style.width = "100%";
      });

    new Setting(containerEl)
      .setName("Gemini API Key")
      .setDesc("Obtenha em aistudio.google.com → Get API Key.")
      .addText((text) => {
        text
          .setPlaceholder("AIza...")
          .setValue(this.plugin.settings.geminiApiKey)
          .onChange(async (value) => {
            this.plugin.settings.geminiApiKey = value.trim();
            await this.plugin.saveSettings();
          });
        text.inputEl.setAttribute("type", "password");
        text.inputEl.style.width = "100%";
      });

    new Setting(containerEl)
      .setName("KimiAI API Key")
      .setDesc("Obtenha em platform.moonshot.cn.")
      .addText((text) => {
        text
          .setPlaceholder("sk-...")
          .setValue(this.plugin.settings.kimiApiKey)
          .onChange(async (value) => {
            this.plugin.settings.kimiApiKey = value.trim();
            await this.plugin.saveSettings();
          });
        text.inputEl.setAttribute("type", "password");
        text.inputEl.style.width = "100%";
      });
  }
}
