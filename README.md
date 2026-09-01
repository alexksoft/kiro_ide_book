# Kiro IDE & AI-with-Python resource books

Curated, link-verified reference documents about **Kiro** (the AWS agentic IDE) and about
**building software with AI in Python**. Every link in these files was requested and checked;
every Python snippet was syntax-checked.

## Documents

| File | What it is |
|------|------------|
| [`Kiro_IDE_Resources.xlsx`](./Kiro_IDE_Resources.xlsx) | Master catalogue of Kiro resources — **292 curated links** across 29 categories, plus an auto-generated index of all **244 official documentation pages** and **13 copy-paste config snippets** (mcp.json, hooks, steering, skills, agents, CI). 6 sheets. |
| [`Build_Software_with_AI_and_Python.docx`](./Build_Software_with_AI_and_Python.docx) | A tiered guide (Word) to creating software with AI in Python — **beginner / intermediate / advanced**. A 14-stage roadmap, **172 curated resources**, and **21 ready-to-run code snippets**. Every resource title is a clickable hyperlink. |
| [`Build_Software_with_AI_and_Python.xlsx`](./Build_Software_with_AI_and_Python.xlsx) | The same AI-with-Python guide as an Excel workbook (6 sheets: Start here, Roadmap, All resources with filters, By level, Code snippets, Index). |

## Levels in the AI-with-Python guide

- **Beginner** — Python fundamentals, your first LLM call, giving it a UI, running models locally.
- **Intermediate** — FastAPI, project tooling (uv / ruff / pytest / mypy), data & ML, reliable structured output, RAG, deployment.
- **Advanced** — agents & orchestration, MCP, fine-tuning, serving (vLLM / Ray), evaluation, observability, OWASP LLM security, cost & performance.

## How the documents were generated

The `src/` directory contains the data modules and build scripts used to produce the files above,
kept for provenance and so the documents can be regenerated or extended.

| Script | Produces | Reads |
|--------|----------|-------|
| `src/build_workbook.py` | `Kiro_IDE_Resources.xlsx` | `kiro_resources_data.py`, `config_snippets.py`, `link_status.json`*, `_docs/llms.txt`* |
| `src/build_docx.py` | `Build_Software_with_AI_and_Python.docx` | `ai_python_data.py`, `ai_python_snippets.py`, `ai_link_status.json`* |
| `src/build_ai_workbook.py` | `Build_Software_with_AI_and_Python.xlsx` | `ai_python_data.py`, `ai_python_snippets.py`, `ai_link_status.json`* |
| `src/check_links.py`, `src/check_links_ai.py` | the `*link_status.json` files | the data modules |

`*` These inputs (`link_status.json`, `ai_link_status.json`, `_docs/llms.txt`) are locally generated
intermediates and are `.gitignore`d. Regenerate them with the link-check scripts before rebuilding.

### Regenerating (from `src/`)

```bash
pip install openpyxl python-docx
cd src

# refresh link-check status (writes ai_link_status.json)
python check_links_ai.py

# rebuild the AI-with-Python documents
python build_docx.py
python build_ai_workbook.py
```

## Notes & caveats

- **Link status.** At the last check, the AI-with-Python catalogue was 166 live (HTTP 200) and 6 behind
  bot protection (they open normally in a browser); none were broken. The Kiro catalogue was similarly
  verified. Both workbooks carry a per-row link-check column.
- The AI/Kiro tooling landscape changes quickly — versions, model names, prices and even documentation
  URLs move. Cross-check community posts against official docs.
- Code snippets are **starting points**, not production code: add real error handling, secrets management
  and tests before shipping.
- Community repositories, gists and courses linked in these documents are not endorsed by their respective
  vendors; paid courses should be checked for reviews and recency before purchase.
