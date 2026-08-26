#!/usr/bin/env python3
"""Genera resumen de postulaciones enviadas, PDF renderizado y envío por correo."""
from __future__ import annotations

import argparse
import html
import re
import smtplib
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PEND = ROOT / "ofertas" / "pendientes.md"
CORREO_CFG = ROOT / ".cursor" / "correo_destino" / "correo_destino.md"
CORREO_CREDS = ROOT / ".cursor" / "correo_destino" / "credentials"
PDF_NAME = "CV_Axel_Pfingsten_Arpe.pdf"
TEX_NAME = "CV_Axel_Pfingsten_Arpe.tex"
CHROME = "google-chrome"

TITLE_RE = re.compile(
    r"\{\\large Enfermero Profesional --- (.+?)\}",
    re.DOTALL,
)
PROFILE_RE = re.compile(
    r"\\section\{Perfil profesional\}\n(.+?)\n\n%========== COMPETENCIAS",
    re.DOTALL,
)
SECTION_RE = re.compile(r"^## (OF-\d{8}-\d{2}) — (.+)$", re.M)
FIELD_RE = re.compile(r"^- \*\*(.+?):\*\* (.+)$", re.M)


@dataclass
class OfertaPostulada:
    of_id: str
    cargo: str
    url: str
    commit: str
    fecha: str
    fuente: str
    comuna: str


def git_remote_web_base() -> str | None:
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return None
    url = re.sub(r"\.git$", "", url)
    if url.startswith("git@"):
        host, repo = url[4:].split(":", 1)
        return f"https://{host}/{repo.removesuffix('.git')}"
    return url


def github_raw_cv_url(web_base: str, commit: str) -> str | None:
    """URL pública que descarga el PDF (sin login si el repo es público)."""
    m = re.search(r"github\.com/([^/]+)/([^/]+)/?$", web_base.rstrip("/"))
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{PDF_NAME}"


def resolve_full_commit(commit: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", commit],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return commit


def parse_postuladas() -> list[OfertaPostulada]:
    text = PEND.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^## OF-\d{8}-\d{2} — )", text, flags=re.M)
    out: list[OfertaPostulada] = []

    for block in blocks:
        header = SECTION_RE.search(block)
        if not header:
            continue
        fields = {k: v.strip() for k, v in FIELD_RE.findall(block)}
        if fields.get("Estado") != "postulada":
            continue
        commit = fields.get("Commit CV", "").strip("`")
        if not commit:
            continue
        out.append(
            OfertaPostulada(
                of_id=header.group(1),
                cargo=header.group(2).strip(),
                url=fields.get("URL", ""),
                commit=resolve_full_commit(commit),
                fecha=fields.get("Fecha postulación", "sin fecha"),
                fuente=fields.get("Fuente", ""),
                comuna=fields.get("Comuna / zona", ""),
            )
        )

    out.sort(key=lambda o: (o.fecha, o.of_id))
    return out


def git_show(commit: str, path: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{path}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return None


def cv_snapshot(commit: str) -> tuple[str, str]:
    tex = git_show(commit, TEX_NAME)
    if not tex:
        return ("(no disponible en commit)", "(no disponible en commit)")
    title_m = TITLE_RE.search(tex)
    profile_m = PROFILE_RE.search(tex)
    title = title_m.group(1).strip() if title_m else "(título no parseado)"
    profile = profile_m.group(1).strip() if profile_m else "(perfil no parseado)"
    profile = re.sub(r"\s+", " ", profile)
    if len(profile) > 220:
        profile = profile[:217] + "..."
    return title, profile


def export_cv_pdf(commit: str, dest: Path) -> bool:
    try:
        data = subprocess.check_output(
            ["git", "show", f"{commit}:{PDF_NAME}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True


def parse_correo_config() -> tuple[str, str]:
    if not CORREO_CFG.exists():
        raise SystemExit(f"No existe {CORREO_CFG}")
    text = CORREO_CFG.read_text(encoding="utf-8")
    origin = re.search(
        r"# Correo Origen\s*\n([^\s#]+@[^\s#]+)",
        text,
        re.I,
    )
    dest = re.search(
        r"# Correo Destino.*?([^\s#]+@[^\s#]+)",
        text,
        re.I | re.S,
    )
    if not origin or not dest:
        raise SystemExit("No pude leer origen/destino en correo_destino.md")
    return origin.group(1).strip(), dest.group(1).strip()


def load_smtp_password() -> str:
    if not CORREO_CREDS.exists():
        raise SystemExit(
            f"Falta {CORREO_CREDS}. Copia credentials.example y agrega app_password de Gmail."
        )
    text = CORREO_CREDS.read_text(encoding="utf-8")
    m = re.search(r"^app_password:\s*(.+)$", text, re.M | re.I)
    if not m or "xxxx" in m.group(1):
        raise SystemExit(
            f"Configura app_password en {CORREO_CREDS} (contraseña de aplicación Gmail)."
        )
    return re.sub(r"\s+", "", m.group(1).strip())


def send_email(
    *,
    from_addr: str,
    to_addr: str,
    subject: str,
    body: str,
    attachment: Path,
) -> None:
    password = load_smtp_password()
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with attachment.open("rb") as fh:
        part = MIMEApplication(fh.read(), _subtype="pdf")
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment.name,
        )
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_addr, password)
        smtp.sendmail(from_addr, [to_addr], msg.as_string())


def build_markdown(
    ofertas: list[OfertaPostulada],
    *,
    web_base: str | None,
    export_dir: Path | None,
) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Resumen de postulaciones enviadas — {today}",
        "",
        f"Total: **{len(ofertas)}** oferta(s) con estado `postulada` en `ofertas/pendientes.md`.",
        "",
        "Cada entrada incluye la URL del aviso, el CV Harvard postulado y el **hash completo** del commit.",
        "",
    ]

    for i, o in enumerate(ofertas, 1):
        title, profile = cv_snapshot(o.commit)
        lines.append(f"## {i}. {o.cargo}")
        lines.append("")
        lines.append(f"- **ID:** `{o.of_id}`")
        lines.append(f"- **URL:** {o.url}")
        if o.fuente:
            lines.append(f"- **Fuente:** {o.fuente}")
        if o.comuna:
            lines.append(f"- **Zona:** {o.comuna}")
        lines.append(f"- **Fecha postulación:** {o.fecha}")
        lines.append(f"- **CV postulado:** `{PDF_NAME}`")
        lines.append(f"- **Commit CV (hash):** `{o.commit}`")
        lines.append(f"- **Título CV:** {title}")
        lines.append(f"- **Perfil adaptado:** {profile}")
        if web_base:
            raw = github_raw_cv_url(web_base, o.commit)
            if raw:
                lines.append(f"- **Descargar CV (PDF):** {raw}")
            else:
                lines.append(
                    f"- **Ver CV en GitHub:** {web_base}/blob/{o.commit}/{PDF_NAME}"
                )
            lines.append(f"- **Commit en GitHub:** {web_base}/commit/{o.commit}")
        if export_dir:
            dest = export_dir / f"{o.of_id}.pdf"
            if export_cv_pdf(o.commit, dest):
                lines.append(f"- **PDF CV exportado:** `{dest.relative_to(ROOT)}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_html(ofertas: list[OfertaPostulada], *, web_base: str | None) -> str:
    today = date.today().isoformat()
    items: list[str] = []
    for i, o in enumerate(ofertas, 1):
        title, profile = cv_snapshot(o.commit)
        url = html.escape(o.url)
        cv_link = ""
        commit_link = ""
        if web_base:
            raw = github_raw_cv_url(web_base, o.commit)
            cv_href = raw or f"{web_base}/blob/{o.commit}/{PDF_NAME}"
            cv_link = (
                f'<p><strong>Descargar CV:</strong> '
                f'<a href="{html.escape(cv_href)}">{PDF_NAME}</a></p>'
            )
            commit_link = (
                f'<p><strong>Commit GitHub:</strong> '
                f'<a href="{web_base}/commit/{o.commit}">{o.commit[:12]}…</a></p>'
            )
        items.append(
            f"""
            <section class="oferta">
              <h2>{i}. {html.escape(o.cargo)}</h2>
              <p><strong>ID:</strong> <code>{html.escape(o.of_id)}</code></p>
              <p><strong>URL:</strong> <a href="{url}">{url}</a></p>
              {"<p><strong>Fuente:</strong> " + html.escape(o.fuente) + "</p>" if o.fuente else ""}
              {"<p><strong>Zona:</strong> " + html.escape(o.comuna) + "</p>" if o.comuna else ""}
              <p><strong>Fecha postulación:</strong> {html.escape(o.fecha)}</p>
              <p><strong>CV postulado:</strong> <code>{PDF_NAME}</code></p>
              <p><strong>Commit CV (hash):</strong><br><code class="hash">{html.escape(o.commit)}</code></p>
              <p><strong>Título CV:</strong> {html.escape(title)}</p>
              <p><strong>Perfil adaptado:</strong> {html.escape(profile)}</p>
              {cv_link}
              {commit_link}
            </section>
            """
        )

    body = "\n".join(items)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Resumen postulaciones {today}</title>
  <style>
    @page {{ margin: 18mm 16mm; }}
    body {{
      font-family: "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.45;
      color: #1a1a1a;
    }}
    h1 {{ font-size: 18pt; border-bottom: 2px solid #005293; padding-bottom: 6px; }}
    h2 {{ font-size: 13pt; color: #005293; margin-top: 18px; }}
    .meta {{ color: #444; margin-bottom: 20px; }}
    .oferta {{ page-break-inside: avoid; margin-bottom: 16px; padding-bottom: 12px;
               border-bottom: 1px solid #ddd; }}
    code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-size: 10pt; }}
    code.hash {{ display: inline-block; word-break: break-all; font-size: 9pt; }}
    a {{ color: #005293; }}
  </style>
</head>
<body>
  <h1>Resumen de postulaciones enviadas — {today}</h1>
  <p class="meta">Total: <strong>{len(ofertas)}</strong> postulación(es) registradas como enviadas.</p>
  {body}
</body>
</html>
"""


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    html_uri = html_path.resolve().as_uri()
    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_uri,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> int:
    ap = argparse.ArgumentParser(description="Resumen de postulaciones enviadas")
    ap.add_argument("-o", "--output", type=Path, help="Ruta del markdown")
    ap.add_argument(
        "--export-pdfs",
        action="store_true",
        help="Exportar PDF de cada CV a reportes/pdfs/",
    )
    ap.add_argument(
        "--stdout",
        action="store_true",
        help="Imprimir markdown en stdout",
    )
    ap.add_argument(
        "--email",
        action="store_true",
        help="Enviar PDF del resumen al correo destino configurado",
    )
    ap.add_argument(
        "--skip-email",
        action="store_true",
        help="No enviar correo aunque se genere PDF",
    )
    args = ap.parse_args()

    ofertas = parse_postuladas()
    if not ofertas:
        print("No hay ofertas con Estado postulada.", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    report_dir = ROOT / "reportes"
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = f"resumen-postulaciones-{today}"
    md_path = args.output or (report_dir / f"{stem}.md")
    html_path = md_path.with_suffix(".html")
    pdf_path = md_path.with_suffix(".pdf")
    export_dir = report_dir / "pdfs" if args.export_pdfs else None
    web_base = git_remote_web_base()

    md = build_markdown(ofertas, web_base=web_base, export_dir=export_dir)
    md_path.write_text(md, encoding="utf-8")
    html_path.write_text(build_html(ofertas, web_base=web_base), encoding="utf-8")
    render_pdf(html_path, pdf_path)

    print(f"Markdown: {md_path}")
    print(f"HTML:     {html_path}")
    print(f"PDF:      {pdf_path}")
    print(f"Total:    {len(ofertas)} postulación(es)")

    if args.stdout:
        print()
        print(md)

    if args.email and not args.skip_email:
        from_addr, to_addr = parse_correo_config()
        subject = f"Resumen postulaciones Axel Pfingsten — {today}"
        body = (
            f"Hola,\n\n"
            f"Adjunto el resumen de {len(ofertas)} postulación(es) enviadas a la fecha ({today}).\n"
            f"Cada entrada incluye URL del aviso y hash del commit del CV usado.\n\n"
            f"Saludos."
        )
        send_email(
            from_addr=from_addr,
            to_addr=to_addr,
            subject=subject,
            body=body,
            attachment=pdf_path,
        )
        print(f"Correo enviado: {from_addr} → {to_addr}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
