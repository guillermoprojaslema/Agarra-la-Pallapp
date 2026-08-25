#!/usr/bin/env python3
"""Adapta título + perfil del Harvard, compila, actualiza pendientes/README (sin commits)."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "CV_Axel_Pfingsten_Arpe.tex"
PEND = ROOT / "ofertas" / "pendientes.md"
README = ROOT / "README.md"


def set_title_profile(title: str, profile: str) -> None:
    text = TEX.read_text(encoding="utf-8")
    text = re.sub(
        r"(\{\\large Enfermero Profesional --- )[^}]+(\}\\\[6pt\])",
        rf"\1{title}\2",
        text,
        count=1,
    )
    text = re.sub(
        r"(\\section\{Perfil profesional\}\n)(.*?)(\n\n%========== COMPETENCIAS)",
        rf"\1{profile}\3",
        text,
        count=1,
        flags=re.S,
    )
    TEX.write_text(text, encoding="utf-8")


def compile_pdf() -> None:
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "CV_Axel_Pfingsten_Arpe.tex"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def mark_estado(of_id: str, estado: str) -> None:
    p = PEND.read_text(encoding="utf-8")
    p = re.sub(
        rf"(## {re.escape(of_id)}[^\n]*\n\n- \*\*Estado:\*\* )[^\n]+",
        rf"\1{estado}",
        p,
        count=1,
    )
    PEND.write_text(p, encoding="utf-8")


def set_commit(of_id: str, commit: str) -> None:
    p = PEND.read_text(encoding="utf-8")
    section = re.search(
        rf"(## {re.escape(of_id)}.*?)(?=\n## OF-|\Z)",
        p,
        flags=re.S,
    )
    if not section:
        raise SystemExit(f"No encontré {of_id}")
    body = section.group(1)
    if "**Commit CV:**" in body:
        body2 = re.sub(
            r"- \*\*Commit CV:\*\* `[^`]*`",
            f"- **Commit CV:** `{commit}`",
            body,
            count=1,
        )
        if body2 == body:
            body2 = re.sub(
                r"- \*\*Commit CV:\*\*[^\n]*",
                f"- **Commit CV:** `{commit}`",
                body,
                count=1,
            )
    else:
        body2 = re.sub(
            r"(- \*\*Detectada:\*\* [^\n]+)\n",
            rf"\1\n- **Commit CV:** `{commit}`\n",
            body,
            count=1,
        )
    PEND.write_text(p[: section.start()] + body2 + p[section.end() :], encoding="utf-8")


def prepend_readme(cargo: str, url: str, commit: str, keywords: str) -> None:
    entry = (
        f"## 2026-08-25 — {cargo}\n\n"
        f"- **URL:** {url}\n"
        f"- **Commit:** `{commit}`\n"
        f"- **Base:** `CV_Base.docx`\n"
        f"- **PDF:** `CV_Axel_Pfingsten_Arpe.pdf`\n"
        f"- **Keywords ATS:** {keywords}\n\n"
    )
    text = README.read_text(encoding="utf-8")
    marker = "## Historial de postulaciones\n\n"
    if cargo in text.split(marker, 1)[-1][:800]:
        # reemplaza bloque incompleto del mismo cargo si existe al tope
        pass
    if marker not in text:
        raise SystemExit("README sin historial")
    # Evitar duplicar el mismo cargo consecutivo
    rest = text.split(marker, 1)[1]
    if rest.startswith(f"## 2026-08-25 — {cargo}\n"):
        rest = re.sub(
            rf"^## 2026-08-25 — {re.escape(cargo)}\n\n.*?(?=\n## |\Z)",
            entry.rstrip() + "\n\n",
            rest,
            count=1,
            flags=re.S,
        )
        README.write_text(text.split(marker, 1)[0] + marker + rest, encoding="utf-8")
    else:
        README.write_text(text.replace(marker, marker + entry, 1), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--of-id", required=True)
    ap.add_argument("--cargo", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--keywords", required=True)
    ap.add_argument("--phase", choices=["prepare", "after-commit"], required=True)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    if args.phase == "prepare":
        mark_estado(args.of_id, "en_adaptacion")
        set_title_profile(args.title, args.profile)
        compile_pdf()
        print("prepared")
    else:
        if not args.commit:
            raise SystemExit("--commit requerido")
        mark_estado(args.of_id, "lista_para_postular")
        set_commit(args.of_id, args.commit)
        prepend_readme(args.cargo, args.url, args.commit, args.keywords)
        print("documented")


if __name__ == "__main__":
    main()
