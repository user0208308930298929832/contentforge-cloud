import csv, io
from typing import Dict, Any
from datetime import datetime

def export_csv(contents: Dict[str, Any]) -> bytes:
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["type","platform","idea","caption","hashtags","cta","thumbnail_prompt","title","bullets","outline"])
    for s in contents.get("shorts", []):
        w.writerow(["short", s.get("platform",""), s.get("idea",""), s.get("caption",""),
                    " ".join(s.get("hashtags", [])), s.get("cta",""), s.get("thumbnail_prompt",""), "", "", ""])
    for c in contents.get("carousels", []):
        w.writerow(["carousel","","","","","","", c.get("title",""), " | ".join(c.get("bullets", [])), ""])
    for b in contents.get("blogs", []):
        w.writerow(["blog","","","","","","", b.get("title",""), "", " | ".join(b.get("outline", []))])
    return output.getvalue().encode("utf-8")

def export_md(contents: Dict[str, Any]) -> bytes:
    lines = [f"# Export {datetime.utcnow().isoformat()}Z\n"]
    lines.append("## Shorts\n")
    for s in contents.get("shorts", []):
        lines.append(f"### {s.get('platform','').upper()} — {s.get('idea','')}")
        lines.append(s.get("caption",""))
        if s.get("hashtags"): lines.append(" ".join(s["hashtags"]))
        if s.get("cta"): lines.append(f"**CTA:** {s['cta']}")
        if s.get("thumbnail_prompt"): lines.append(f"`{s['thumbnail_prompt']}`")
        lines.append("")
    lines.append("## Carrosséis\n")
    for c in contents.get("carousels", []):
        lines.append(f"### {c.get('title','')}")
        for b in c.get("bullets", []):
            lines.append(f"- {b}")
        lines.append("")
    lines.append("## Blogs\n")
    for b in contents.get("blogs", []):
        lines.append(f"### {b.get('title','')}")
        for o in b.get("outline", []):
            lines.append(f"- {o}")
        lines.append("")
    return "\n".join(lines).encode("utf-8")

def export_txt(contents: Dict[str, Any]) -> bytes:
    return export_md(contents)
