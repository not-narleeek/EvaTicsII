# Notas del modelo económico — qué cambió y qué pegar en el informe

Fuente: `excel/PedioLink_Flujo_Caja.xlsx` (generado por `excel/generar_excel.py`; fórmulas verificadas contra el motor con recálculo LibreOffice, VAN normal idéntico al centavo). Hipótesis declaradas en la hoja `Supuestos` (SAM calificado = 38 = 30% de los 128 RM, editable).

## 1. Hallazgo central (para caps. 17-20)

La Tabla 6 del Word era **ingresos ×10 sin sustento**: exigía ~100 instituciones activas, pero el cap. 5 declara 2→10. Con las hipótesis declaradas del propio informe, **el proyecto no alcanza equilibrio operativo en ningún escenario de 5 años**:

| Indicador (Normal, estructura BASE) | Informe decía | Modelo recalculado |
|---|---|---|
| Ingresos año 5 | 2.700 k | **279,5 k** (10 inst. × 26,4k + impl + adicionales) |
| EBITDA año 1 → 5 | −264 → +1.600 | **−433 → −433 k** (siempre negativo) |
| VAN @ Ke | +380 k | **−1.937 k** |
| TIR | 22% | **No existe** (flujos siempre negativos) |
| PRI simple / descontado | 3,5 / 4,1 años | **No recupera** |
| Déficit de caja máximo | — | **−2.731 k** |
| Ke CAPM | 11,4% | **14,9%** (5,0 + 1,15×6,0 + 3,0) |

Escenarios (VAN a Ke propia):

| | Pesimista | Normal | Optimista | Normal-Ajustada | Optimista-Ajustada |
|---|---|---|---|---|---|
| VAN | −2.366 k | −1.937 k | −1.500 k | −1.231 k | −702 k |
| EBITDA año 5 | −613 k | −433 k | −120 k | −203 k | **+110 k** |
| VAN con valor terminal (g=3%) | — | — | — | — | ≈ −364 k |

## 2. Por qué no cierra y qué lo haría cerrar

Punto de equilibrio (instituciones activas, costos año 3) vs. 10 capturables en la hipótesis normal:

| Estructura | Precio 2.200 | Precio 3.000 |
|---|---|---|
| BASE (11 personas) | **22,6** | 16,3 |
| AJUSTADA (7 personas, coworking, socios sin sueldo año 1) | **14,9** | 10,8 |

**Condiciones de viabilidad** (materia para el análisis crítico del cap. 20): captura sostenida ≥ 15-23 instituciones (según estructura y precio), o duplicar el margen por institución (más volumen de estudios, precio en el tramo alto, canal white-label/API del cap. 6), o costos fijos −40% sostenido. Además: financiar con subsidios + aportes, **no con deuda al 12%** (el escudo tributario APV es de solo 2,7k; el servicio de la deuda profundiza el déficit).

## 3. Doble conteo detectado en el cap. 10 vs. 12 (corregir en el Word)

- "Equipamiento cloud año 1: 15.000" (cap. 10) **y** "Cloud AWS 3.500/mes" (cap. 12) — el modelo separa: base 2.500/mes + variable 1,50/estudio.
- "Contratación equipo: 50.000" (cap. 10) **y** remuneraciones de 11 personas (cap. 12) — en el modelo la contratación es costo de reclutamiento (gasto diferido), no salario duplicado.

## 4. Qué pegar en cada capítulo

| Capítulo | Reemplazar por |
|---|---|
| 17 | Tabla 6 → hoja `Flujo de Caja` (ingresos 45,3 / 103,8 / 162,4 / 221,0 / 279,5 k); EERR y Balance de las hojas `Estado Resultados` y `Balance` (patrimonio negativo desde año 1 = señal de estructura de capital insuficiente; déficit de caja año 1 ≈ −460 k) |
| 18 | CAPM con Ke **14,9%** citando fila/fecha exacta de Damodaran; VAN normal −1.937k; VAN ajustado esperado (0,25/0,50/0,25) −1.935k; APV −1.935k; TIR inexistente; PRI no recupera |
| 19 | Tabla de escenarios de la hoja `Escenarios` + puntos de equilibrio de la §2 |
| 20 | Conclusión honesta: bajo las hipótesis declaradas el proyecto **no es invertible en 5 años**; la decisión queda condicionada a las palancas de la §2 (es exactamente el "análisis crítico" que pide la guía) |
| Figura 4 | Flujo corregido: −285 / −502,9 / −497,3 / −495,3 / −497,1 / −453,2 (k USD) |

## 5. Cómo probar hipótesis alternativas

1. Editar celdas amarillas de `Supuestos` (captura, precio, cloud, inversión, beta…).
2. Las hojas `Flujo de Caja` y `Evaluacion` recalculan solas.
3. Para las 5 columnas de `Escenarios`: `python3 excel/generar_excel.py` tras editar `ESCENARIOS` en el script.

**Decisión pendiente del grupo:** (a) mantener hipótesis y presentar la no-viabilidad con condiciones (recomendado: es defendible en la defensa), o (b) cambiar hipótesis (captura/precio/estructura) para obtener VAN positivo — si eligen (b), las nuevas hipótesis deben ser defendibles ante preguntas.
