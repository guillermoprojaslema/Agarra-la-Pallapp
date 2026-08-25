---
description: Flujo 1 — buscar ofertas ad-hoc, listarlas y guardarlas en ofertas/
alwaysApply: true
---

# Flujo 1: Buscar ofertas

Cuando el usuario pida **buscar ofertas**, **encontrar vacantes**, **listar trabajos** o similar (sin pedir aún postular), ejecutar este flujo.

## Alcance

- Perfil: enfermero APS / domiciliaria / SAR / procedimientos, según `CV_Base.docx`.
- Región: **Región Metropolitana (RM), Chile**.
- Solo ofertas **aún disponibles** (publicadas recientemente / con postulación abierta).
- No hace falta match 100 %; sí ad-hoc al cargo.

## Pasos

1. Buscar en Computrabajo, Mipleo, Empleos Públicos, portales municipales/CESFAM, Ancora/UC Christus, etc.
2. Verificar vigencia (fecha, “hace X horas/días”, plazo de postulación).
3. Presentar al usuario un **listado numerado** (cargo, comuna, renta si hay, por qué encaja, URL).
4. **Guardar/actualizar** `ofertas/pendientes.md` con las ofertas nuevas (sin duplicar la misma URL).
5. Estado inicial de cada ítem: `pendiente`.

## Formato en `ofertas/pendientes.md`

```markdown
## OF-YYYYMMDD-NN — Título del cargo

- **Estado:** pendiente
- **URL:** https://...
- **Comuna / zona:** ...
- **Fuente:** Computrabajo | Empleos Públicos | ...
- **Renta:** ... (si aparece)
- **Encaje:** 1–2 líneas vs CV_Base
- **Detectada:** YYYY-MM-DD
```

IDs: `OF-` + fecha + correlativo del día (`01`, `02`, …).

## No hacer en este flujo

- No adaptar el CV.
- No abrir postulación en el navegador.
- No marcar `postulada` aquí.
