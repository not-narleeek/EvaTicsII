# Barrido de consistencia — cambios aplicados al informe (02-nov)

Ejecutado sobre `PedioLink_Informe_PEP(1).docx` (XML validado, render verificado). Aplica las decisiones del 29-oct (retirar ISP, 3 regiones, Leipzig→ZZU, precisión no demostrada) y del 02-nov (dataset ZZU), y alinea el informe con el modelo viable (`excel/PedioLink_Flujo_Caja.xlsx`). Los 30 comentarios del Word siguen intactos — cerrarlos al revisar.

## Cap. 1 — Introducción
- Horizonte: 5 → **10 años** (con corte de referencia a 5), citando la facultad explícita de la guía.

## Cap. 3 — CANVAS
- Estructura de costos alineada al caso viable: 7 personas (12,5 k/mes), cloud base 2,5 k, coworking 900, total fijo ≈ 21,6 k/mes (antes: 11 personas, 37 k/mes, datos inconsistentes).

## Cap. 4 — Mercado
- Suscripción de referencia 2.200 → **2.450 USD/mes** (mix ponderado 30/50/20 del rango propio); ingreso por institución 26,4 k → 29,4 k/año.

## Cap. 5 — Situación
- Tabla de participación: 2/4/6/8/10 → **2/5/9/14/20** instituciones; columna regional recalculada sobre SAM calificado 38 (5,3% → 52,6%).

## Cap. 6 — Estrategia
- FODA: "Leipzig" → **ZZU (Tan et al., 2025)**; "B2B2C probado" → "SaaS B2B con referencias"; amenaza "Cambios regulatorios ISP" → "Regulación de software médico en evolución"; debilidad "Demora en certificación ISP" → "Sin validación clínica prospectiva".
- Estrategia: pilotos con hospitales/clínicas RM (antes CESFAM/ISAPRE); expansión por criterios (antes Valparaíso/Biobío en años 2-3); white-label/API cuantificado ≈10% desde año 3.

## Cap. 7 — Productivo
- Sin bodega ni kits (SaaS puro); coworking año 1-2, oficina 100 m² desde año 3; cloud 2,5 k base + 0,80/estudio; sin "sala de servidores".

## Cap. 8 — Técnica
- Transmisión definida: HTTPS (TLS 1.3), interoperabilidad HL7 v2/FHIR R4 (cierra #6; TLS revisado #8).
- Dataset **ZZU** con cita (reemplaza Leipzig; cierra #7 y #29); métricas declaradas como objetivos de diseño, no resultados demostrados.

## Cap. 9 — Gantt
- Actividad 3: "Certificación ISP Clase I" → **"Dataset ZZU + validación retrospectiva" (M2-M5)**; convenios piloto hospital/clínica (M3-M6); piloto 50 pacientes M6-M7; sin fila de kits IoT; lanzamiento mes 8. Tabla 2 y narrativa consistentes con `fig2_gantt.png`.

## Cap. 10 — Inversiones
- "Certificación ISP + asesoría legal" → "Validación clínica + asesoría legal" (35 k, misma partida); recurrente 70 k/año en todo el horizonte.

## Cap. 11 — Financiamiento
- Nueva Tabla 4: aportes 235 k (30%) + CORFO 150 k (19%) + **Banca Desarrollo 400 k (51%; 12%, 10 años, 3 de gracia)** = 785 k. Justificación reescrita sin tono genérico (#13) y con respuesta a "¿por qué este banco?" (#15): el crédito comercial destruía valor en el ramp-up. Nueva alternativa descartada (e).

## Cap. 12 — Costos
- Tabla 5 reconstruida: 7 personas 12,5 k / cloud base 2,5 k / coworking 900 / marketing 3,0 k / servicios 1,0 k / software 0,8 k / otros 0,9 k = **21,6 k/mes (259,2 k año 1)**; variable 0,80 USD/estudio (300 estudios → 240/mes).

## Cap. 13 — Legal
- ISP: verificación con asesor regulatorio antes de puesta en marcha; cronograma no condicionado a tramitación (retiro de "Decreto Exento 25/2026" sin fuente); Ley REP/kits eliminada; Ley 21.719 y su agencia explícitas con entrada gradual (#18); justificación SPA directa (cierra #17).

## Cap. 14 — Personal
- 11 → **7 personas** (4 socios a sueldo parcial + 3 contrataciones); contabilidad y legal externalizadas (#19); escala a ~14 al año 10. Consistente con `fig3_organigrama.png` (regenerar: el PNG actual aún muestra 8 cajas → ver pendiente).

## Cap. 15 — Localización
- Coworking años 1-2 (≈900/mes) y oficina 100 m² desde año 3 (referencial 2.500, a validar — #21/#22); sin Omron ni kits.

## Cap. 16 — Ambiental
- Sin Ley REP ni kits (SaaS puro, cero residuos propios); se mantiene el compromiso AWS São Paulo + reporte anual (cierra #23).

## Cap. 17 — Flujo
- Tabla 6 recalculada (miles USD): ingresos 38,8/160,5/325,6/522,3/761,0; EBITDA −105,5/−131,5/−38,2/+112,8/+300,4; flujo −175,5/−201,5/−108,2/+42,8/+230,4; impuestos 0 (arrastre de pérdidas). Equilibrio operativo año 4; financiero año 7.

## Cap. 18 — Evaluación
- Ke **14,9%** (corrección del error aritmético); VAN **+323 k** a 10 años; TIR **21,9%** (+7,0 pp); PRI 6,5/8,6; corte a 5 años −522 k explicado; VAN ajustado esperado +204 k (cierra #26).

## Cap. 19 — Sensibilización
- Tabla 8 con escenarios del modelo: instituciones 1/12, 2/20, 3/25; precio 1.500/2.450/3.000; VAN −1.685/+323/+1.853; TIR n.r./21,9%/49,4%; PRI —/6,5/4,1; Ke común 14,9%. Matriz antigua (hecha para el modelo previo) reemplazada por referencia a las hojas `Evaluacion`/`Escenarios` + recomendación Monte Carlo (cierra #27 parcial).

## Cap. 20 — Conclusión
- Cifras sin fuente eliminadas ("30 hospitales", "8.000 pacientes", "un hospital por mes", "reduce 20%"); retorno actualizado a VAN +323 k / TIR 21,9% / PRI 6,5; debilidad Leipzig → ZZU con convenios locales; riesgo regulatorio sin certificación específica (cierra #28 parcial).

## Pendiente que queda del barrido

1. ~~`fig3_organigrama.png` aún dibuja 8 cajas~~ — ✅ Hecho (regenerado a 7 personas y centrado).
2. ~~Insertar los gráficos de `informe/graficos/` en el Word~~ — ✅ Hecho (10 figuras insertadas consecutivamente con sus referencias y captions).
3. Fila y fecha de la beta Damodaran (cap. 18).
4. Cotización real de coworking/oficina y cálculo AWS (ítems 24-25).
