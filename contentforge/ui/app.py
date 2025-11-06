import os, sys, json, base64
import streamlit as st
from pathlib import Path

# --- Corrige imports para Streamlit Cloud ---
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
# --------------------------------------------

from contentforge.services.generator import generate_all
from contentforge.services.exporter import export_csv, export_md, export_txt

st.set_page_config(page_title="ContentForge — Cloud", layout="wide")
st.title("ContentForge — Geração de Conteúdo (Cloud Only)")

with st.sidebar:
    st.header("Parâmetros")
    niche = st.text_input("Nicho/Tema", "fitness")
    objective = st.text_input("Objetivo", "atrair clientes PT")
    tone = st.text_input("Tom", "motivacional")
    platforms = st.multiselect("Plataformas", ["instagram", "tiktok", "linkedin"], default=["instagram","tiktok"])
    count = st.slider("Nº de ideias por plataforma", 1, 10, 3)

    st.subheader("Modelo")
    model = st.text_input("OpenAI model", os.getenv("OPENAI_MODEL","gpt-4o-mini"))

    st.caption("A app usa a variável de ambiente OPENAI_API_KEY (define-a no Streamlit Cloud).")

    st.subheader("Presets")
    preset_name = st.text_input("Nome do preset", "default")
    if st.button("Guardar Preset"):
        preset = {"niche": niche, "objective": objective, "tone": tone, "platforms": platforms, "count": count, "model": model}
        Path("contentforge/data/presets").mkdir(parents=True, exist_ok=True)
        (Path("contentforge/data/presets")/f"{preset_name}.json").write_text(json.dumps(preset, ensure_ascii=False, indent=2), encoding="utf-8")
        st.success(f"Preset '{preset_name}' guardado.")
    if st.button("Carregar Preset"):
        p = Path(f"contentforge/data/presets/{preset_name}.json")
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            niche = d.get("niche", niche)
            objective = d.get("objective", objective)
            tone = d.get("tone", tone)
            platforms = d.get("platforms", platforms)
            count = d.get("count", count)
            model = d.get("model", model)
            st.success(f"Preset '{preset_name}' carregado.")
        else:
            st.error("Preset não encontrado.")

col1, col2, col3 = st.columns([1,1,1])

if "last_data" not in st.session_state:
    st.session_state["last_data"] = None

with col1:
    if st.button("Gerar Conteúdo", use_container_width=True):
        try:
            data = generate_all(niche, objective, tone, platforms, count, model=model)
            st.session_state["last_data"] = data
            st.success("Conteúdo gerado com IA!")
        except Exception as e:
            st.error(f"Falha ao gerar: {e}")

with col2:
    if st.button("Exportar CSV", use_container_width=True):
        if not st.session_state["last_data"]:
            st.warning("Gera primeiro.")
        else:
            b = export_csv(st.session_state["last_data"])
            st.download_button("Descarregar CSV", b, file_name="contentforge_export.csv", mime="text/csv")

with col3:
    if st.button("Exportar MD/TXT", use_container_width=True):
        if not st.session_state["last_data"]:
            st.warning("Gera primeiro.")
        else:
            b = export_md(st.session_state["last_data"])
            st.download_button("Descarregar MD", b, file_name="contentforge_export.md", mime="text/markdown")

st.markdown("---")

data = st.session_state.get("last_data")
if data:
    st.subheader("Shorts (Reels/TikTok/LinkedIn)")
    for i, item in enumerate(data.get("shorts", [])[:100]):
        with st.expander(f"{i+1}. [{item.get('platform','').upper()}] {item.get('idea','')}"):
            st.write("**Legenda:**", item.get("caption",""))
            st.write("**Hashtags:**", " ".join(item.get("hashtags", [])))
            st.write("**CTA:**", item.get("cta",""))
            st.code(item.get("thumbnail_prompt",""), language="text")

    st.subheader("Carrosséis (IG)")
    for c in data.get("carousels", []):
        st.write(f"**{c.get('title','')}**")
        for b in c.get("bullets", []):
            st.write(f"- {b}")
        st.write("---")

    st.subheader("Blogs")
    for b in data.get("blogs", []):
        st.write(f"**{b.get('title','')}**")
        for sec in b.get("outline", []):
            st.write(f"- {sec}")
        st.write("---")
else:
    st.info("Gera conteúdo para aparecer aqui.")
