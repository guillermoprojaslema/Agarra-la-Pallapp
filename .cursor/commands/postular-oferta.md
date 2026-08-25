---
description: Flujo 2 — postular con navegador adaptando el CV desde la cola de ofertas
alwaysApply: true
---

# Flujo 2: Postular a una oferta

Cuando el usuario diga **postula**, **aplica**, **postular a OF-…**, o elija un ítem de `ofertas/pendientes.md`, ejecutar este flujo.

## Entrada

- ID de oferta (`OF-…`) o URL concreta.
- Leer la fila en `ofertas/pendientes.md` (debe existir o crearse si solo dio URL).

## Pasos (en orden)

1. **Leer la oferta** (URL) y `CV_Base.docx`.
2. **Adaptar el CV** según la regla `adaptar-cv-oferta` (Harvard desde el base, perfil + bullets ATS, compilar).
3. **Commit + README** según esa misma regla (URL + hash).
4. **Navegador:** abrir la URL, revisar que siga vigente.
5. **Confirmación obligatoria** antes de enviar: mostrar cargo + URL y preguntar «¿Confirmo el envío de la postulación?».
6. Tras el sí del usuario: completar el formulario de postulación con el PDF adaptado (`CV_Axel_Pfingsten_Arpe.pdf`) y datos de contacto del base.
7. Si hay **login, captcha o paso manual**, detenerse y pedir que el usuario tome el control; no inventar credenciales.
8. Actualizar `ofertas/pendientes.md`:
   - `Estado: postulada` (o `bloqueada` / `cerrada` si falló)
   - **Commit** del CV adaptado
   - **Fecha postulación**
9. Responder en español: resultado, hash, PDF usado.

## Estados válidos

`pendiente` → `en_adaptacion` → `lista_para_postular` → `postulada` | `bloqueada` | `cerrada`

## Prohibido

- Postular sin confirmación explícita del usuario.
- Usar o subir `.github/credentials.txt` a portales de empleo.
- Modificar `CV_Base.docx` con texto de la vacante.
