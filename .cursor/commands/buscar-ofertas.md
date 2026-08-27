---
description: Flujo 1 — buscar ofertas ad-hoc, listarlas y guardarlas en ofertas/
alwaysApply: true
---

# Flujo 1: Buscar ofertas

Cuando el usuario pida **buscar ofertas**, **encontrar vacantes**, **listar trabajos** o similar (sin pedir aún postular), ejecutar este flujo.

## Alcance

- Perfil: enfermero APS / domiciliaria / SAR / procedimientos, según `CV_Base.docx`.
- Región: **Región Metropolitana (RM), Chile**.
- Ofertas **aún disponibles** o con plazo vencido de **como máximo 2 semanas** (los reclutadores a veces siguen recibiendo). Más de 14 días de cierre: no agregar.
- No hace falta match 100 %; sí ad-hoc al cargo.

## Pasos

1. Buscar en estos portales (priorizar volumen en salud / APS; recorrer varios, no solo uno):
   - **Generales Chile:** Computrabajo, Laborum, Indeed Chile, Trabajando.com, ChileTrabajos, Jooble, Blackboardjob, Mipleo, OpciónEmpleo, Yapo Empleos, ChileAtiende (avisos laborales), Trovit Empleo, Careerjet, SimplyHired (agregadores)
   - **Salud especializados:** ClinicalWork, portales/avisos de hospitalización domiciliaria (Medical Home, Home Medical Clinic, TeveuCI, etc. cuando publiquen), XinerLink / consultoras de staffing clínico
   - **Público / APS:** Empleos Públicos (Servicio Civil), Bolsa Nacional de Empleo (BNE), OMIL comunales, portales de corporaciones municipales de salud / CESFAM / CECOSF / SAR, sitios de Servicios de Salud Metropolitanos (Norte, Sur, Oriente, Occidente, Central), Hospitales de la red pública (concursos vigentes / Empleos Públicos)
   - **Redes clínicas privadas:** Ancora UC / UC CHRISTUS (Pandapé), Clínica Alemana, Clínica Las Condes, Red Salud UC CHRISTUS, Clínica Santa María, Clínica Dávila / Vespucio, Clínica Indisa, Bupa / Integramédica, Clínica Bupa Santiago, RedSalud, Clínica Bicentenario / Tabancura / Avansalud (cuando tengan “trabaja con nosotros”)
   - **Mutuales / seguros / ISL:** ACHS, Mutual de Seguridad, Instituto de Seguridad Laboral (ISL), Isapres (Banmédica, Colmena, Consalud, Cruz Blanca, Nueva Masvida, Vida Tres) — secciones de empleo o Computrabajo/Laborum corporativo
   - **Universidades / docencia clínica (si aparece enfermería APS):** portales de RR.HH. UC, U. de Chile, Usach, U. Central, UNAB, UDD, USS, UBO, etc.
   - **Redes y comunidades:** LinkedIn (empleos + posts #enfermería #APS #CESFAM), Facebook grupos de empleo salud Chile, Instagram de corporaciones municipales de salud
   - **Agencias / outsourcing salud:** Seniority, Workforce/EST, Progestion, consultoras que publiquen EU/TENS en RM
2. Verificar vigencia (fecha, “hace X horas/días”, plazo de postulación). Si el plazo ya pasó pero **≤ 14 días**, **igual incluirla** (regla `plazo-postulacion`).
3. Presentar al usuario un **listado numerado** (cargo, comuna, renta si hay, por qué encaja, URL).
4. **Guardar/actualizar** `ofertas/pendientes.md` con las ofertas nuevas (sin duplicar la misma URL).
5. Estado inicial de cada ítem: `pendiente`.

## Formato en `ofertas/pendientes.md`

```markdown
## OF-YYYYMMDD-NN — Título del cargo

- **Estado:** pendiente
- **URL:** https://...
- **Comuna / zona:** ...
- **Fuente:** Computrabajo | Laborum | Indeed | Trabajando | ChileTrabajos | ClinicalWork | Empleos Públicos | BNE | LinkedIn | Municipal/CESFAM | Ancora/UC | Clínica/Mutual | Agencia | …
- **Renta:** ... (si aparece)
- **Encaje:** 1–2 líneas vs CV_Base
- **Detectada:** YYYY-MM-DD
```

IDs: `OF-` + fecha + correlativo del día (`01`, `02`, …).

## No hacer en este flujo

- No adaptar el CV.
- No abrir postulación en el navegador.
- No marcar `postulada` aquí.
