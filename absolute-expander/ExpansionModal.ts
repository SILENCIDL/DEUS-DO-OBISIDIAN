import { App, Editor, Modal } from "obsidian";

const CARD_META = [
  {
    label: "TÉCNICA",
    description: "Objetiva · Terminologicamente precisa",
  },
  {
    label: "CRIATIVA",
    description: "Narrativa · Metáforas e síntese pessoal",
  },
  {
    label: "SINTÉTICA",
    description: "Comprimida · Apta para título ou link-âncora",
  },
] as const;

// Fallback seguro caso a IA retorne menos de 3 variações.
const EMPTY_META = {
  label: "VARIAÇÃO",
  description: "Expansão gerada pela IA",
} as const;

export class ExpansionModal extends Modal {
  constructor(
    app: App,
    private readonly editor: Editor,
    private readonly expansions: string[]
  ) {
    super(app);
  }

  onOpen(): void {
    const { contentEl, modalEl } = this;

    modalEl.style.width = "min(92vw, 960px)";
    modalEl.style.maxWidth = "960px";

    contentEl.empty();

    contentEl.createEl("h2", {
      text: "Escolha uma Expansão",
      attr: {
        style: [
          "margin: 0 0 4px 0",
          "font-size: var(--font-ui-large)",
          "color: var(--text-normal)",
        ].join(";"),
      },
    });

    contentEl.createEl("p", {
      text: "Selecione a variação que melhor se encaixa no seu contexto. O texto selecionado será substituído.",
      attr: {
        style: [
          "margin: 0 0 20px 0",
          "font-size: var(--font-ui-small)",
          "color: var(--text-muted)",
        ].join(";"),
      },
    });

    const grid = contentEl.createDiv({
      attr: {
        style: [
          "display: grid",
          "grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))",
          "gap: 16px",
          "align-items: stretch",
        ].join(";"),
      },
    });

    this.expansions.forEach((text, i) => {
      // Bounds-check defensivo: usa EMPTY_META se o índice estiver fora.
      const meta = i < CARD_META.length ? CARD_META[i] : EMPTY_META;
      this.buildCard(grid, text, meta);
    });
  }

  private buildCard(
    parent: HTMLElement,
    text: string,
    meta: typeof CARD_META[number] | typeof EMPTY_META
  ): void {
    const isEmpty = !text.trim();

    const card = parent.createDiv({
      attr: {
        style: [
          "background: var(--background-secondary)",
          "border: 1px solid var(--background-modifier-border)",
          "border-radius: var(--radius-m)",
          "padding: 16px",
          "display: flex",
          "flex-direction: column",
          "gap: 12px",
          isEmpty ? "opacity: 0.5" : "",
        ]
          .filter(Boolean)
          .join(";"),
      },
    });

    const header = card.createDiv({
      attr: { style: "display:flex;flex-direction:column;gap:4px" },
    });

    header.createEl("span", {
      text: meta.label,
      attr: {
        style: [
          "font-size: var(--font-ui-smaller)",
          "font-weight: 700",
          "letter-spacing: 0.08em",
          "color: var(--interactive-accent)",
          "text-transform: uppercase",
        ].join(";"),
      },
    });

    header.createEl("span", {
      text: meta.description,
      attr: {
        style: [
          "font-size: var(--font-ui-smaller)",
          "color: var(--text-faint)",
        ].join(";"),
      },
    });

    card.createEl("p", {
      text: isEmpty ? "(sem resposta — tente novamente)" : text,
      attr: {
        style: [
          "flex: 1",
          "margin: 0",
          "font-size: var(--font-ui-medium)",
          "color: var(--text-normal)",
          "line-height: 1.65",
          "white-space: pre-wrap",
          "word-break: break-word",
        ].join(";"),
      },
    });

    const btn = card.createEl("button", {
      text: "Inserir esta Variação",
      attr: {
        style: [
          "width: 100%",
          "padding: 8px 12px",
          "background: var(--interactive-accent)",
          "color: var(--text-on-accent)",
          "border: none",
          "border-radius: var(--radius-s)",
          "font-size: var(--font-ui-small)",
          "font-weight: 600",
          isEmpty ? "cursor: not-allowed" : "cursor: pointer",
        ].join(";"),
      },
    });

    if (isEmpty) {
      btn.disabled = true;
      return;
    }

    btn.addEventListener("click", () => {
      this.editor.replaceSelection(text);
      this.close();
    });

    btn.addEventListener("mouseenter", () => {
      btn.style.filter = "brightness(1.12)";
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.filter = "";
    });
  }

  onClose(): void {
    this.contentEl.empty();
  }
}
