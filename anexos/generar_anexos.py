#!/usr/bin/env python3
"""Genera PedioLink_Anexos.docx — Anexos con la información complementaria
soportante del informe de evaluación (entregable CANVAS 4).

Fuentes de verdad:
  - PedioLink_Informe_PEP_FINAL.docx (cuerpo principal)
  - PedioLink_Flujo_Caja.xlsx (modelo económico, caso viable)
  - docs/excel-notas.md (palancas y trazabilidad)
  - anexos/fuentes/bibliografia-por-capitulo.md (APA, mapeo por capítulo)

Uso: python3 anexos/generar_anexos.py
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PRIMARY = "0F4C81"
HEADER_FILL = "D9E2F3"

GRUPO = "Gustavo Castro · Carlos Jara · Fernando Llancao · Donovan Iturra"
CURSO = "Evaluación de Proyectos TIC — Sección 2 · Prof. Jorge Elliott"
FECHA = "Noviembre de 2026"


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def set_cell(cell, text, bold=False, size=9.5):
    cell.text = ""
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold


def tabla(doc, headers, rows, size=9.5):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        set_cell(t.rows[0].cells[j], h, bold=True, size=size)
        shade(t.rows[0].cells[j], HEADER_FILL)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            set_cell(t.rows[i].cells[j], str(val), size=size)
    doc.add_paragraph()
    return t


def para(doc, text, size=10.5, bold=False, italic=False, style=None, align=None):
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if align:
        p.alignment = align
    return p


def ref_apa(doc, texto):
    """Referencia APA 7 con sangría francesa."""
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.font.size = Pt(10)
    pf = p.paragraph_format
    pf.left_indent = Inches(0.4)
    pf.first_line_indent = Inches(-0.4)
    pf.space_after = Pt(6)
    return p


doc = Document()

# Estilo base
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)

# Pie de página
section = doc.sections[0]
footer = section.footer
fp = footer.paragraphs[0]
fp.text = "PedioLink — Anexos · " + CURSO + " · " + FECHA
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in fp.runs:
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)

# ============ PORTADA ============
para(doc, "Universidad Diego Portales", 14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "Facultad de Ingeniería", 12, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, CURSO, 11, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
doc.add_paragraph()
para(doc, "ANEXOS", 26, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "Información complementaria soportante del informe de evaluación", 13,
     align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
para(doc, "Proyecto PedioLink — Software de soporte diagnóstico de arritmias "
          "pediátricas vía ECG y machine learning", 12, italic=True,
     align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
doc.add_paragraph()
para(doc, "Grupo: " + GRUPO, 11, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "Entrega CANVAS — 9 de noviembre de 2026", 10, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ============ ÍNDICE DE ANEXOS ============
doc.add_heading("Contenido de los anexos", level=1)
indice = [
    ("Anexo A", "Bibliografía y fuentes por capítulo (APA 7)"),
    ("Anexo B", "Ficha técnica del dataset ZZU (Tan et al., 2025)"),
    ("Anexo C", "Fichas de competidores y alternativas en el mercado"),
    ("Anexo D", "Marco legal y regulatorio aplicable"),
    ("Anexo E", "Referencia de mercado público: licitación 1057390-86-LP25"),
    ("Anexo F", "Supuestos del modelo económico y trazabilidad de palancas"),
    ("Anexo G", "Detalle financiero del caso viable (flujo 10 años, CAPM, escenarios)"),
    ("Anexo H", "Programa de inversiones"),
    ("Anexo I", "Estructura de financiamiento y alternativas descartadas"),
    ("Anexo J", "Estructura de costos fijos del año 1"),
    ("Anexo K", "Precedencias y holguras — Carta Gantt / PERT"),
    ("Anexo L", "Referencias de precios (hipótesis declaradas del modelo)"),
    ("Anexo M", "Glosario de términos y siglas"),
]
for cod, titulo in indice:
    para(doc, f"{cod} — {titulo}", 11)
doc.add_paragraph()
para(doc, "Nota: los anexos complementan el informe principal (capítulos 1–20) y la "
          "planilla PedioLink_Flujo_Caja.xlsx (hojas Supuestos, Flujo de Caja, Estado "
          "Resultados, Balance, Evaluacion y Escenarios). Los valores monetarios se "
          "expresan en dólares estadounidenses (USD).", 9.5, italic=True)
doc.add_page_break()

# ============ ANEXO A: BIBLIOGRAFÍA ============
doc.add_heading("Anexo A — Bibliografía y fuentes por capítulo (APA 7)", level=1)
para(doc, "Fuentes utilizadas en el informe, agrupadas según el capítulo en que "
          "respaldan los antecedentes. Formato APA 7.", 10.5)

doc.add_heading("Capítulo 3 — Modelo de Negocios (CANVAS)", level=2)
ref_apa(doc, "Biblioteca del Congreso Nacional de Chile. (2025). Reporte Regional 2025: "
             "Región Metropolitana de Santiago (sección 4.4, Salud). "
             "https://www.bcn.cl/siit/reportesregionales/reporte_final.html?unidad=regional"
             "&anno=2025&cod_region=13")

doc.add_heading("Capítulo 4 — Estimación de Mercado", level=2)
ref_apa(doc, "The Insight Partners. (2025). Digital health market. "
             "https://www.theinsightpartners.com/pr/digital-health-market")
ref_apa(doc, "Business Research Insights. (s. f.). AI ECG analysis market report. "
             "https://www.businessresearchinsights.com/market-reports/ai-ecg-analysis-market-115488")
ref_apa(doc, "Ministerio de Salud de Chile. (2023). Estrategia Nacional de Salud al 2030. "
             "https://degreyd.minsal.cl/wp-content/uploads/2023/12/Estrategia-Nacional-de-"
             "Salud-al-2030.pdf")

doc.add_heading("Capítulo 5 — Situación de Mercado", level=2)
ref_apa(doc, "Philips Chile. (s. f.). PageWriter TC35 Cardiograph. "
             "https://www.philips.cl/healthcare/product/860437/pagewriter-tc35-cardiograph")
ref_apa(doc, "GE HealthCare. (s. f.). MAC 5 Resting ECG. https://www.gehealthcare.com.sg/"
             "en/products/diagnostic-ecg/resting-ecg/mac-5-resting-ecg")
ref_apa(doc, "Atrys Chile. (s. f.). Telecardiología. https://atrys.cl/telecardiologia/")
ref_apa(doc, "Cardiowapp. (s. f.). Plataforma. https://www.cardiowapp.cl/plataforma")

doc.add_heading("Capítulo 18 — Evaluación (CAPM)", level=2)
ref_apa(doc, "Damodaran, A. (2025). Betas by sector (US). NYU Stern School of Business. "
             "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html "
             "(tabla de enero de 2025; beta del sector de salud de EE. UU.)")

doc.add_heading("Capítulos 1, 2, 6, 8 y 20 — Dataset y método", level=2)
ref_apa(doc, "Tan, J., Fan, H., Luo, J., Zhou, Y., Wang, N., Wang, X., Liu, G., Liu, C., "
             "& Wang, Z. (2025). A pediatric ECG database with disease diagnosis covering "
             "11 643 children. Scientific Data, 12, 867. https://doi.org/10.1038/s41597-025-05225-z")
ref_apa(doc, "Tan, J. et al. (2025). Pediatric ECG database (ZZU) [Conjunto de datos]. "
             "Figshare. https://doi.org/10.6084/m9.figshare.27078763")

doc.add_heading("Mapa de uso de fuentes", level=2)
tabla(doc,
      ["Capítulo del informe", "Fuente", "Antecedente que respalda"],
      [
          ["3 — Modelo de Negocios", "BCN (2025), sección 4.4",
           "227 hospitales y 155 clínicas en Chile; 45 y 83 en la RM (universo institucional)"],
          ["4 — Estimación de Mercado", "The Insight Partners (2025)",
           "CAGR de salud digital 25,7% (2025–2031)"],
          ["4 — Estimación de Mercado", "Business Research Insights (s. f.)",
           "Mercado IA-ECG: USD 1.240M (2026) → 3.690M (2035), CAGR 13,7%"],
          ["4 — Estimación de Mercado", "MINSAL (2023)",
           "Modelo de salud digital sostenible de la Estrategia Nacional de Salud 2030"],
          ["5 — Situación de Mercado", "Philips (s. f.); GE HealthCare (s. f.)",
           "Algoritmos DXL (PageWriter TC35) y Marquette 12SL (MAC 5) con análisis pediátrico"],
          ["5 — Situación de Mercado", "Atrys (s. f.); Cardiowapp (s. f.)",
           "Telecardiología remota con especialistas; gestión y visualización de ECG"],
          ["6, 8, 20 — FODA, técnica, conclusión", "Tan et al. (2025)",
           "Entrenamiento y validación del clasificador sobre dataset pediátrico público ZZU"],
          ["18 — Evaluación", "Damodaran (2025)",
           "Beta sectorial para el cálculo CAPM de la tasa de descuento"],
      ])
doc.add_page_break()

# ============ ANEXO B: DATASET ZZU ============
doc.add_heading("Anexo B — Ficha técnica del dataset ZZU (Tan et al., 2025)", level=1)
para(doc, "Base de datos utilizada para el entrenamiento y la validación retrospectiva "
          "del pipeline DSP+ML de PedioLink (caps. 2, 6, 8 y 20 del informe).", 10.5)
tabla(doc,
      ["Atributo", "Detalle"],
      [
          ["Nombre", "Pediatric ECG database (ZZU)"],
          ["Publicación", "Tan, J. et al. (2025). Scientific Data, 12, 867 (revista de acceso abierto, Springer Nature)"],
          ["Institución de origen", "Primer Hospital Afiliado de la Universidad de Zhengzhou (China)"],
          ["Período de recolección", "2018–2024"],
          ["Tamaño", "11.643 niños; 14.190 registros ECG (12.334 de 12 derivaciones)"],
          ["Etiquetas", "Diagnóstico por enfermedad (arritmias y alteraciones del ritmo)"],
          ["Acceso", "Público y gratuito en Figshare: https://doi.org/10.6084/m9.figshare.27078763"],
          ["Rol en el proyecto", "Entrenamiento del modelo de deep learning y validación retrospectiva del pipeline (actividad 3 de la ruta crítica, meses 2–5)"],
          ["Decisión del grupo (02-nov)", "ZZU sustituye al dataset anterior (Leipzig) por ser 100% pediátrico, público y con diagnóstico por enfermedad; se retiran las menciones a Leipzig Heart Center / Leone et al."],
      ])
para(doc, "Limitación declarada en la conclusión del informe: al ser de origen chino, la "
          "generalización a la población pediátrica chilena requiere ampliar el conjunto "
          "de datos con convenios locales (Dr. Sótero del Río, Calvo Mackenna) y fuentes "
          "públicas complementarias (PTB-XL, MIT-BIH).", 10, italic=True)
doc.add_page_break()

# ============ ANEXO C: COMPETIDORES ============
doc.add_heading("Anexo C — Fichas de competidores y alternativas en el mercado", level=1)
para(doc, "Alternativas identificadas en el capítulo 5 del informe. La diferenciación de "
          "PedioLink se sustenta en la especialización pediátrica con deep learning, el "
          "aprovechamiento de equipos existentes y el acompañamiento de implementación.", 10.5)

def ficha(titulo, cuerpo):
    doc.add_heading(titulo, level=2)
    para(doc, cuerpo, 10.5)

ficha("Philips — PageWriter TC35 con algoritmo DXL",
      "Electrocardiógrafo de sobremesa con interpretación automatizada DXL, cuya "
      "documentación incluye análisis de poblaciones pediátricas e integración con "
      "sistemas de información clínica. Es un producto de hardware: exige renovación o "
      "adquisición de equipos. Implicancia para PedioLink: competidor directo en la "
      "interpretación automatizada; la diferencia es que PedioLink opera como capa de "
      "software sobre los equipos existentes, sin renovar hardware.")
ficha("GE HealthCare — MAC 5 Resting ECG con programa Marquette 12SL",
      "Electrocardiógrafo reposo con interpretaciones específicas para población "
      "pediátrica (programa Marquette 12SL). Misma lógica de competidor de hardware "
      "que Philips. Implicancia: la diferenciación de PedioLink no puede sustentarse "
      "solo en 'analizar ECG de niños'; debe demostrarse por desempeño por arritmia y "
      "edad, facilidad de uso, compatibilidad, soporte y costo-beneficio.")
ficha("Atrys Chile — Telecardiología",
      "Servicio remoto de informes de ECG de doce derivaciones para pacientes adultos y "
      "pediátricos, con participación de especialistas. No aplica deep learning como "
      "PedioLink: el informe lo elabora un cardiólogo. Implicancia: alternativa válida "
      "para instituciones sin especialista; PedioLink compite en tiempo de respuesta, "
      "costo por estudio y trazabilidad del análisis automatizado.")
ficha("Cardiowapp — Plataforma de gestión de ECG",
      "Plataforma para gestionar, almacenar, visualizar y facilitar la revisión remota "
      "de registros ECG. No interpreta la señal: es una capa de gestión. Implicancia: "
      "puede ser complementaria (integración) más que competidora; en la venta conviene "
      "diferenciar 'gestión de registros' de 'análisis de la señal con ML'.")

tabla(doc,
      ["Alternativa", "Tipo", "Análisis pediátrico", "Modelo", "Diferencia con PedioLink"],
      [
          ["Philips PageWriter TC35 (DXL)", "Equipo (hardware)", "Sí (DXL)",
           "Venta de equipo", "Exige renovar hardware; PedioLink usa equipos existentes"],
          ["GE MAC 5 (Marquette 12SL)", "Equipo (hardware)", "Sí (12SL)",
           "Venta de equipo", "Ídem; competir por desempeño/arritmia y costo total"],
          ["Atrys telecardiología", "Servicio remoto", "Sí (con especialista)",
           "Informe por especialista", "Sin ML; tiempo y costo por estudio; no automatiza"],
          ["Cardiowapp", "Software de gestión", "No interpreta",
           "Suscripción", "Gestión sin análisis; complementario/integrable"],
          ["PedioLink", "SaaS de análisis", "Sí (deep learning, dataset ZZU)",
           "Suscripción institucional", "Especializado en pediatría, sobre equipos existentes"],
      ])
doc.add_page_break()

# ============ ANEXO D: MARCO LEGAL ============
doc.add_heading("Anexo D — Marco legal y regulatorio aplicable", level=1)
para(doc, "Normativa considerada en el capítulo 13 del informe, con su implicancia "
          "operativa para PedioLink.", 10.5)
tabla(doc,
      ["Norma / organismo", "Materia", "Implicancia para PedioLink"],
      [
          ["Ley 20.190 (2007)", "Sociedad por Acciones (SPA)",
           "Figura societaria elegida: capital flexible, emisión de nuevas series sin modificar estatutos, responsabilidad limitada, administración simple"],
          ["Ley 19.628, modificada por Ley 21.719 (2024)", "Protección de la vida privada; datos sensibles",
           "Datos de salud: consentimiento explícito, cifrado, restricción de cesión; crea la Agencia de Protección de Datos con vigencia gradual, a monitorear"],
          ["Ley 20.584", "Derechos y deberes en salud",
           "Atención segura e información al paciente; el reporte PedioLink se inserta en la ficha clínica respetando estos deberes"],
          ["Ley 17.336", "Propiedad intelectual",
           "Derechos de autor sobre el código fuente propio"],
          ["INAPI", "Propiedad industrial",
           "Registro de la marca PedioLink (nombre e isotipo; nombre disponible según verificación del grupo)"],
          ["ISP — dispositivos médicos", "Regulación de software de salud",
           "El tratamiento aplicable al software de apoyo a la interpretación deberá verificarse con asesor regulatorio antes de la puesta en marcha (riesgo declarado en cap. 20)"],
          ["Normativa de telecomunicaciones", "Transmisión de datos clínicos",
           "Cifrado TLS 1.3 o superior en redes públicas"],
          ["Ley 19.300 / SEIA", "Medio ambiente",
           "Proyecto exento: no hay infraestructura física relevante ni residuos propios (cap. 16); operación cloud en AWS São Paulo"],
      ])
para(doc, "Riesgos de judicialización: (1) responsabilidad médica — mitigada con póliza "
          "de maledicencia y disclaimer explícito de rol de soporte en el dashboard; "
          "(2) protección de datos — sanciones conforme a la Ley 21.719 ante filtración "
          "de datos sensibles.", 10)
doc.add_page_break()

# ============ ANEXO E: LICITACIÓN ============
doc.add_heading("Anexo E — Referencia de mercado público: licitación 1057390-86-LP25", level=1)
para(doc, "Antecedente local de compra pública de servicios relacionados, citado en el "
          "capítulo 5 (canales de venta) del informe.", 10.5)
tabla(doc,
      ["Campo", "Detalle"],
      [
          ["Proceso", "Licitación pública 1057390-86-LP25"],
          ["Comprador", "Servicio de Salud Araucanía Norte"],
          ["Objeto", "Teleelectrocardiografía y teleradiografía"],
          ["Ponderaciones", "Criterio económico 60% · experiencia de la empresa 35% · programa de integridad 5%"],
          ["Implicancia comercial", "La entrada al mercado público exige antecedentes comerciales y operativos, además de la oferta tecnológica; sostiene la estrategia de pilotos y referencias previas a licitar"],
      ])
doc.add_page_break()

# ============ ANEXO F: SUPUESTOS Y TRAZABILIDAD ============
doc.add_heading("Anexo F — Supuestos del modelo económico y trazabilidad de palancas", level=1)
para(doc, "Hipótesis del caso viable materializado en la planilla "
          "PedioLink_Flujo_Caja.xlsx. Cada palanca es trazable al informe o a una "
          "decisión del grupo; los valores son editables en la hoja Supuestos y el "
          "modelo recalcula VAN, TIR y PRI automáticamente.", 10.5)
tabla(doc,
      ["Palanca", "Valor", "Trazabilidad / justificación"],
      [
          ["Horizonte de evaluación", "10 años",
           "La guía permite un horizonte distinto a cinco cuando se considere de interés; el SaaS aún está en ramp-up a los 5 años (VAN corte: −522 k)"],
          ["Precio de suscripción", "USD 2.450/mes",
           "Mix ponderado del rango declarado en el informe: 30% × 3.000 + 50% × 2.500 + 20% × 1.500"],
          ["Volumen por institución", "300 estudios/mes",
           "Supuesto declarado de hospital pediátrico referencial; valida el catastro institucional"],
          ["White-label / API", "10% de la suscripción desde año 3",
           "Línea de ingresos complementaria ya declarada en el cap. 6 del informe"],
          ["Expansión nacional", "Desde año 6; 37 instituciones al año 10 (~32% del universo calificado ≈115)",
           "Decisión del 29-oct: expansión según criterios de demanda y soporte, no meta arbitraria"],
          ["Costo cloud por estudio", "USD 0,80",
           "Extremo optimista del rango del informe (0,50–5), justificado por committed-use a volumen"],
          ["Dotación", "7 personas año 1 (socios a sueldo parcial); ~14 al año 10",
           "Guía cap. 12: 'tratar de minimizar sus costos fijos'; sustituye la estructura original de 11"],
          ["Año 1 parcial", "3,5 meses de operación por institución; 55% de los costos fijos",
           "Lanzamiento mes 8–9 según carta Gantt (cap. 9)"],
          ["Financiamiento", "USD 785 k: aportes 235 k + CORFO 150 k + Banca de Desarrollo 400 k (12%, 10 años, 3 de gracia)",
           "El crédito comercial al 12% de plazo corto destruía valor durante el ramp-up; la banca de desarrollo opera vía agentes CORFO en Chile"],
          ["Tasa de descuento", "Ke = 14,9%",
           "CAPM corregido con los insumos del informe (Anexo G)"],
      ])
para(doc, "Punto de equilibrio (año 5): 11,4 instituciones con la estructura ajustada; "
          "el caso viable alcanza 20 al cierre del año 5. La estructura original "
          "(11 personas) exigía 24,9 instituciones y motivó la reestructuración "
          "(diagnóstico descartado con VAN −2.968 k, hoja Escenarios del Excel).", 10)
doc.add_page_break()

# ============ ANEXO G: DETALLE FINANCIERO ============
doc.add_heading("Anexo G — Detalle financiero del caso viable", level=1)

doc.add_heading("G.1 — Flujo de caja proyectado (10 años, miles de USD)", level=2)
tabla(doc,
      ["Concepto", "Año 0", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5",
       "Año 6", "Año 7", "Año 8", "Año 9", "Año 10"],
      [
          ["Flujo neto", "−285", "−175,5", "−201,5", "−108,2", "+42,8", "+230,4",
           "+301,7", "+391,1", "+484,0", "+525,7", "+1.027,4"],
      ], size=8.5)
para(doc, "Ingresos, costos operacionales, EBITDA e impuestos por año se detallan en las "
          "hojas 'Flujo de Caja' y 'Estado Resultados' del Excel adjunto (fórmulas "
          "vivas; recálculo verificado con motor LibreOffice).", 9.5, italic=True)

doc.add_heading("G.2 — Cálculo CAPM de la tasa de descuento", level=2)
tabla(doc,
      ["Componente", "Valor", "Fuente / justificación"],
      [
          ["Rf — tasa libre de riesgo", "5,0%", "Bono soberano de Chile a 10 años"],
          ["Beta sectorial", "1,15", "Damodaran (2025), Betas by Sector (US), tabla de enero de 2025"],
          ["Rm − Rf — prima de mercado", "6,0%", "Prima de mercado US Equities, Damodaran"],
          ["PRP — prima por riesgo país", "3,0%", "Spread CDS Chile 2025"],
          ["Ke = Rf + β·(Rm−Rf) + PRP", "14,9%", "Tasa de descuento aplicada al flujo del proyecto"],
      ])

doc.add_heading("G.3 — Indicadores de evaluación", level=2)
tabla(doc,
      ["Indicador", "Valor", "Lectura"],
      [
          ["VAN normal (10 años, Ke 14,9%)", "+USD 323 k", "El proyecto crea valor para los inversionistas"],
          ["TIR", "21,9%", "+7,0 puntos porcentuales sobre Ke"],
          ["PRI simple / descontado", "6,5 / 8,6 años", "Recuperación dentro del horizonte"],
          ["VAN ajustado (esperado)", "+USD 204 k", "Ponderación probabilística 0,25 / 0,50 / 0,25 de escenarios"],
          ["VAN corte a 5 años", "−USD 522 k", "El SaaS aún está en ramp-up; sostiene la elección del horizonte de 10 años"],
          ["Punto de equilibrio operativo", "Año 4", "EBITDA positivo desde el año 4 (+113 k)"],
          ["Equilibrio de flujo acumulado", "Año 7", "El flujo acumulado se vuelve positivo"],
      ])

doc.add_heading("G.4 — Escenarios de sensibilización", level=2)
tabla(doc,
      ["Variable", "Pesimista", "Viable (normal)", "Optimista"],
      [
          ["Instituciones activas año 1", "1", "2", "3"],
          ["Instituciones activas año 5", "12", "20", "25"],
          ["Precio suscripción (USD/mes)", "1.500", "2.450", "3.000"],
          ["Churn anual", "20%", "10%", "5%"],
          ["Costo cloud (USD/estudio)", "1,50", "0,80", "0,80"],
          ["Inversión inicial (USD)", "320.000", "285.000", "260.000"],
          ["Ke (CAPM, común)", "14,9%", "14,9%", "14,9%"],
          ["VAN (miles USD)", "−1.685", "+323", "+1.853"],
          ["TIR", "n.r.", "21,9%", "49,4%"],
          ["Payback (años)", "No recupera", "6,5", "4,1"],
      ])
para(doc, "Variables críticas: velocidad de captura institucional y margen por "
          "institución (precio y volumen). El piso del pesimista (−1.685 k) exige "
          "planes de mitigación explícitos. Se recomienda complementar con simulación "
          "Monte Carlo (@Risk / Crystal Ball) en la fase de factibilidad, según la "
          "propia guía (cap. 19 del informe).", 10)
doc.add_page_break()

# ============ ANEXO H: INVERSIONES ============
doc.add_heading("Anexo H — Programa de inversiones", level=1)
para(doc, "Desglose de la inversión inicial (USD 285.000) y su programa de realización "
          "(cap. 10 del informe, tabla 3).", 10.5)
tabla(doc,
      ["Concepto", "USD", "Meses", "Comentario"],
      [
          ["Desarrollo de plataforma (4 devs × 6 meses)", "120.000", "M1–M6",
           "Rediseño cloud + multi-tenancy"],
          ["Validación clínica + asesoría legal", "35.000", "M3–M6",
           "Dataset ZZU, validación retrospectiva, revisión regulatoria"],
          ["Equipamiento cloud año 1", "15.000", "M1–M12", "Setup AWS + primeros meses de operación"],
          ["Contratación de equipo", "50.000", "M1–M6", "3 personas adicionales al equipo fundador"],
          ["Marketing y lanzamiento", "15.000", "M5–M8", "Ferias, webinars, materiales, demo hospitalaria"],
          ["Capital de trabajo", "50.000", "M1–M12", "Cubre 6 meses de operación inicial"],
          ["TOTAL INVERSIÓN INICIAL", "285.000", "M1–M8", "100% ejecutado al cierre del mes 8"],
      ])
para(doc, "Inversiones recurrentes (años 1–10): USD 70.000 anuales — mejoras de "
          "plataforma, expansión a nuevas regiones y funcionalidades avanzadas "
          "(multi-canal, API para terceros, wearables pediátricos). Se incluyen como "
          "egreso en el flujo de caja (cap. 17).", 10)
doc.add_page_break()

# ============ ANEXO I: FINANCIAMIENTO ============
doc.add_heading("Anexo I — Estructura de financiamiento y alternativas descartadas", level=1)
para(doc, "Estructura propuesta (cap. 11 del informe, tabla 4): total USD 785.000.", 10.5)
tabla(doc,
      ["Fuente", "Monto USD", "%", "Modalidad", "Condiciones"],
      [
          ["Aporte de socios", "235.000", "30%", "Capital propio",
           "Cubre inversión y ramp-up; sueldos parciales de socios"],
          ["CORFO Transforma Innovación Salud", "150.000", "19%", "Subsidio no reembolsable",
           "Convocatoria 2026; hitos verificables"],
          ["Banca de desarrollo (agente CORFO)", "400.000", "51%", "Crédito de largo plazo",
           "12% anual, 10 años, 3 de gracia de capital; amortización desde año 4"],
          ["TOTAL", "785.000", "100%", "—", "Inversión (285 k) + reserva de capital de trabajo (500 k)"],
      ])
doc.add_heading("Alternativas evaluadas y descartadas", level=2)
tabla(doc,
      ["Alternativa", "Razón de descarte"],
      [
          ["Leasing financiero", "No se adquieren activos fijos relevantes: los servidores son cloud"],
          ["Factoring", "El modelo no genera cuentas por cobrar significativas (suscripción prepaga)"],
          ["Venture Capital", "Dilución excesiva para los socios fundadores en esta etapa"],
          ["Crowdfunding", "Naturaleza B2B del producto"],
          ["Crédito bancario comercial de plazo corto", "El servicio de la deuda durante el ramp-up (EBITDA negativo años 1–3) destruía valor; confirmado por la evaluación (cap. 18)"],
      ])
doc.add_page_break()

# ============ ANEXO J: COSTOS FIJOS ============
doc.add_heading("Anexo J — Estructura de costos fijos del año 1", level=1)
para(doc, "Desglose mensual (cap. 12 del informe, tabla 5). El año 1 opera parcial "
          "(55% de los costos fijos) según la carta Gantt.", 10.5)
tabla(doc,
      ["Categoría", "USD/mes", "%", "Comentario"],
      [
          ["Remuneraciones (7 personas)", "12.500", "57,9%",
           "CEO, CTO, 2 devs ML, 1 ing. cloud, Director Médico (media jornada), Dir. Comercial, Admin./Finanzas"],
          ["Cloud base (infraestructura)", "2.500", "11,6%", "Committed-use a volumen: USD 0,80 por estudio"],
          ["Coworking (años 1–2)", "900", "4,2%", "Zona oriente de Santiago; oficina 100 m² desde año 3"],
          ["Marketing médico", "3.000", "13,9%", "Convenios, ferias, webinars"],
          ["Servicios (legal, auditoría)", "1.000", "4,6%", "Asesoría regulatoria continua"],
          ["Software y licencias de desarrollo", "800", "3,7%", "Repositorios, CI/CD, monitoreo"],
          ["Otros (seguros, servicios)", "900", "4,2%", "Póliza de responsabilidad, internet"],
          ["TOTAL COSTOS FIJOS", "21.600", "100%", "≈ USD 259.200 anuales a régimen"],
      ])
para(doc, "Costos variables: USD 0,80 por estudio procesado (300 estudios/mes por "
          "institución ≈ USD 240 mensuales por cliente). Estrategia de minimización: "
          "AWS Lambda (pago por ejecución), outsourcing de contabilidad, pediatra "
          "asesor media jornada y stack 100% de software libre.", 10)
doc.add_page_break()

# ============ ANEXO K: GANTT-PERT ============
doc.add_heading("Anexo K — Precedencias y holguras (Carta Gantt / PERT)", level=1)
para(doc, "Descomposición de la puesta en marcha (8 meses, cap. 9 del informe, tabla 2). "
          "La ruta crítica encadena constitución, desarrollo cloud, validación con "
          "dataset ZZU y piloto: cualquier demora retrasa el lanzamiento.", 10.5)
tabla(doc,
      ["Actividad", "Meses", "Predecesora", "Holgura", "Crítica"],
      [
          ["1. Constitución SPA + levantamiento de capital", "M1–M2", "—", "0", "Sí"],
          ["2. Desarrollo cloud multi-tenant (AWS)", "M2–M6", "1", "0", "Sí"],
          ["3. Dataset ZZU + validación retrospectiva", "M2–M5", "2 (parcial)", "0", "Sí"],
          ["4. Convenios piloto (hospital/clínica RM)", "M3–M6", "1", "2 semanas", "No"],
          ["5. Piloto con 50 pacientes", "M6–M7", "3, 4", "0", "Sí"],
          ["6. Lanzamiento comercial", "M8", "5", "0", "Sí"],
      ])
para(doc, "Ruta crítica: 1 → 2 → 3 → 5 → 6. Actividades con holgura: convenios piloto "
          "(2 semanas) y preparación comercial (M5–M8, 3 semanas). El calendario "
          "sostiene las estimaciones de inversión del Anexo H.", 10)
doc.add_page_break()

# ============ ANEXO L: REFERENCIAS DE PRECIOS ============
doc.add_heading("Anexo L — Referencias de precios (hipótesis declaradas del modelo)", level=1)
para(doc, "Valores referenciales utilizados en la evaluación, tal como se declaran en el "
          "informe. Son hipótesis de planificación, no cotizaciones formales: los rubros "
          "marcados 'a validar' se formalizarán con cotizaciones reales antes de las "
          "decisiones respectivas (traslado de oficina, contratos cloud).", 10.5)
tabla(doc,
      ["Rubro", "Valor referencial", "Estado / fuente"],
      [
          ["Suscripción institucional", "USD 1.500–3.000/mes (cupo base 200 estudios)",
           "Hipótesis comercial del informe; mix ponderado 30/50/20 → USD 2.450"],
          ["Estudio adicional sobre cupo", "USD 8 por estudio", "Hipótesis comercial del informe (cap. 3)"],
          ["Cargo inicial de implementación", "USD 8.000 por institución",
           "Configuración, capacitación e integración (cap. 3)"],
          ["Coworking zona oriente (años 1–2)", "≈ USD 900/mes", "Referencial; representa ~4,2% de los costos fijos"],
          ["Oficina 100 m² en Providencia (desde año 3)", "≈ USD 2.500/mes", "Referencial, a validar con cotizaciones del mercado antes del traslado"],
          ["Cloud AWS", "USD 2.500/mes base + USD 0,80 por estudio", "Committed-use a volumen; región São Paulo"],
          ["Remuneraciones equipo año 1", "USD 12.500/mes (7 personas, socios a sueldo parcial)", "Hipótesis del modelo (hoja Supuestos del Excel)"],
          ["Póliza de responsabilidad/maledicencia", "Incluida en 'Otros' (USD 900/mes)", "Referencial"],
      ])
doc.add_page_break()

# ============ ANEXO M: GLOSARIO ============
doc.add_heading("Anexo M — Glosario de términos y siglas", level=1)
tabla(doc,
      ["Término", "Definición"],
      [
          ["BPMN", "Business Process Model and Notation: notación estándar de modelamiento de procesos de negocio"],
          ["CANVAS", "Modelo de negocios de nueve bloques (Osterwalder) usado en el cap. 3"],
          ["CAPM", "Capital Asset Pricing Model: Ke = Rf + β·(Rm−Rf) + PRP"],
          ["Churn", "Tasa anual de cancelación de suscripciones"],
          ["Deep Learning", "Aprendizaje profundo: clasificación supervisada mediante redes neuronales multicapa"],
          ["DICOM-ECG / WFDB", "Formatos estandarizados de almacenamiento/exportación de registros ECG"],
          ["DSP", "Procesamiento digital de señales: filtrado, detección de picos R (Pan-Tompkins), extracción de características"],
          ["EBITDA", "Utilidad antes de intereses, impuestos, depreciación y amortización"],
          ["FHIR R4 / HL7 v2", "Estándares de interoperabilidad clínica para integración con HIS/HLE"],
          ["HIS/HLE", "Sistemas de información hospitalaria / de laboratorio y examen"],
          ["INAPI / ISP", "Instituto Nacional de Propiedad Industrial / Instituto de Salud Pública"],
          ["Ke", "Tasa de descuento del capital propio (costo de equity)"],
          ["PRI", "Período de recuperación de la inversión (simple y descontado)"],
          ["SaaS", "Software como Servicio: licencia por suscripción, sin instalación local"],
          ["TAM / SAM / SOM", "Mercado potencial total / atendible / objetivo a captar (metodología del cap. 4)"],
          ["SEIA", "Sistema de Evaluación de Impacto Ambiental (Ley 19.300); PedioLink está exento"],
          ["SPA", "Sociedad por Acciones (Ley 20.190)"],
          ["TIR / VAN", "Tasa Interna de Retorno / Valor Actual Neto"],
          ["ZZU", "Dataset pediátrico público (Tan et al., 2025; Anexo B)"],
      ])

doc.save("PedioLink_Anexos.docx")
print("OK PedioLink_Anexos.docx")
