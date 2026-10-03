# RESUME IQ — How the analysis works

RESUME IQ intentionally separates deterministic results from Gemini-generated feedback.

## Deterministic layer

`resume_parser.py` extracts text from PDF and DOCX files. `resume_insights.py` then looks for explicitly named items in a maintained skills catalog and recognizable resume section headings. When a job description is supplied, it compares only those explicit catalog matches. `ml_features.py` also calculates lexical TF-IDF similarity.

These signals are useful indicators, not an ATS score, competency assessment, or hiring decision.

## Optional Gemini layer

When the user selects Gemini review and supplies a valid API key, the workflow runs in this order:

```text
Extractor Agent → Evaluator Agent + RAG context → Coach Agent
```

All agents use `gemini_client.py`; it is the only place that reads `GEMINI_API_KEY` and `GEMINI_MODEL`. Errors returned by an agent are raised by the orchestrator and shown in the interface without preventing deterministic results from rendering.

## Extending the product

- Add carefully reviewed terms to `SKILL_CATALOG` rather than inferring skills from unrelated text.
- Add tests whenever a catalog or matching rule changes.
- Keep generated Gemini advice visually and semantically distinct from rule-based findings.
- Never commit `.streamlit/secrets.toml` or an API key.
