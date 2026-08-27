---
description: Generar resumen PDF de postulaciones enviadas y enviarlo por correo
---

# Resumen de postulaciones enviadas

Cuando el usuario pida **resumen de postulaciones**, **resumen postuladas**, **qué CV postulé**, `/resumen-postulaciones` o similar, ejecutar este flujo.

## Fuente de verdad

- Cola: [`ofertas/pendientes.md`](ofertas/pendientes.md) — solo **`Estado: postulada`**.
- CV por oferta: **`Commit CV`** → `CV_Axel_Pfingsten_Arpe.pdf` congelado en ese commit (hash **completo**).
- Correo: [`.cursor/correo_destino/correo_destino.md`](.cursor/correo_destino/correo_destino.md) (origen/destino).
- SMTP: [`.cursor/correo_destino/credentials`](.cursor/correo_destino/credentials) (`app_password` Gmail del correo origen). **No commitear.**

## Pasos

1. Verificar que exista `.cursor/correo_destino/credentials` con `app_password` válida (si falta, copiar desde `credentials.example` y pedir al usuario que la complete **solo si el envío falla**).

2. Ejecutar desde la raíz:

```bash
python3 scripts/resumen_postulaciones.py --export-pdfs --email --stdout
```

3. El script genera:
   - `reportes/resumen-postulaciones-YYYY-MM-DD.md`
   - `reportes/resumen-postulaciones-YYYY-MM-DD.html` (intermedio)
   - `reportes/resumen-postulaciones-YYYY-MM-DD.pdf` (resumen renderizado)
   - `reportes/pdfs/OF-YYYYMMDD-NN.pdf` (CV de cada postulación, opcional)

4. **Envía por correo** el PDF del resumen al destino configurado en `correo_destino.md` (desde el origen indicado ahí).

5. Responder al usuario en **español**: rutas generadas, cantidad de postulaciones, confirmación de envío (origen → destino).

## Orden de las publicaciones

Listar **de la postulación más reciente a la más antigua** (fecha descendente; el mismo día, ID `OF-…` más alto primero; sin fecha al final). No usar el orden de `pendientes.md`.

## Contenido mínimo por oferta

- URL de la postulación
- `CV_Axel_Pfingsten_Arpe.pdf`
- **Hash completo** del commit CV
- Título y perfil adaptados (desde el `.tex` en ese commit)
- Enlace público de descarga del PDF (`raw.githubusercontent.com`) y al commit si `origin` está configurado. El repo es público para que quien reciba el resumen no necesite login.

## No hacer

- No incluir ofertas que no estén `postulada` (salvo pedido explícito).
- No commitear `reportes/` ni `.cursor/correo_destino/credentials`.
- No imprimir `app_password` en chat, logs ni commits.

## Opciones

```bash
python3 scripts/resumen_postulaciones.py --email
python3 scripts/resumen_postulaciones.py --export-pdfs --email --stdout
python3 scripts/resumen_postulaciones.py --skip-email   # solo generar PDF, sin enviar
```
