# PedioLink — Evaluación de Proyectos TIC (2S-2026)

Perfil de evaluación de un SaaS de apoyo a la interpretación de ECG pediátricos (DSP + ML, suscripción institucional B2B). Curso: Evaluación de Proyectos TIC, Sección 2 — Prof. Jorge Elliott, UDP. Grupo de 4 estudiantes.

**Entrega: lunes 9 de noviembre 2026, 23:59 (CANVAS).** Defensas individuales: 11, 17, 20 nov / 1, 4 dic (incluye *elevator pitch* de 60 s).

## Estado

Informe Word en revisión con 30 comentarios del grupo (ver `docs/comentarios-revision.md`). Verificación punto por punto contra la guía: **`docs/verificacion-cumplimiento.md`** — incluye hallazgos numéricos (CAPM, VAN, TIR, consistencia ingresos↔instituciones). Plan de trabajo con dueños: **`docs/todos.md`**.

## Entregables CANVAS (los 4 exigidos)

| # | Entregable | Estado | Dónde |
|---|---|---|---|
| 1 | Informe Word/PDF (20 puntos de la guía) | ⚠️ En corrección | `PedioLink_Informe_PEP(1).docx` → copia final en `informe/` |
| 2 | **Excel** con flujo de caja y evaluación económica | ✅ `PedioLink_Flujo_Caja.xlsx` (caso viable: VAN +323k, TIR 21,9%, horizonte 10 años; fórmulas vivas verificadas) — detalles y trazabilidad en `docs/excel-notas.md` | `excel/` |
| 3 | PowerPoint de presentación | ❌ No existe | `presentacion/` |
| 4 | Anexos con información soportante | ⚠️ Bibliografía APA por capítulo lista (`anexos/fuentes/bibliografia-por-capitulo.md`); faltan capturas y respaldos | `anexos/` |

## Estructura

```
├── PedioLink_Informe_PEP(1).docx   # informe en revisión (fuente)
├── PEP-TallerfFinal-2S2026-CA02.pdf# guía del profesor (20 puntos exigidos)
├── links.txt                       # fuentes web usadas en el informe
├── docs/
│   ├── verificacion-cumplimiento.md# matriz 20 puntos: estado, evidencia, acciones
│   ├── comentarios-revision.md     # los 30 comentarios del docx, por capítulo
│   └── actas/                      # acuerdos del grupo
├── informe/                        # versión final Word/PDF para CANVAS
├── excel/                          # Supuestos · Flujo de Caja · EERR · Balance · Evaluación · Escenarios
├── presentacion/                   # PPT + elevator pitch (60 s)
└── anexos/
    ├── fuentes/                    # fuentes citadas, capturas, reportes BCN/MINSAL
    └── cotizaciones/               # cotizaciones reales (arriendo, cloud, banco, legal)
```

## Prioridades antes del 9-nov (detalle en `docs/verificacion-cumplimiento.md`)

1. **P0 — ✅ Hecho (caso viable, opción b):** Excel completo con VAN +323k, TIR 21,9% @ Ke 14,9% corregida, PRI 6,5 años; cifras para los caps. 17-20 en `docs/excel-notas.md`.
2. **P0 — ✅ Hecho:** hojas `Supuestos`, `Flujo de Caja`, `Estado Resultados`, `Balance`, `Evaluacion` + `Escenarios`.
3. **P1 — Barrido de consistencia:** aplicar en todo el cuerpo la decisión del 29-oct (retirar ISP Clase I, meta de 3 regiones) y del 02-nov (dataset ZZU reemplaza a Leipzig), y resolver la contradicción de los "kits IoT" contra el modelo SaaS puro.
4. **P1 — Gráficos:** BPMN y layout (hoy solo texto), logo (hoy solo descrito), gráficos de mercado, organigrama en página horizontal, CANVAS con código de color.
5. **P2 —** CLP/UF en inversiones y financiamiento, cotizaciones reales, bibliografía (hay citas sin lista de referencias), completar portada.

## Flujo de trabajo

- Rama `main` = última versión entregable. Correcciones por capítulo en ramas `fix/cap-XX-*`.
- Tras editar el Word: actualizar TOC (clic derecho → *Actualizar campos*) antes de exportar PDF.
- Los comentarios del docx son la lista de pendientes; cerrar cada uno marcándolo resuelto en Word.
