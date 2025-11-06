import os, json
from typing import List, Dict, Any
from openai import OpenAI
from ..core.prompts import CONTENT_SYSTEM, SHORTS_USER_TEMPLATE, CAROUSEL_TEMPLATE, BLOGS_TEMPLATE

def _client() -> OpenAI:
    # Corrige bug do Streamlit Cloud com proxies
    os.environ.pop("http_proxy", None)
    os.environ.pop("https_proxy", None)
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def _chat_json(system: str, user: str, model: str) -> Dict[str, Any]:
    cli = _client()
    resp = cli.chat.completions.create(
        model=model,
        temperature=0.7,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}],
        response_format={"type":"json_object"}
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        start = content.find("{"); end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(content[start:end+1])
        raise

def generate_shorts(niche: str, objective: str, tone: str, platforms: List[str], count: int, model: str) -> List[Dict[str, Any]]:
    prompt = SHORTS_USER_TEMPLATE.format(niche=niche, objective=objective, tone=tone, platforms=", ".join(platforms), count=count)
    data = _chat_json(CONTENT_SYSTEM, prompt, model=model)
    items = data.get("items") if isinstance(data, dict) else None
    return items if isinstance(items, list) else []

def generate_carousels(niche: str, model: str) -> List[Dict[str, Any]]:
    data = _chat_json(CONTENT_SYSTEM, CAROUSEL_TEMPLATE, model=model)
    items = data.get("items") if isinstance(data, dict) else None
    return items if isinstance(items, list) else []

def generate_blogs(niche: str, objective: str, model: str) -> List[Dict[str, Any]]:
    data = _chat_json(CONTENT_SYSTEM, BLOGS_TEMPLATE, model=model)
    items = data.get("items") if isinstance(data, dict) else None
    return items if isinstance(items, list) else []

def generate_all(niche: str, objective: str, tone: str, platforms: List[str], count: int, model: str) -> Dict[str, Any]:
    shorts = generate_shorts(niche, objective, tone, platforms, count, model=model)
    carousels = generate_carousels(niche, model=model)
    blogs = generate_blogs(niche, objective, model=model)
    return {"shorts": shorts, "carousels": carousels, "blogs": blogs}
