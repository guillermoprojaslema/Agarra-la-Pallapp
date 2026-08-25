#!/usr/bin/env bash
# Genera PDFs en todos los estilos populares de CV en LaTeX
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

ok()  { echo "  OK $1"; }
fail(){ echo "  FAIL $1"; rg -n "^!" "$2" | head -8 || true; }

echo "==> Harvard (artículo clásico)"
pdflatex -interaction=nonstopmode CV_Axel_Pfingsten_Arpe.tex >/tmp/cv_harvard.log 2>&1 \
  && ok CV_Axel_Pfingsten_Arpe.pdf || fail harvard /tmp/cv_harvard.log

echo "==> moderncv (casual, classic, banking, oldstyle, fancy)"
for style in casual classic banking oldstyle fancy; do
  sed "s/\\\\moderncvstyle{[^}]*}/\\\\moderncvstyle{${style}}/" CV_moderncv.tex > "CV_moderncv_${style}.tex"
  pdflatex -interaction=nonstopmode "CV_moderncv_${style}.tex" >/tmp/cv_${style}.log 2>&1 || true
  pdflatex -interaction=nonstopmode "CV_moderncv_${style}.tex" >/tmp/cv_${style}.log 2>&1 || true
  if [[ -f "CV_moderncv_${style}.pdf" ]] && ! rg -q "Fatal error|No pages of output" /tmp/cv_${style}.log; then
    ok "CV_moderncv_${style}.pdf"
  else
    fail "$style" /tmp/cv_${style}.log
  fi
done

echo "==> europecv (Europass)"
pdflatex -interaction=nonstopmode CV_europecv.tex >/tmp/cv_europecv.log 2>&1 || true
[[ -f CV_europecv.pdf ]] && ok CV_europecv.pdf || fail europecv /tmp/cv_europecv.log

echo "==> AltaCV"
(cd altacv-tpl && pdflatex -interaction=nonstopmode CV_Axel_altacv.tex >/tmp/cv_altacv.log 2>&1 \
  && cp -f CV_Axel_altacv.pdf ../CV_altacv.pdf && ok CV_altacv.pdf) \
  || fail AltaCV /tmp/cv_altacv.log

echo "==> Awesome-CV (xelatex)"
(cd awesome-cv-tpl && xelatex -interaction=nonstopmode CV_Axel_awesome.tex >/tmp/cv_awesome.log 2>&1 \
  && cp -f CV_Axel_awesome.pdf ../CV_awesome.pdf && ok CV_awesome.pdf) \
  || fail Awesome-CV /tmp/cv_awesome.log

echo
echo "PDFs listos en: $ROOT"
ls -1 CV_*.pdf | sort
