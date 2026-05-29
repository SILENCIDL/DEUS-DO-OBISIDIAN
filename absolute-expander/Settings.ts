import { App, PluginSettingTab, Setting } from "obsidian";
import type AbsoluteExpanderPlugin from "./main";

export interface AbsoluteExpanderSettings {
  claudeApiKey: string;
  geminiApiKey: string;
  activeModel: "claude" | "gemini";
  claudeModel: "claude-sonnet-4-6" | "claude-haiku-4-5-20251001";
}

export const DEFAULT_SETTINGS: AbsoluteExpanderSettings = {
  claudeApiKey: "",
  geminiApiKey: "",
  activeModel: "claude",
  claudeModel: "claude-sonnet-4-6",
};

export class AbsoluteExpanderSettingTab extends PluginSettingTab {
  constructor(app: App, private plugin: AbsoluteExpanderPlugin) {
    super(app, plugin);
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Absolute Expander" });

    // -------------------------------------------------------------------------
    // Modelo ativo (Claude ou Gemini)
    // -------------------------------------------------------------------------
    new Setting(containerEl)
      .setName("Modelo ativo")
      .setDesc("LLM usada para expandir os textos selecionados.")
      .addDropdown((dd) =>
        dd
          .addOption("claude", "Claude (Anthropic)")
          .addOption("gemini", "Gemini 2.0 Flash (Google)")
          .setValue(this.plugin.settings.activeModel)
          .onChange(async (value) => {
            this.plugin.settings.activeModel = value as "claude" | "gemini";
            await this.plugin.saveSettings();
          })
      );

    // -------------------------------------------------------------------------
    // Versão do modelo Claude
    // -------------------------------------------------------------------------
    new Setting(containerEl)
      .setName("Versão Claude")
      .setDesc(
        "Sonnet: melhor qualidade. Haiku: mais rápido e mais barato. " +
        "Só relevante quando o modelo ativo for Claude."
      )
      .addDropdown((dd) =>
        dd
          .addOption("claude-sonnet-4-6", "Claude Sonnet 4.6 (recomendado)")
          .addOption("claude-haiku-4-5-20251001", "Claude Haiku 4.5 (econômico)")
          .setValue(this.plugin.settings.claudeModel)
          .onChange(async (value) => {
            this.plugin.settings.claudeModel = value as AbsoluteExpanderSettings["claudeModel"];
            await this.plugin.saveSettings();
          })
      );

    // -------------------------------------------------------------------------
    // Claude API Key
    // -------------------------------------------------------------------------
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

    // -------------------------------------------------------------------------
    // Gemini API Key
    // -------------------------------------------------------------------------
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
  }
}
