# 🃏 AI Card Generator with HTML/CSS and PDF Output

Create beautiful, data-driven **trading/flash/collectible cards** from natural language prompts using **open-source LLMs**, **Unsplash API**, and **PDF rendering engines**.

---

## 🚀 Project Overview

This project takes a user prompt (like "Make a dragon spell card with purple aura") and generates a print-ready **PDF** of cards using:

1. **Prompt Enhancement** using LLMs
2. **HTML + CSS Generation** for card layout
3. **Unsplash Image Fetching** based on keywords
4. **Card Rendering** using Jinja2 templates
5. **PDF Export** via rendering API (e.g., WeasyPrint or html2pdf.app)

---

## 🧠 Models Used (Open Source Only)

| Stage               | Model                                     | Provider | License           |
| ------------------- | ----------------------------------------- | -------- | ----------------- |
| Prompt Enhancer     | `deepseek-ai/deepseek-coder-33b-instruct` | DeepSeek | Apache 2.0 ✅      |
| Code Generator      | `bigcode/starcoder2-15b`                  | BigCode  | OpenRAIL-M ✅      |
| Alt. Code Generator | `codellama/CodeLlama-34b-Instruct-hf`     | Meta AI  | Non-commercial 🔒 |

All models are accessed via **Hugging Face Inference API** to stay lightweight.

---

## 🌄 Image Generator

* **API**: [Unsplash Developer API](https://unsplash.com/developers)
* **Usage**: Keyword-based image search
* **Input**: Enhanced prompt keywords (e.g., "fire dragon")
* **Output**: Public image URL injected into the card template

---

## 🧰 Project Structure

```bash
cardgen-ai/
├── backend/                  # FastAPI app
│   ├── main.py               # API orchestrator
│   ├── llm_agents.py         # Prompt enhancer + code generator
│   ├── image_fetcher.py      # Unsplash API integration
│   ├── html_builder.py       # Injects data into HTML
│   └── pdf_generator.py      # Converts HTML to PDF
│
├── templates/               # HTML + CSS templates
│   ├── card_template.html    
│   └── style.css             
│
├── data/
│   └── cards.csv             # Dynamic card data
│
├── outputs/
│   └── cards.pdf             # Final PDF result
│
├── .env                     # Stores API keys (Unsplash, HuggingFace)
├── requirements.txt         # Python deps
└── README.md
```

---

## 📦 Dependencies

```txt
fastapi
jinja2
weasyprint
pandas
requests
python-dotenv
```

> You can also optionally use `html2pdf.app` or `pdfshift.io` for PDF generation instead of WeasyPrint.

---

## ⚙️ API Flow

1. User submits a prompt → `/generate`
2. Prompt is enhanced → passed to LLM (HuggingFace API)
3. HTML + CSS template is generated
4. Unsplash API is queried for images → injected into template
5. Final HTML is rendered and exported as PDF
6. PDF is returned/downloaded

---

## 🛡️ Environment Variables (`.env`)

```env
UNSPLASH_ACCESS_KEY=your_key_here
HF_API_TOKEN=your_token_here
```

---

## ✅ Example Prompt

```bash
POST /generate
{
  "prompt": "Create a legendary fire dragon card with purple border and high power."
}
```

🔁 → returns `cards.pdf` with full layout, image, and styling.

---

## 📌 Future Ideas

* 🔄 Auto-translate cards into multiple languages
* 🖼️ Support custom uploaded images
* ✨ Rarity logic with star icons or effects
* 💾 Export as PNGs or SVG as well

---

## 📜 License

MIT License. All models used are open-source or have free usage rights under their respective licenses.
