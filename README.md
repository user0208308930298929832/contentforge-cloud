# ContentForge — Cloud Only (Streamlit)

App de geração de conteúdo (PT‑PT) 100% em Streamlit, sem backend externo.
Liga-se diretamente à OpenAI (gpt-4o-mini).

## Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # coloca a tua OPENAI_API_KEY
streamlit run contentforge/ui/app.py
```

## Streamlit Cloud
- Main file: `contentforge/ui/app.py`
- Env vars:
  - `OPENAI_API_KEY` = a tua chave
  - `OPENAI_MODEL` = gpt-4o-mini
```

