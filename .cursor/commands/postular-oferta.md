---
description: Flujo 2 — postular en lote (todas las no postuladas) adaptando el CV desde la cola
alwaysApply: true
---

# Flujo 2: Postular a ofertas

Cuando el usuario diga **postula**, **aplica**, **postular**, `/postular-oferta`, o similar, ejecutar este flujo.

## Entrada (por defecto: lote completo)

- **Por defecto:** procesar **todas** las ofertas de `ofertas/pendientes.md` cuyo estado **no** sea `postulada`, `bloqueada` ni `cerrada` (típicamente `pendiente`, `en_adaptacion`, `lista_para_postular`).
- **Excepción:** si el usuario indica un `OF-…` o URL concreta, procesar solo esa.
- Si solo dio URL y no está en la cola, crear el ítem y continuar.

## Orden del lote

1. Listar al inicio las ofertas a procesar (ID, cargo, URL).
2. Recorrerlas **una a una** en el orden de `pendientes.md` (o el que indique el usuario).
3. No saltar una pendiente salvo que el usuario la excluya o quede `cerrada`/`bloqueada`.

## Pasos por cada oferta (en orden)

1. Marcar `Estado: en_adaptacion`.
2. **Leer la oferta** (URL) y `CV_Base.docx`.
3. **Adaptar el CV** según la regla `adaptar-cv-oferta` (Harvard desde el base, perfil + bullets ATS, compilar).
4. **Commit + README** según esa misma regla (URL + hash).
5. Marcar `Estado: lista_para_postular`.
6. **Navegador:** abrir la URL, revisar que siga vigente.
7. **Confirmación obligatoria** antes de enviar:
   - En lote: una confirmación puede cubrir varias ofertas pendientes de envío; listar cargo + URL de cada una y preguntar «¿Confirmo el envío de la(s) postulación(es)?».
   - Si el usuario confirma solo algunas, enviar solo esas.
8. Tras el sí: completar el formulario con el PDF adaptado de esa oferta (`CV_Axel_Pfingsten_Arpe.pdf` de esa adaptación) y datos de contacto del base.
9. Si hay **login**, usar solo `.cursor/job_credentials/credentials` (nunca `.github/credentials.txt`). Si hay **captcha o paso manual**, detenerse y pedir que el usuario tome el control; no inventar credenciales.
10. Actualizar `ofertas/pendientes.md`:
    - `Estado: postulada` (o `bloqueada` / `cerrada` si falló)
    - **Commit** del CV adaptado
    - **Fecha postulación**
11. Continuar con la siguiente oferta del lote.

## Al cerrar el lote

Responder en español: resumen por oferta (resultado, hash, PDF), cuántas `postulada` / `bloqueada` / `cerrada`.

## Estados válidos

`pendiente` → `en_adaptacion` → `lista_para_postular` → `postulada` | `bloqueada` | `cerrada`

## Prohibido

- Postular sin confirmación explícita del usuario (al menos una vez por lote o por oferta).
- Usar o subir `.github/credentials.txt` a portales de empleo.
- Modificar `CV_Base.docx` con texto de la vacante.
- Dar por terminado el flujo dejando ofertas `pendiente` sin procesar, salvo exclusión del usuario o bloqueo real.
