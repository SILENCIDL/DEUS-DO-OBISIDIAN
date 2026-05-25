import { App, PluginSettingTab, Setting } from "obsidian";
import type AbsoluteExpanderPlugin from "./main";

export interface AbsoluteExpanderSettings {
  claudeApiKey: string;
  geminiApiKey: string;
  activeModel: "claude" | "gemini";
}

export const DEFAULT_SETTINGS: AbsoluteExpanderSettings = {
  claudeApiKey: "",
  geminiApiKey: "",
  activeModel: "claude",
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
          .setValue(this.plugin.settings.activeModel)
          .onChange(async (value) => {
            this.plugin.settings.activeModel = value as "claude" | "gemini";
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
  }
}
