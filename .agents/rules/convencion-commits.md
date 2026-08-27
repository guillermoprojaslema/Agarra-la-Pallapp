---
description: Convención de mensajes y buenas prácticas al hacer commits
alwaysApply: true
---

# Convención de commits

Autor y PAT: regla `git-credentials`. Adaptación de CV: regla `commits-adaptacion` (3 commits; no fusionar CV y README).

## Mensaje

- **Español**, una línea de asunto; cuerpo opcional separado por línea en blanco.
- **Infinitivo** que explica el *porqué* (no listar archivos): Adaptar, Registrar, Marcar, Documentar, Ordenar, Corregir.
- Asunto **≤ 72 caracteres** si cabe; en adaptaciones de CV puede ir el cargo completo.
- Terminar el asunto con punto. Sin `feat:`/`fix:`, sin emoji, sin issue IDs inventados.
- Pasar el mensaje por HEREDOC; no `--amend`, `--no-verify` ni `git config` salvo pedido explícito.

```text
✅ Adaptar CV Harvard a OF-20260826-22: Enfermero(a) Intermedio / UTI — Clínica San Carlos.
✅ Registrar en README la adaptación OF-20260826-22 (cf1ad1d).
✅ Ordenar el resumen de postulaciones de más reciente a más antigua.

❌ Updated files
❌ feat: add stuff
❌ WIP
❌ Ajustes varios
```

## Qué entra en el commit

- **Un cambio lógico** por commit; no mezclar reglas, CV de otra oferta y cola.
- Revisar `git status` y `git diff` antes de `git add`; staging selectivo.
- **Nunca** staged: `.github/credentials.txt`, `.cursor/**/credentials`, `reportes/`, secretos, `.env`.
- No `CV_Base.docx` salvo que el usuario pida actualizar el base.
- No commit vacío. No push a menos que el flujo o el usuario lo pidan (`git-credentials`).
