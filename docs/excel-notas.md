# Notas del modelo económico — caso VIABLE (opción b adoptada)

Fuente: `excel/PedioLink_Flujo_Caja.xlsx` (generado por `excel/generar_excel.py`; fórmulas vivas verificadas contra el motor con recálculo LibreOffice — VAN, TIR y PRI coinciden a precisión de máquina). Hipótesis declaradas y editables en la hoja `Supuestos`.

## 1. Resultado del caso viable

| Indicador | Valor |
|---|---|
| VAN normal (10 años, Ke CAPM 14,9%) | **+323 k USD** |
| TIR | **21,9%** (+7,0 pp sobre Ke) |
| PRI simple / descontado | **6,5 / 8,6 años** |
| EBITDA | positivo desde el año 4 (+113 k); año 10: +818 k |
| VAN ajustado (esperado, prob. 0,25/0,50/0,25) | **+204 k USD** |
| VAN corte a 5 años | −522 k (el SaaS aún está en ramp-up → por eso el horizonte es 10 años, que la guía permite expresamente) |

Escenarios: Pesimista −1.685 k · **Viable +323 k** · Optimista +1.853 k · Diagnóstico original (2→10 inst., 11 personas): −2.968 k, descartado.

## 2. Palancas del caso viable y su trazabilidad (para defender en preguntas)

| Palanca | Valor | Trazabilidad |
|---|---|---|
| Horizonte | 10 años | Guía: "Flujo de Caja mínimo a cinco años **u otro horizonte que Ud. considere de interés**" |
| Precio | 2.450 USD/mes | Mix ponderado declarado del propio rango del informe: 30%×3.000 + 50%×2.500 + 20%×1.500 |
| Volumen | 300 estudios/mes por institución | Supuesto declarado (hospital pediátrico referencial); valida el catastro del SAM |
| White-label/API | 10% de la suscripción desde año 3 | Ya declarado en cap. 6 del informe ("línea de ingresos complementaria") |
| Expansión nacional | desde año 6; 37 inst. año 10 ≈ 32% del universo calificado (~115 = 30% de 382) | Decisión del 29-oct: expansión según criterios, no meta arbitraria |
| Cloud | 0,80 USD/estudio | Valor optimista del propio informe, justificado por committed-use a volumen |
| Costos | Estructura ajustada: 7 personas año 1 (socios con sueldo parcial), ~14 al año 10 | Guía cap. 12: "Tratar de minimizar sus costos fijos" |
| Año 1 | Operación parcial: 3,5 meses/institución, 55% de los costos fijos | Lanzamiento mes 8-9 según carta Gantt |
| Financiamiento | 785 k: aportes 235 k + CORFO 150 k + Banca Desarrollo 400 k (12%, 10 años, 3 de gracia) | El banco comercial al 12% corto plazo destruía valor; Banca Desarrollo existe en Chile (agentes CORFO) |
| Ke | 14,9% (sin trucos) | CAPM corregido con los insumos del informe |

Punto de equilibrio (año 5): **11,4 instituciones** con la estructura ajustada a precio 2.450 y 300 estudios (la estructura original de 11 personas exigía 24,9). El caso viable llega a 20 en el año 5 — sobre el equilibrio.

## 3. Qué pegar en cada capítulo del informe

| Capítulo | Cambio |
|---|---|
| 1 | Horizonte de evaluación: 10 años (justificar con la guía) |
| 6 | White-label/API: la línea ya está declarada; el modelo le asigna 10% de la suscripción desde año 3 |
| 11 | **Reescribir**: aportes 235 k + CORFO 150 k + Banca Desarrollo 400 k = 785 k; descartar banco comercial argumentando el VAN (responde a comentarios #12, #15); declarar línea de capital de trabajo comprometida (~430 k) para el déficit del ramp-up |
| 12 | Reemplazar la estructura de 11 personas por la ajustada de 7 (tabla de Supuestos), manteniendo los rubros |
| 17 | Nueva tabla de flujo (10 años, abajo) + EERR y Balance de las hojas del Excel; explicar el patrimonio negativo año 1-3 (amortización no-caja de intangibles en ramp-up, se revierte año 5-6) |
| 18 | Ke 14,9%; VAN +323 k; VAN ajustado esperado +204 k; TIR 21,9%; PRI 6,5 / 8,6 años |
| 19 | Escenarios de la hoja `Escenarios` + punto de equilibrio + valor terminal (solo optimista: EBITDA año 10 > 0) |
| 20 | Conclusión: proyecto viable **condicionado** a las palancas de la §2; sensibilidad: captura y precio son las variables críticas (pesimista −1.685 k) |

## 4. Cifras para la Figura 4 (flujo del proyecto, k USD)

| Año | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Flujo | −285 | −175,5 | −201,5 | −108,2 | +42,8 | +230,4 | +301,7 | +391,1 | +484,0 | +525,7 | +1.027,4 |

## 5. Probar alternativas

1. Editar celdas amarillas de `Supuestos` → `Flujo de Caja` y `Evaluacion` recalculan solos.
2. Para las 4 columnas de `Escenarios`: editar `ESCENARIOS` en el script y correr `python3 excel/generar_excel.py`.

Advertencia para la defensa: si cambian hipótesis para "mejorar" el VAN, cada cambio debe ser defendible (fuente de mercado o referencia al informe). El pesimista −1.685 k no es un error: muestra el piso real del proyecto y sostiene el análisis de riesgo.
