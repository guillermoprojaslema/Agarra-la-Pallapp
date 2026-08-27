---
description: Autenticación Git/GitHub y autor de commits desde .github/credentials.txt
alwaysApply: true
---

# Credenciales Git para commits y push

Cuando el usuario pida **commit**, **push** o cuando un flujo del proyecto (p. ej. `postular-oferta`, `adaptar-cv-oferta`) requiera registrar cambios en Git, usar **siempre** `.github/credentials.txt`. Mensajes y alcance del commit: regla `convencion-commits`.

## Formato del archivo

```
<usuario_github>
token: <PAT>

email: <email_autor>
Author: <nombre_autor>
```

- **Línea 1:** usuario de GitHub.
- **Línea 2:** token personal con prefijo `token: `.
- **Email:** línea `email: guillermorojaslema@gmail.com`.
- **Nombre:** línea `Author: Guillermo Rojas Lema`.

Leer el archivo al inicio de la operación; no repetir el token en chat, commits, README ni reglas.

## Protocolo obligatorio

1. **Antes de `git commit` o `git push`**, leer y parsear usuario, token, email y nombre.
2. **No modificar** `git config` (ni global ni local).
3. **No agregar** `.github/credentials.txt` al staging (ya está en `.gitignore`).
4. **No imprimir** el token en terminal, logs ni respuestas.

## Commit (autor obligatorio)

Cada commit debe quedar con autor **`guillermorojaslema@gmail.com`** (desde el archivo). Usar `--author` o variables de entorno **solo en ese comando**, sin persistir:

```bash
EMAIL=$(grep -m1 '^email:' .github/credentials.txt | sed 's/^email:[[:space:]]*//')
NAME=$(grep -m1 '^Author:' .github/credentials.txt | sed 's/^Author:[[:space:]]*//')
git commit --author="${NAME} <${EMAIL}>" -m "$(cat <<'EOF'
Mensaje del commit.

EOF
)"
```

Equivalente con env vars:

```bash
GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
git commit -m "..."
```

## Push a `origin`

Autenticar **solo para ese comando** con usuario + token del archivo:

```bash
USER=$(sed -n '1p' .github/credentials.txt)
TOKEN=$(sed -n '2s/^token: //p' .github/credentials.txt)
REMOTE=$(git remote get-url origin | sed -E 's#^https://([^/@]+@)?#https://#')
git push "https://${USER}:${TOKEN}@${REMOTE#https://}" HEAD
```

## Errores

- Si falta email, nombre o token: informar al usuario y **no** commitear/pushear.
- Si el push falla por auth: verificar validez del PAT; no reintentar exponiendo el token.
