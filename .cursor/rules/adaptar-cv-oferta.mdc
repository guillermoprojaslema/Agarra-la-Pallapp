---
description: Adaptar el CV a cada oferta desde CV_Base.docx; registrar URL + hash en README
alwaysApply: true
---

# Adaptar CV a ofertas laborales

Cuando el usuario compartá una **nueva oferta** (URL, texto o PDF) **o** el Flujo 2 (`postular-oferta`) dispare una adaptación desde `ofertas/pendientes.md`, aplicar **todo** este flujo sin esperar pedidos parciales.

## Fuente de verdad (obligatorio)

- El **CV base** es `CV_Base.docx` en la raíz del proyecto.
- **Toda** adaptación ad-hoc a una oferta parte de ese archivo: hechos, cargos, fechas, formación y competencias acreditadas.
- **No modificar** `CV_Base.docx` con lenguaje específico de una vacante; ese archivo permanece como plantilla maestra.
- **No inventar** experiencia que no figure en `CV_Base.docx` (salvo que el usuario la confirme explícitamente).

## 1. Adaptar el CV a la oferta

1. **Leer la oferta** completa (funciones, requisitos, keywords).
2. **Leer `CV_Base.docx`** y usarlo como base del contenido.
3. Generar/actualizar la versión de postulación prioritaria: **Harvard** `CV_Axel_Pfingsten_Arpe.tex` → `CV_Axel_Pfingsten_Arpe.pdf`. Otros estilos solo si el usuario lo pide.
4. **Título / encabezado** alineado al cargo.
5. **Perfil (≤ 4 oraciones)** con lenguaje de la oferta + **5 keywords ATS**, sin contradecir el base.
6. **Bullets afines:** `verbo + qué hiciste + resultado medible` (menos de 20 palabras), reescribiendo solo lo que ya existe en el base.
7. **Compilar** el Harvard (`pdflatex CV_Axel_Pfingsten_Arpe.tex`).

## 2. Commits + README.md (obligatorio)

Tras adaptar y compilar, aplicar la regla `commits-adaptacion` (3 commits + push; atajo `scripts/_commit_adaptacion.sh`):

1. **Commit del CV** adaptado (`.tex` + `.pdf`; no el base, salvo pedido explícito).
2. Hash: `git rev-parse HEAD`.
3. **README.md**: entrada nueva **arriba** del historial (más reciente primero) con fecha, cargo, URL, hash, base y keywords.
4. **Segundo commit** del `README.md`.
5. **Tercer commit** de `ofertas/pendientes.md` (`lista_para_postular` + `Commit CV`).
6. **Push** a `origin` (credenciales según `git-credentials`).

### Formato de entrada en README.md

```markdown
## YYYY-MM-DD — Cargo de la oferta

- **URL:** https://...
- **Commit:** `abc1234`
- **Base:** `CV_Base.docx`
- **PDF:** `CV_Axel_Pfingsten_Arpe.pdf`
- **Keywords ATS:** palabra1, palabra2, palabra3, palabra4, palabra5
```

## 3. Respuesta al usuario

En **español**: resumen nuevo, keywords ATS, bullets tocados, URL y hash del commit.

## Fuera de alcance

- No subir secretos (`.github/credentials.txt`).
- No reescribir todo el historial: solo perfil + bullets de mayor match.
- No sobrescribir `CV_Base.docx` con textos tailor-made de una sola oferta.
