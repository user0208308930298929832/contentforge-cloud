CONTENT_SYSTEM = (
    "És um assistente especialista em marketing e social media em Português‑Portugal. "
    "Geras ideias curtas, legendas objetivas, 15 hashtags relevantes e um CTA claro. "
    "Mantém o texto direto e prático. Responde SEMPRE em JSON válido."
)
SHORTS_USER_TEMPLATE = (
    "Nicho: {niche}\nObjetivo: {objective}\nTom: {tone}\nPlataformas: {platforms}\nQuantidade por plataforma: {count}\n"
    "Devolve JSON com a chave 'items' = lista de objetos com: platform, idea, caption (<=300), hashtags (15), cta, thumbnail_prompt."
)
CAROUSEL_TEMPLATE = (
    "Cria 4 ideias de carrossel para Instagram (JSON). "
    "Formato: { 'items': [ { 'title': str, 'bullets': [str, ...] }, ... ] } Bullets: 4–7."
)
BLOGS_TEMPLATE = (
    "Cria 3 ideias de artigos de blog (JSON). "
    "Formato: { 'items': [ { 'title': str, 'outline': [str, ...] }, ... ] } 5 secções por outline."
)
