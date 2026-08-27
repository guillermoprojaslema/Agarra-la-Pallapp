import re, sys
from pathlib import Path
of_id, hash_ = sys.argv[1], sys.argv[2]
p = Path("ofertas/pendientes.md")
text = p.read_text()
needle = f"## {of_id} —"
idx = text.find(needle)
if idx < 0:
    raise SystemExit(f"no hallado {of_id}")
nxt = text.find("\n## ", idx + 1)
block = text[idx:] if nxt < 0 else text[idx:nxt]
block2 = block.replace("**Estado:** en_adaptacion", "**Estado:** lista_para_postular", 1)
block2 = block2.replace("**Estado:** pendiente", "**Estado:** lista_para_postular", 1)
if "**Commit CV:**" in block2:
    block2 = re.sub(r"- \*\*Commit CV:\*\* `[^`]+`", f"- **Commit CV:** `{hash_}`", block2, count=1)
elif "- **Detectada:**" in block2:
    block2 = block2.replace("- **Detectada:**", f"- **Commit CV:** `{hash_}`\n- **Detectada:**", 1)
else:
    block2 = block2.rstrip() + f"\n- **Commit CV:** `{hash_}`\n"
text2 = text[:idx] + block2 + ("" if nxt < 0 else text[nxt:])
p.write_text(text2)
print(f"ok {of_id} {hash_}")
