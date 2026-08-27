#!/usr/bin/env bash
# Uso: ./scripts/_commit_adaptacion.sh "OF-ID" "Cargo" "URL" "kw1, kw2, kw3, kw4, kw5"
set -euo pipefail
cd "$(dirname "$0")/.."
OF_ID="${1:?}"
CARGO="${2:?}"
URL="${3:?}"
KEYWORDS="${4:?}"
EMAIL=$(grep -m1 '^email:' .github/credentials.txt | sed 's/^email:[[:space:]]*//')
NAME=$(grep -m1 '^Author:' .github/credentials.txt | sed 's/^Author:[[:space:]]*//')
USER=$(sed -n '1p' .github/credentials.txt)
TOKEN=$(sed -n '2s/^token: //p' .github/credentials.txt)
REMOTE=$(git remote get-url origin | sed -E 's#^https://([^/@]+@)?#https://#')

pdflatex -interaction=nonstopmode CV_Axel_Pfingsten_Arpe.tex >/tmp/pdflatex1.log
pdflatex -interaction=nonstopmode CV_Axel_Pfingsten_Arpe.tex >/tmp/pdflatex2.log

git add CV_Axel_Pfingsten_Arpe.tex CV_Axel_Pfingsten_Arpe.pdf
GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
git commit -m "$(cat <<EOF
Adaptar CV Harvard a ${OF_ID}: ${CARGO}.

Partiendo de CV_Base.docx; perfil y bullets alineados a la oferta.
EOF
)"
HASH=$(git rev-parse HEAD)

TMP=$(mktemp)
{
  echo "## $(date +%Y-%m-%d) — ${CARGO}"
  echo
  echo "- **URL:** ${URL}"
  echo "- **Commit:** \`${HASH}\`"
  echo "- **Base:** \`CV_Base.docx\`"
  echo "- **PDF:** \`CV_Axel_Pfingsten_Arpe.pdf\`"
  echo "- **Keywords ATS:** ${KEYWORDS}"
  echo
} >"$TMP"
awk -v f="$TMP" '
  /^## Historial de postulaciones$/ { print; print ""; while ((getline line < f) > 0) print line; next }
  { print }
' README.md > README.md.new && mv README.md.new README.md
rm -f "$TMP"

git add README.md
GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
git commit -m "$(cat <<EOF
Registrar en README la adaptación ${OF_ID} (${HASH:0:7}).

EOF
)"

python3 scripts/_update_pendiente.py "$OF_ID" "$HASH"
git add ofertas/pendientes.md
GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
git commit -m "$(cat <<EOF
Marcar ${OF_ID} lista_para_postular con hash del CV.

EOF
)"

git push "https://${USER}:${TOKEN}@${REMOTE#https://}" HEAD >/tmp/gitpush.log 2>&1
echo "OK ${OF_ID} HASH=${HASH}"
tail -5 /tmp/gitpush.log
