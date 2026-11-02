# Verificación de cumplimiento — PedioLink vs. guía PEP 2S-2026

Contraste entre `PEP-TallerfFinal-2S2026-CA02.pdf` (guía, 20 puntos) y `PedioLink_Informe_PEP(1).docx` (revisión del 2-nov-2026), incluyendo los 30 comentarios del grupo (`docs/comentarios-revision.md`).

**Resumen:** 20/20 capítulos presentes en el índice del informe. Contenido: 6 conformes, 12 parciales, **2 rehacer** (17 y 18). **Los 4 entregables CANVAS solo tienen 1:** falta el Excel (que el propio Word cita 5 veces), el PowerPoint y los anexos. No hay bibliografía pese a haber citas en el texto.

Leyenda: ✅ cumple · ⚠️ parcial/pendiente · ❌ rehacer o ausente.

## 1. Matriz punto por punto

| # | Punto de la guía | Estado | Evidencia y brechas | Comentarios |
|---|---|---|---|---|
| 1 | Introducción: descripción, objetivos g/e, alcances | ⚠️ | Estructura correcta y ya reeditada según acuerdo del 29-oct; el cuerpo (caps. 6, 8, 9, 13, 19, 20) aún NO refleja esas decisiones | #0 (2/5, previo), #1 |
| 2 | Definición del proyecto: producto/servicio y valor | ⚠️ | Producto, componentes y propuesta de valor presentes; nivel de detalle técnico por resolver (pregunta al profe); contradicción "no incluye equipos" vs. kits (caps. 7, 9, 15, 16) | #2 |
| 3 | Modelo de negocios CANVAS | ⚠️ | Figura 1 presente; falta código de color Valor↔Segmentos; cifras del canvas (37k USD/mes) no calzan con cap. 12 (40,5k USD/mes) | #3 |
| 4 | Estimación de mercado: dimensionar y proyectar demanda | ⚠️ | TAM-SAM-SOM con fuentes (BCN 2025, CAGR sectoriales); SAM queda sin conteo calificado; SOM (2 inst. año 1) no coincide con el 3% usado en escenarios (cap. 19); sin proyección de demanda en estudios/pacientes | — |
| 5 | Situación de mercado: competidores, cuotas, ciclo de vida, posicionamiento, canales, **proveedores** | ⚠️ | Competidores (Philips, GE, Atrys, Cardiowapp), tabla de participación, ciclo de vida, posicionamiento, canales y posventa ✓; **proveedores y suministros sin sección propia** (solo AWS/Omron dispersos); sin gráficos | #4 |
| 6 | Estrategia comercial: FODA, PEST, logo y nombre | ⚠️ | FODA en tabla y PEST en texto (→ cuadrante visual); marca e isotipo solo **descritos en texto, sin imagen**; FODA aún lista Leipzig y "B2B2C probado"; estrategia menciona expansión a 3 regiones (decisión: retirar) y pilotos CESFAM que contradicen el cliente declarado (hospitales/clínicas) | #5 |
| 7 | Plan productivo: operación, equipos, **BPMN y layout** | ⚠️ | Procesos y tecnología descritos en texto; **faltan los diagramas BPMN y layout** (la guía los pide explícitamente); bodega con 200 kits contradice el SaaS puro | #10 |
| 8 | Solución técnica: arquitectura, componentes, justificación de opciones | ✅ | Capa por capa, pipeline DSP, criterios de selección y alternativas descartadas; pendiente: definir HTTPS vs HL7, reemplazar Leipzig (PTB-XL/MIT-BIH son adultos → sintético + convenio local), revisar TLS | #6, #7, #8, #29 |
| 9 | Carta Gantt-PERT: precedencias, ruta crítica, holguras | ⚠️ | Figura 2 + tabla con precedencias, holguras y ruta crítica ✓; mejorar especificidad de la figura; certificación ISP M3-M6 (4 meses) vs. cap. 13 "≈6 meses" | #9 |
| 10 | Inversiones y programa en el tiempo | ⚠️ | Tabla 3 con montos y meses ✓; falta equivalencia CLP/UF; "capital de trabajo 50k" puede duplicarse con costos del flujo — verificar doble conteo | #11 |
| 11 | Financiamiento: modalidades y justificación | ⚠️ | Tabla 4 con 3 fuentes y alternativas descartadas ✓; falta CLP, condiciones reales de BancoEstado (tasa vigente citable), verificar reglas CORFO; reescribir tono "muy IA" | #12–#15 |
| 12 | Costos: fijos/variables, minimizar fijos | ⚠️ | Tabla 5 suma correcta (40,5k/mes) pero contradice cap. 3 (37k) y Tabla 6 (444k/año vs. 486k declarado); costo variable 1,50 USD/estudio sin fuente; sin cotizaciones ni referencias reales | #16 |
| 13 | Aspectos legales: forma societaria y marcos | ⚠️ | SPA justificada (simplificar redacción); Ley 19.628/21.719 citada → explicitar fase de entrada en vigencia y agencia aún no operativa; **"Decreto Exento 25/2026" sin fuente verificable**; si se retira el ISP (decisión #1), reescribir este capítulo y su impacto en Gantt/riesgos | #17, #18 |
| 14 | Personal: calificación, organigrama, perfiles | ⚠️ | 11 personas con perfiles ✓; organigrama ilegible (imagen 2046×1013 comprimida en texto vertical) → página apaisada; definir qué se externaliza (contabilidad ya se menciona en cap. 12) | #19, #20 |
| 15 | Localización con valores actualizados e impactos | ⚠️ | Justificación cualitativa ✓; arriendo 2.500 USD/150 m² sin cita (≈0,53 UF/m² — validar con portalinmobiliario); usar una oficina real como referencia | #21, #22 |
| 16 | Aspectos ambientales: SEIA, Ley 19.300 | ⚠️ | Exención SEIA bien argumentada ✓; el compromiso Ley REP sobre "kits electrónicos" contradice el modelo sin hardware → eliminar o reescribir | #23 |
| 17 | Flujo 5 años + EERR y balance 3 años consistentes | ❌ | Tabla 6 con inconsistencias graves (ver §2); EERR y balance **remitidos a un Excel que no existe**; rehacer desde cero | #24, #25 |
| 18 | Evaluación: TIR, PRI, VAN normal **y ajustado**, CAPM con beta Damodaran | ❌ | CAPM con insumos propios da 14,9% (no 11,4%); VAN/TIR/Payback no reproducibles (ver §2); **falta el VAN ajustado** (pedido explícito); beta 1,15 y sector "HealthTech" → citar fila exacta de Damodaran | #26 |
| 19 | Sensibilización: @Risk/Crystal Ball o 3 escenarios | ⚠️ | 3 escenarios ✓ (vía "menor ponderación"); matriz bidimensional remitida al Excel inexistente; tasa de captura 3% inconsistente con SOM; Monte Carlo solo mencionado; rehacer tras corregir flujo | #27 |
| 20 | Conclusión: síntesis, rentabilidad, análisis crítico | ⚠️ | Síntesis + análisis crítico con debilidades y mejoras ✓; cifra "30 hospitales / 8.000 pacientes / un hospital por mes" sin fuente ni consistencia con caps. 4–5; faltan citas | #28 |

## 2. Hallazgos numéricos (verificados por recálculo)

El flujo declarado (miles USD): `-285, -334, -170, +178, +572, +1.098`.

| Indicador | Informe dice | Recálculo | Observación |
|---|---|---|---|
| Ke (CAPM) | 11,4% | **14,9%** | 5,0% + 1,15×6,0% + 3,0% = 14,9%. Error aritmético con sus propios insumos |
| VAN | ≈380k | **418k @11,4%** · **289k @14,9%** | Aún con la tasa corregida el VAN sigue positivo |
| TIR | ≈22% | **26,2%** | — |
| Payback simple | 3,5 años | **4,04 años** | Cruce entre años 4 y 5 |
| Payback descontado | 4,1 años | **4,35 años @11,4%** | — |

**Consistencia ingresos↔instituciones (el problema mayor):**

| Año | Instituciones activas (cap. 5) | Ingreso implícito (suscripción 26,4k/inst.) | Ingreso en Tabla 6 | Brecha |
|---|---|---|---|---|
| 1 | 2 | ≈69k (incl. 2 implementaciones de 8k) | 180k | ×2,6 |
| 5 | 10 | ≈264k | 2.700k | **×10** |

La conclusión además habla de "un hospital por mes", contradiciendo la tabla del cap. 5 (2 incorporaciones netas anuales). Todo el modelo económico debe reconstruirse desde una única hoja de supuestos (cantidad de clientes por año × precio × mezcla de ingresos) de la que se derivan flujo, EERR, balance y evaluación.

Otras inconsistencias menores: costos fijos año 1 = 40,5k/mes (cap. 12) vs. 37k/mes (cap. 3) vs. 444k/año en Tabla 6 (vs. 486k declarado en cap. 12); "tasa captura año 1: 3%" en escenarios vs. 2/128 ≈ 1,6% del SOM.

## 3. Entregables CANVAS

| Entregable | Estado |
|---|---|
| Word/PDF | ⚠️ en corrección; portada con placeholders (`[número a definir]`, `[nombres a definir]`) y TOC sin actualizar |
| Excel (flujos y evaluación) | ❌ **No existe.** El Word referencia hojas `Supuestos`, `Flujo de Caja`, `Estado Resultados`, `Balance`, `Evaluacion` → construirlas con esos nombres exactos |
| PowerPoint | ❌ No existe. Incluir *elevator pitch* de 60 s para la defensa |
| Anexos | ❌ Solo `links.txt`. Mover a `anexos/fuentes/` con las citas completas |

## 4. Bibliografía

Hay citas en formato autor-año (BCN 2025; The Insight Partners 2025; Business Research Insights s. f.; Leone et al. 2024; Damodaran ene-2025; MINSAL) **pero no existe capítulo de Referencias**. Agregarlo con `links.txt` como base y formato APA.

## 5. Plan de acción sugerido (hasta el 9-nov)

1. **P0:** definir supuestos comerciales únicos (clientes/año consistentes con cap. 4–5) → reconstruir Tabla 6 → corregir CAPM (14,9% o ajustar insumos) → recalcular VAN **normal y ajustado**, TIR, PRI → construir el Excel real.
2. **P0:** resolver con el profe: nivel de detalle del cap. 2 (#2), financiamiento (#12), si el ISP entra o sale (#1 vs. caps. 9/13/19).
3. **P1:** barrido ISP/Leipzig/3-regiones/kits en todo el cuerpo; gráficos faltantes (BPMN, layout, logo, mercado, organigrama apaisado, CANVAS color); completar SAM calificado.
4. **P2:** CLP/UF, cotizaciones reales (arriendo, cloud, banco, legal), bibliografía, portada, TOC.

*Recálculos reproducibles:* flujos de la Tabla 6; VAN por suma de `F_t/(1+r)^t`; TIR por bisección; payback por interpolación lineal del acumulado.
