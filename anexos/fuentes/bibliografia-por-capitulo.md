# Bibliografía por capítulo — fuentes de `links.txt`

Mapeo según Donovan (WhatsApp, 02-nov): *"El primero si no me equivoco en la 3, los siguientes 3 en la 4 y los últimos 4 en la 5"* — los saltos de línea de `links.txt` separan los tres grupos.

## Mapa de uso

| Cap. del informe | Fuentes (orden de `links.txt`) | Qué respaldan |
|---|---|---|
| **3 — Modelo de Negocios (CANVAS)** | 1. BCN Reporte Regional 2025 | 227 hospitales y 155 clínicas en Chile; 45 y 83 en la RM (sección 4.4) |
| **4 — Estimación de Mercado** | 2. The Insight Partners · 3. Business Research Insights · 4. MINSAL ENS 2030 | CAGR salud digital 25,7% (2025-2031); mercado IA-ECG USD 1.240M→3.690M, CAGR 13,7%; modelo de salud digital del MINSAL |
| **5 — Situación de Mercado** | 5. Philips · 6. GE HealthCare · 7. Atrys · 8. Cardiowapp | Competidores: DXL en PageWriter TC35; Marquette 12SL en MAC 5; telecardiología remota; gestión de ECG |
| **6 (FODA), 8 (solución técnica), 20 (conclusión)** | 9. Tan et al. 2025 — dataset **ZZU** | Entrenamiento/validación del clasificador: base 100% pediátrica y pública (sustituye a Leipzig, decisión 02-nov; responde a comentarios #7 y #29) |

## Referencias en formato APA 7

**Capítulo 3**

> Biblioteca del Congreso Nacional de Chile. (2025). *Reporte Regional 2025: Región Metropolitana de Santiago* (sección 4.4, Salud). https://www.bcn.cl/siit/reportesregionales/reporte_final.html?unidad=regional&anno=2025&cod_region=13

**Capítulo 4**

> The Insight Partners. (2025). *Digital health market*. https://www.theinsightpartners.com/pr/digital-health-market

> Business Research Insights. (s. f.). *AI ECG analysis market report*. https://www.businessresearchinsights.com/market-reports/ai-ecg-analysis-market-115488

> Ministerio de Salud de Chile. (2023). *Estrategia Nacional de Salud al 2030*. https://degreyd.minsal.cl/wp-content/uploads/2023/12/Estrategia-Nacional-de-Salud-al-2030.pdf

**Capítulo 5**

> Philips Chile. (s. f.). *PageWriter TC35 Cardiograph*. https://www.philips.cl/healthcare/product/860437/pagewriter-tc35-cardiograph

> GE HealthCare. (s. f.). *MAC 5 Resting ECG*. https://www.gehealthcare.com.sg/en/products/diagnostic-ecg/resting-ecg/mac-5-resting-ecg

> Atrys Chile. (s. f.). *Telecardiología*. https://atrys.cl/telecardiologia/

> Cardiowapp. (s. f.). *Plataforma*. https://www.cardiowapp.cl/plataforma

**Usadas en otros capítulos**

> Damodaran, A. (2025). *Betas by sector (US)*. NYU Stern School of Business. https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html — **PENDING: citar fila exacta del sector y fecha de la tabla usada (cap. 18; la guía da este link)**

> Tan, J., Fan, H., Luo, J., Zhou, Y., Wang, N., Wang, X., Liu, G., Liu, C., & Wang, Z. (2025). A pediatric ECG database with disease diagnosis covering 11643 children. *Scientific Data, 12*, 867. https://doi.org/10.1038/s41597-025-05225-z — **dataset ZZU (reemplaza a Leipzig, decide 02-nov): 11.643 niños del Primer Hospital Afiliado de la Universidad de Zhengzhou, 2018-2024; 14.190 registros ECG, 12.334 de 12 derivaciones, con diagnóstico por enfermedad. Datos en Figshare: https://doi.org/10.6084/m9.figshare.27078763**

## Cómo citar en el texto

- Cap. 3: "(BCN, 2025, sección 4.4)" — ya está bien usado.
- Cap. 4: "(The Insight Partners, 2025)", "(Business Research Insights, s. f.)", "(MINSAL, 2023)".
- Cap. 5: describir a cada competidor con cita: "Philips incorpora el algoritmo DXL en la línea PageWriter (Philips, s. f.)".
- Cap. 18: "(Damodaran, 2025)" con fila y fecha.
- Caps. 6/8/20: "(Tan et al., 2025)" — el dataset ZZU sustituye a Leipzig en FODA, entrenamiento del pipeline y conclusión.

## Pendientes para cerrar la bibliografía

1. Fila y fecha exactas de la beta en la tabla de Damodaran (captura → `anexos/fuentes/`).
2. Capturas PDF de cada fuente (guardar en esta carpeta como respaldo del anexo).
3. Retirar toda mención a "Leipzig Heart Center" / "Leone et al." en el Word (caps. 6, 8, 20) y reemplazar por ZZU: filtrar el texto por "Leipzig" y "Leone".
