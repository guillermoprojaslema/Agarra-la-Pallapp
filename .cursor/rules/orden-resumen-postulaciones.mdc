---
description: En el resumen de postulaciones, listar de la más reciente a la más antigua
alwaysApply: true
---

# Orden del documento de resumen

En `reportes/resumen-postulaciones-*.md` / `.html` / `.pdf` (y al regenerarlo con `scripts/resumen_postulaciones.py` o `/resumen-postulaciones`), las publicaciones van **de la postulación más reciente a la más antigua**.

## Criterio

1. Ordenar por **Fecha postulación** (`YYYY-MM-DD`), descendente.
2. El mismo día: por **ID** (`OF-YYYYMMDD-NN`), correlativo más alto primero.
3. Sin fecha: al **final**.

No usar el orden de `ofertas/pendientes.md`.

```python
# ✅ más reciente primero
ofertas.sort(
    key=lambda o: (o.fecha if o.fecha and o.fecha != "sin fecha" else "0000-00-00", o.of_id),
    reverse=True,
)

# ❌ más antigua primero
ofertas.sort(key=lambda o: (o.fecha, o.of_id))
```
