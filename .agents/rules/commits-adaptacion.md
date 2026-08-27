---
description: Secuencia de 3 commits al adaptar un CV (CV, README, cola) y push con credenciales
alwaysApply: true
---

# Commits de adaptación

Tras adaptar y compilar el Harvard, **tres commits separados** y luego **push**. Autor y PAT solo desde `.github/credentials.txt` (regla `git-credentials`); no tocar `git config`. Atajo: `scripts/_commit_adaptacion.sh "OF-…" "Cargo" "URL" "kw1, kw2, kw3, kw4, kw5"`.

## Secuencia (obligatoria)

1. **CV** — `CV_Axel_Pfingsten_Arpe.tex` y `.pdf`  
   `Adaptar CV Harvard a OF-…: Cargo.`
2. **README** — entrada **arriba** del historial (más reciente primero) con fecha, cargo, URL, **hash completo** del commit 1, `CV_Base.docx`, PDF, 5 keywords ATS  
   `Registrar en README la adaptación OF-… (abcdefg).`
3. **Cola** — `ofertas/pendientes.md`: `lista_para_postular` + `Commit CV` (helper `scripts/_update_pendiente.py`)  
   `Marcar OF-… lista_para_postular con hash del CV.`
4. **Push** a `origin` con usuario+token del archivo de credenciales (sin imprimir el PAT).

No fusionar CV y README en un solo commit: el README necesita el hash del primero.

## Prohibido en staging

`.github/credentials.txt`, `.cursor/correo_destino/credentials`, `.cursor/job_credentials/credentials`, `reportes/`, `CV_Base.docx` (salvo que el usuario pida actualizar el base).
