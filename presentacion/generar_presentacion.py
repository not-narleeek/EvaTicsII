#!/usr/bin/env python3
"""Genera presentacion/PedioLink_Presentacion.pptx — entregable CANVAS 3.

Estructura de defensa (25 min) con elevator pitch de 60 s al inicio,
según la guía del curso. Cada lámina lleva notas del expositor con las
cifras de respaldo. Fuentes de verdad: informe FINAL, docs/excel-notas.md,
gráficos en informe/graficos/.

Uso: python3 presentacion/generar_presentacion.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

PRIMARY = RGBColor(0x0F, 0x4C, 0x81)   # azul institucional
ACCENT = RGBColor(0x14, 0xB8, 0xA6)    # teal salud digital
DARK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x6B, 0x72, 0x80)
LIGHT = RGBColor(0xF3, 0xF4, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB9, 0x1C, 0x1C)

GRUPO = "Gustavo Castro · Carlos Jara · Fernando Llancao · Donovan Iturra"
CURSO = "Evaluación de Proyectos TIC — Sección 2 · Prof. Jorge Elliott · UDP"
G = "informe/graficos/"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def base(titulo=None, kicker=None):
    """Lámina en blanco con banda superior + título + pie."""
    s = prs.slides.add_slide(BLANK)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.14))
    band.fill.solid(); band.fill.fore_color.rgb = PRIMARY
    band.line.fill.background(); band.shadow.inherit = False
    if titulo:
        tb = s.shapes.add_textbox(Inches(0.55), Inches(0.32), Inches(12.3), Inches(0.75))
        p = tb.text_frame.paragraphs[0]
        r = p.add_run(); r.text = titulo
        r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = PRIMARY
        r.font.name = "Calibri"
    if kicker:
        kb = s.shapes.add_textbox(Inches(0.57), Inches(0.98), Inches(12.2), Inches(0.4))
        p = kb.text_frame.paragraphs[0]
        r = p.add_run(); r.text = kicker
        r.font.size = Pt(13); r.font.color.rgb = MUTED; r.font.name = "Calibri"
    return s


def pie(s, n, total=18):
    fb = s.shapes.add_textbox(Inches(0.55), Inches(7.08), Inches(12.3), Inches(0.35))
    p = fb.text_frame.paragraphs[0]
    r = p.add_run(); r.text = f"PedioLink — Evaluación de Proyectos TIC 2S-2026   ·   {n}/{total}"
    r.font.size = Pt(9); r.font.color.rgb = MUTED; r.font.name = "Calibri"


def bullets(s, items, left, top, width, height, size=15, spacing=6):
    """items: str o (str, nivel). 'Título: resto' deja el prefijo en negrita."""
    tb = s.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        txt, lvl = (it, 0) if isinstance(it, str) else it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(spacing)
        if lvl == 0 and ":" in txt and txt.index(":") < 48:
            head, rest = txt.split(":", 1)
            r = p.add_run(); r.text = head + ":"
            r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = DARK
            r.font.name = "Calibri"
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.color.rgb = DARK; r2.font.name = "Calibri"
        else:
            r = p.add_run(); r.text = ("•  " if lvl == 0 else "–  ") + txt if lvl >= 0 else txt
            r.font.size = Pt(size if lvl == 0 else size - 1)
            r.font.color.rgb = DARK if lvl == 0 else MUTED
            r.font.name = "Calibri"
        p.level = max(lvl, 0)
    return tb


def img_fit(s, path, left, top, width, height):
    iw, ih = Image.open(path).size
    sc = min(width / iw, height / ih)
    w, h = int(iw * sc), int(ih * sc)
    return s.shapes.add_picture(path, left + int((width - w) / 2),
                                top + int((height - h) / 2), w, h)


def tabla(s, data, left, top, width, height, font=11, col_w=None):
    rows, cols = len(data), len(data[0])
    gfx = s.shapes.add_table(rows, cols, left, top, width, height).table
    if col_w:
        for j, w in enumerate(col_w):
            gfx.columns[j].width = w
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            c = gfx.cell(i, j)
            c.text = str(val)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.margin_left = Inches(0.06); c.margin_right = Inches(0.06)
            c.margin_top = Inches(0.02); c.margin_bottom = Inches(0.02)
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(font); p.font.name = "Calibri"
            if i == 0:
                p.font.bold = True; p.font.color.rgb = WHITE
                c.fill.solid(); c.fill.fore_color.rgb = PRIMARY
            else:
                p.font.color.rgb = DARK
                c.fill.solid()
                c.fill.fore_color.rgb = WHITE if i % 2 else LIGHT
    return gfx


def kpi(s, left, top, w, h, valor, etiqueta, sub=None, color=PRIMARY):
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    box.adjustments[0] = 0.08
    box.fill.solid(); box.fill.fore_color.rgb = color
    box.line.fill.background(); box.shadow.inherit = False
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_top = Inches(0.06); tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = valor
    r.font.size = Pt(26); r.font.bold = True; r.font.color.rgb = WHITE
    r.font.name = "Calibri"
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = etiqueta
    r2.font.size = Pt(11); r2.font.color.rgb = WHITE; r2.font.name = "Calibri"
    if sub:
        p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
        r3 = p3.add_run(); r3.text = sub
        r3.font.size = Pt(9); r3.font.color.rgb = RGBColor(0xD7, 0xE3, 0xEE)
        r3.font.name = "Calibri"


def notas(s, texto):
    s.notes_slide.notes_text_frame.text = texto


# ============================================================ 1. PORTADA
s = prs.slides.add_slide(BLANK)
side = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(4.6), SH)
side.fill.solid(); side.fill.fore_color.rgb = PRIMARY
side.line.fill.background(); side.shadow.inherit = False
strip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.6), 0, Inches(0.09), SH)
strip.fill.solid(); strip.fill.fore_color.rgb = ACCENT
strip.line.fill.background(); strip.shadow.inherit = False
tb = s.shapes.add_textbox(Inches(0.55), Inches(2.2), Inches(3.8), Inches(2.8))
tf = tb.text_frame; tf.word_wrap = True
for txt, sz, bold, col in [("PedioLink", 44, True, WHITE),
                           ("Soporte diagnóstico de arritmias pediátricas vía ECG y machine learning", 16, False, RGBColor(0xD7, 0xE3, 0xEE))]:
    p = tf.paragraphs[0] if txt == "PedioLink" else tf.add_paragraph()
    r = p.add_run(); r.text = txt
    r.font.size = Pt(sz); r.font.bold = bold; r.font.color.rgb = col
    r.font.name = "Calibri"
img_fit(s, G + "fig_logo.png", Inches(5.1), Inches(1.6), Inches(7.6), Inches(3.4))
tb = s.shapes.add_textbox(Inches(5.2), Inches(5.3), Inches(7.5), Inches(1.6))
tf = tb.text_frame; tf.word_wrap = True
for txt, sz, col in [("Evaluación económica de un proyecto SaaS institucional B2B", 14, DARK),
                     (CURSO, 12, MUTED), ("Grupo: " + GRUPO, 12, MUTED),
                     ("Entrega CANVAS · 9 de noviembre de 2026", 12, MUTED)]:
    p = tf.paragraphs[0] if col == DARK else tf.add_paragraph()
    p.space_after = Pt(4)
    r = p.add_run(); r.text = txt
    r.font.size = Pt(sz); r.font.color.rgb = col; r.font.name = "Calibri"
notas(s, "Presentación de 25 min + 60 s de elevator pitch. Cada integrante defiende "
         "individualmente: todos deben dominar las cifras (VAN, TIR, Ke, captura).")

# ============================================================ 2. ELEVATOR PITCH
s = base("Elevator pitch (60 segundos)", "Como ante CORFO, SERCOTEC, financistas o un directorio")
box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(1.6),
                         Inches(11.9), Inches(4.6))
box.adjustments[0] = 0.05
box.fill.solid(); box.fill.fore_color.rgb = LIGHT
box.line.color.rgb = PRIMARY; box.line.width = Pt(1.2); box.shadow.inherit = False
tf = box.text_frame; tf.word_wrap = True
tf.margin_left = Inches(0.45); tf.margin_right = Inches(0.45)
tf.margin_top = Inches(0.35); tf.margin_bottom = Inches(0.3)
pitch = ("La interpretación de un ECG pediátrico exige criterios que cambian con la edad, y hoy los médicos la hacen "
         "apoyados en algoritmos diseñados para adultos o esperando informes de especialistas. "
         "PedioLink es una plataforma SaaS que analiza el ECG de niños mediante procesamiento digital de señales y "
         "deep learning —entrenado con un dataset público de 11.643 pacientes pediátricos— y entrega al clínico un "
         "reporte que destaca los hallazgos a revisar, sin reemplazar su criterio. "
         "Vendemos suscripciones a hospitales y clínicas: hay 382 establecimientos de referencia en Chile y un mercado "
         "calificado de unas 38 instituciones solo en la Región Metropolitana, con precios entre USD 1.500 y 3.000 mensuales. "
         "El proyecto requiere USD 785 mil de financiamiento y evalúa VAN positivo de USD 323 mil, TIR de 21,9% sobre una "
         "tasa exigida de 14,9%, con equilibrio operativo en el año 4. "
         "PedioLink: la señal cardíaca del niño, leída con estándares pediátricos.")
p = tf.paragraphs[0]
for seg, bold in [(pitch.split("PedioLink: la señal")[0], False),
                  ("PedioLink: la señal cardíaca del niño, leída con estándares pediátricos.", True)]:
    r = p.add_run(); r.text = seg
    r.font.size = Pt(16.5); r.font.bold = bold; r.font.color.rgb = DARK
    r.font.name = "Calibri"; r.font.italic = not bold
p.alignment = PP_ALIGN.LEFT; p.line_spacing = 1.15
bullets(s, ["Cifras clave: 382 establecimientos · SAM calificado ≈38 · USD 785 k · VAN +323 k · TIR 21,9% · equilibrio año 4"],
        Inches(0.7), Inches(6.35), Inches(11.9), Inches(0.5), size=12)
pie(s, 2)
notas(s, "Cronometrar 60 s exactos. Estructura: problema → solución → mercado → cifras → cierre. "
         "Cifras: dataset ZZU 11.643 niños (Tan et al. 2025); VAN +323 k a 10 años; Ke 14,9% CAPM.")

# ============================================================ 3. PROBLEMA Y OPORTUNIDAD
s = base("Problema y oportunidad", "Capítulos 1, 2 y 4 del informe")
bullets(s, [
    "Problema clínico: el ECG pediátrico exige parámetros normales que varían con la edad; la revisión es más exigente que en adultos",
    "Alternativas actuales: equipos con interpretación adulto-céntrica (DXL, Marquette 12SL) o informes remotos con especialistas",
    "Salud digital global: CAGR 25,7% (2025–2031)",
    "IA aplicada a ECG: USD 1.240M (2026) → USD 3.690M (2035), CAGR 13,7%",
    "Marco favorable: Estrategia Nacional de Salud 2030 promueve un modelo de salud digital sostenible",
], Inches(0.7), Inches(1.75), Inches(7.3), Inches(4.6), size=15.5)
kpi(s, Inches(8.5), Inches(1.9), Inches(4.1), Inches(1.5), "25,7%", "CAGR salud digital 2025–2031", "The Insight Partners (2025)")
kpi(s, Inches(8.5), Inches(3.55), Inches(4.1), Inches(1.5), "13,7%", "CAGR IA-ECG hasta 2035", "USD 1.240M → 3.690M · BRI", color=ACCENT)
kpi(s, Inches(8.5), Inches(5.2), Inches(4.1), Inches(1.5), "382", "Hospitales + clínicas en Chile", "BCN Reporte Regional 2025 (45H+83C en RM)")
pie(s, 3)
notas(s, "El problema no es 'diagnosticar arritmias' en general: es la brecha de apoyo específico pediátrico. "
         "Cifras de mercado citadas como referencia sectorial, no como proyección del segmento chileno (transparencia metodológica).")

# ============================================================ 4. LA SOLUCIÓN
s = base("La solución: PedioLink", "Capítulo 2 del informe — SaaS institucional, decisión clínica final del médico")
bullets(s, [
    "Módulo 1 — Recepción: valida archivos ECG digitales exportados por los equipos existentes (WFDB / DICOM-ECG)",
    "Módulo 2 — Análisis: pipeline DSP + deep learning entrenado con el dataset pediátrico público ZZU (11.643 niños)",
    "Módulo 3 — Interfaz web: dashboard React; el médico revisa registro y resultados con segmentos marcados",
    "Propuesta de valor: herramienta especializada en pediatría, integrada al flujo de revisión, sin renovar hardware",
    "Rol de soporte: no sustituye el criterio clínico; probabilidades con nivel de certeza explícito",
    "Incluye capacitación digital (manual, videos, registros de práctica); usa los equipos que ya tiene la institución",
], Inches(0.7), Inches(1.8), Inches(7.6), Inches(4.8), size=15)
img_fit(s, G + "fig_bpmn.png", Inches(8.5), Inches(2.2), Inches(4.4), Inches(3.9))
bullets(s, ["Proceso de negocio (BPMN, cap. 7)"], Inches(8.5), Inches(6.2), Inches(4.4), Inches(0.4), size=10)
pie(s, 4)
notas(s, "Tres componentes, en ese orden, forman el flujo BPMN. Subrayar: la decisión clínica final "
         "siempre es del profesional — clave para el marco regulatorio y la responsabilidad (cap. 13).")

# ============================================================ 5. CANVAS
s = base("Modelo de negocios — CANVAS", "Capítulo 3 del informe (guía: punto 3)")
img_fit(s, G + "fig1_canvas.png", Inches(0.55), Inches(1.55), Inches(12.2), Inches(5.3))
pie(s, 5)
notas(s, "Lógica comercial: suscripción recurrente institucional + implementación (USD 8.000) + uso adicional "
         "(USD 8/estudio sobre cupo 200). Socios clave: AWS, sociedades médicas, asesor regulatorio. "
         "Costos fijos año 1: USD 21,6 k/mes; variables: USD 0,80/estudio.")

# ============================================================ 6. MERCADO
s = base("Estimación de mercado — TAM · SAM · SOM", "Capítulo 4 del informe (metodología TAM-SAM-SOM)")
img_fit(s, G + "fig_tam_sam_som.png", Inches(0.55), Inches(1.6), Inches(12.2), Inches(3.6))
kpi(s, Inches(0.7), Inches(5.45), Inches(3.7), Inches(1.3), "382", "TAM: hospitales + clínicas (BCN 2025)", sub=None)
kpi(s, Inches(4.8), Inches(5.45), Inches(3.7), Inches(1.3), "128 → ≈38", "SAM: RM → calificado (catastro pendiente)", color=ACCENT)
kpi(s, Inches(8.9), Inches(5.45), Inches(3.7), Inches(1.3), "2 → 20", "SOM: instituciones año 1 → año 5", sub="Expansión nacional desde año 6 (37 al año 10)")
pie(s, 6)
notas(s, "Precio de referencia: USD 2.450/mes (mix 30/50/20 sobre el rango 1.500–3.000) → USD 29,4 k/año por institución. "
         "El SAM calificado (~38) es estimación pendiente de catastro: honestidad metodológica que hay que defender.")

# ============================================================ 7. COMPETENCIA
s = base("Situación de mercado — competencia y diferenciación", "Capítulo 5 del informe")
tabla(s, [
    ["Alternativa", "Tipo", "Análisis pediátrico", "Modelo", "Frente a PedioLink"],
    ["Philips PageWriter TC35 (DXL)", "Equipo", "Sí (DXL)", "Venta de equipo", "Exige renovar hardware"],
    ["GE MAC 5 (Marquette 12SL)", "Equipo", "Sí (12SL)", "Venta de equipo", "Competir por desempeño/costo total"],
    ["Atrys telecardiología", "Servicio remoto", "Sí (especialista)", "Informe por estudio", "Sin ML; costo y tiempo por informe"],
    ["Cardiowapp", "Software de gestión", "No interpreta", "Suscripción", "Complementario (gestión, no análisis)"],
    ["PedioLink", "SaaS de análisis", "Sí (deep learning, ZZU)", "Suscripción institucional", "Especialización + equipos existentes"],
], Inches(0.7), Inches(1.75), Inches(11.9), Inches(3.2), font=12.5,
    col_w=[Inches(3.1), Inches(1.6), Inches(2.4), Inches(2.3), Inches(2.5)])
bullets(s, [
    "Diferenciación: no basta 'analizar ECG de niños' — hay que demostrar desempeño por arritmia y edad, facilidad de uso y costo total",
    "Ciclo de vida: etapa de desarrollo/validación, previa a la introducción comercial",
    "Referencia de compra pública: licitación 1057390-86-LP25 (SS Araucanía Norte) pondera 60% económico + 35% experiencia",
], Inches(0.7), Inches(5.35), Inches(11.9), Inches(1.5), size=13.5)
pie(s, 7)
notas(s, "La tabla resume las fichas del Anexo C. Pregunta esperable: '¿por qué un hospital cambiaría?' — "
         "Respuesta: no renueva hardware, mantiene su flujo y gana una capa pediátrica especializada con soporte local.")

# ============================================================ 8. ESTRATEGIA COMERCIAL
s = base("Plan y estrategia comercial", "Capítulo 6 del informe — FODA, PEST y palancas")
tabla(s, [
    ["Fortalezas", "Debilidades", "Oportunidades", "Amenazas"],
    ["Equipo combinado salud-TIC; dataset pediátrico público ZZU; SaaS con referencias; stack libre",
     "Sin canal comercial; marca nueva; sin validación prospectiva",
     "Salud digital MINSAL; CORFO Transforma Salud; IA-ECG +13,7% anual",
     "Regulación sanitaria en evolución; reacción de Philips/GE; adopción pública lenta"],
], Inches(0.7), Inches(1.7), Inches(11.9), Inches(2.1), font=11.5,
    col_w=[Inches(3.1), Inches(2.9), Inches(2.9), Inches(3.0)])
bullets(s, [
    "Penetración: pilotos RM año 1 con demo gratuita de 3 meses",
    "Posicionamiento: 'alternativa exclusivamente pediátrica' en SOCHICARDIO / SOCHIPE + paper con el asesor clínico",
    "Línea complementaria: white-label y API desde año 3 (~10% de la suscripción)",
    "Expansión territorial: desde año 6, según criterios de demanda y soporte (37 instituciones al año 10)",
], Inches(0.7), Inches(4.15), Inches(11.9), Inches(2.4), size=14)
pie(s, 8)
notas(s, "Consistencia exigida por la guía: la estrategia deriva del FODA y de los caps. 3-5. "
         "El white-label/API ya estaba declarado en el cap. 6 y el modelo lo valoriza desde el año 3.")

# ============================================================ 9. OPERACIÓN Y TECNOLOGÍA
s = base("Plan operacional y solución técnica", "Capítulos 7 y 8 del informe")
img_fit(s, G + "fig_bpmn.png", Inches(0.55), Inches(1.6), Inches(12.2), Inches(3.1))
bullets(s, [
    "Cloud: AWS región São Paulo — Lambda (serverless), RDS PostgreSQL, S3, API Gateway",
    "Pipeline: filtros FIR/notch 50 Hz → Pan-Tompkins adaptado a pediatría (precisión ≥95%) → deep learning (dataset ZZU)",
    "Interoperabilidad: HL7 v2 / FHIR R4 con HIS/HLE; TLS 1.3 en tránsito, AES-256 en reposo",
    "Stack 100% open source (Python, React): costo cero de licencias y auditoría reproducible",
], Inches(0.7), Inches(4.95), Inches(11.9), Inches(1.9), size=13.5)
pie(s, 9)
notas(s, "Criterios de selección del stack (guía, punto 8): costo cero, escalabilidad serverless, "
         "cumplimiento normativo y replicabilidad. Cloud: USD 2,5 k/mes base + USD 0,80/estudio committed-use.")

# ============================================================ 10. GANTT-PERT
s = base("Puesta en marcha — Carta Gantt / PERT", "Capítulo 9 del informe — ruta crítica M1–M8")
img_fit(s, G + "fig2_gantt.png", Inches(0.55), Inches(1.6), Inches(12.2), Inches(3.7))
bullets(s, [
    "Ruta crítica: constitución SPA + capital → desarrollo cloud → dataset ZZU + validación → piloto 50 pacientes → lanzamiento (M8)",
    "Holguras: convenios piloto (2 semanas, M3–M6) y preparación comercial (3 semanas, M5–M8)",
    "Cualquier demora en la ruta crítica retrasa el lanzamiento — base de las inversiones del cap. 10",
], Inches(0.7), Inches(5.5), Inches(11.9), Inches(1.4), size=13.5)
pie(s, 10)
notas(s, "El piloto (50 pacientes, hospital RM) cierra la validación clínica antes del lanzamiento. "
         "La carta Gantt justifica la operación parcial del año 1 (3,5 meses por institución, 55% de costos fijos).")

# ============================================================ 11. INVERSIÓN Y FINANCIAMIENTO
s = base("Inversiones y financiamiento", "Capítulos 10 y 11 del informe — USD 285 k de inversión · USD 785 k de estructura")
tabla(s, [
    ["Inversión inicial (USD 285 k)", "USD", "M"],
    ["Desarrollo plataforma (4 devs × 6 m)", "120.000", "M1–M6"],
    ["Validación clínica + legal (ZZU)", "35.000", "M3–M6"],
    ["Cloud año 1", "15.000", "M1–M12"],
    ["Equipo (3 contrataciones)", "50.000", "M1–M6"],
    ["Marketing y lanzamiento", "15.000", "M5–M8"],
    ["Capital de trabajo", "50.000", "M1–M12"],
], Inches(0.7), Inches(1.8), Inches(5.8), Inches(3.3), font=12.5,
    col_w=[Inches(3.4), Inches(1.3), Inches(1.1)])
tabla(s, [
    ["Financiamiento (USD 785 k)", "USD", "%", "Condiciones"],
    ["Aporte de socios", "235.000", "30%", "Capital propio"],
    ["CORFO Transforma Salud", "150.000", "19%", "Subsidio no reembolsable"],
    ["Banca de desarrollo (CORFO)", "400.000", "51%", "12%, 10 años, 3 de gracia"],
    ["Reserva de capital de trabajo", "500.000", "—", "Cubre ramp-up años 1–3"],
], Inches(6.9), Inches(1.8), Inches(5.75), Inches(2.7), font=12.5,
    col_w=[Inches(2.5), Inches(1.15), Inches(0.7), Inches(1.4)])
bullets(s, [
    "Descartadas (justificadas en el modelo): leasing (no hay activos fijos), factoring (suscripción prepaga), VC (dilución), crowdfunding (B2B)",
    "Crédito comercial de plazo corto: destruía valor durante el ramp-up (EBITDA negativo años 1–3) — por eso banca de desarrollo",
], Inches(0.7), Inches(5.35), Inches(11.9), Inches(1.3), size=13)
pie(s, 11)
notas(s, "785 k = 285 k inversión + 500 k reserva de liquidez. La banca de desarrollo opera vía agentes CORFO "
         "en Chile: plazo largo con 3 años de gracia de capital; amortización desde año 4 (EBITDA +113 k).")

# ============================================================ 12. ORGANIZACIÓN Y COSTOS
s = base("Organización y estructura de costos", "Capítulos 12 y 14 del informe — minimizar costos fijos (guía, punto 12)")
img_fit(s, G + "fig3_organigrama.png", Inches(0.55), Inches(1.7), Inches(7.3), Inches(4.6))
bullets(s, [
    "Año 1: 7 personas (4 socios a sueldo parcial) → ~14 al año 10",
    "Costos fijos: USD 21.600/mes (remuneraciones 57,9%)",
    "Costo variable: USD 0,80 por estudio (300 estudios/mes por institución)",
    "Minimización: Lambda pago-por-ejecución, outsourcing contable, pediatra asesor media jornada, software libre",
    "Coworking años 1–2 (USD 900/mes); oficina 100 m² Providencia desde año 3 (USD 2.500/mes, a validar con cotizaciones)",
], Inches(8.2), Inches(1.9), Inches(4.5), Inches(4.6), size=13.5)
pie(s, 12)
notas(s, "Punto de equilibrio año 5: 11,4 instituciones (estructura ajustada); el caso viable llega a 20. "
         "La estructura original de 11 personas exigía 24,9 y arrojaba VAN −2.968 k: esa comparación defendió la reestructuración.")

# ============================================================ 13. FLUJO DE CAJA
s = base("Flujo de caja proyectado — 10 años", "Capítulo 17 del informe · Excel adjunto (hojas Flujo de Caja, EERR, Balance)")
img_fit(s, G + "fig4_flujo.png", Inches(0.55), Inches(1.6), Inches(12.2), Inches(4.3))
bullets(s, [
    "Ramp-up: EBITDA negativo años 1–3 (−105,5 / −131,5 / −38,2 k) — coherente con la Gantt y la reserva de liquidez",
    "Punto de equilibrio operativo año 4 (EBITDA +113 k) · flujo acumulado positivo año 7",
    "EERR y Balance primeros 3 años consistentes con el flujo (patrimonio negativo 1–3 por amortización no-caja, revierte año 5–6)",
], Inches(0.7), Inches(6.0), Inches(11.9), Inches(1.1), size=13)
pie(s, 13)
notas(s, "Flujo neto por año (k USD): −285 · −175,5 · −201,5 · −108,2 · +42,8 · +230,4 · +301,7 · +391,1 · +484,0 · +525,7 · +1.027,4. "
         "Año 1 parcial: ingresos 38,8 k con 3,5 meses de operación por institución.")

# ============================================================ 14. EVALUACIÓN ECONÓMICA
s = base("Evaluación económica — VAN · TIR · PRI · CAPM", "Capítulo 18 del informe · Excel (hoja Evaluacion)")
kpi(s, Inches(0.7), Inches(1.8), Inches(3.7), Inches(1.6), "+USD 323 k", "VAN normal (10 años)", "Ke 14,9% (CAPM)")
kpi(s, Inches(4.8), Inches(1.8), Inches(3.7), Inches(1.6), "21,9%", "TIR", "+7,0 pp sobre Ke", color=ACCENT)
kpi(s, Inches(8.9), Inches(1.8), Inches(3.7), Inches(1.6), "6,5 / 8,6", "PRI simple / descontado (años)")
kpi(s, Inches(0.7), Inches(3.6), Inches(3.7), Inches(1.6), "+USD 204 k", "VAN ajustado (esperado)", "Escenarios 0,25/0,50/0,25")
kpi(s, Inches(4.8), Inches(3.6), Inches(3.7), Inches(1.6), "−USD 522 k", "VAN corte a 5 años", "Ramp-up → horizonte 10 años (guía)", color=MUTED)
kpi(s, Inches(8.9), Inches(3.6), Inches(3.7), Inches(1.6), "14,9%", "Ke = CAPM", "5,0 + 1,15×6,0 + 3,0", color=ACCENT)
bullets(s, [
    "CAPM con beta sectorial de Damodaran (ene-2025): Rf 5,0% + β 1,15 × prima 6,0% + riesgo país 3,0%",
    "El VAN positivo y TIR > Ke indican creación de valor para los inversionistas, condicionada a las palancas del cap. 19",
], Inches(0.7), Inches(5.6), Inches(11.9), Inches(1.2), size=14)
pie(s, 14)
notas(s, "Pregunta esperable: '¿por qué 10 años?' — La guía lo permite expresamente; a 5 años el SaaS sigue en "
         "ramp-up (VAN −522 k). Se reporta el VAN ajustado (+204 k) como esperado ponderado de escenarios.")

# ============================================================ 15. SENSIBILIDAD
s = base("Sensibilización del proyecto", "Capítulo 19 del informe · Excel (hoja Escenarios)")
img_fit(s, G + "fig5_escenarios.png", Inches(0.55), Inches(1.6), Inches(12.2), Inches(4.2))
bullets(s, [
    "Escenarios (VAN k USD): pesimista −1.685 · viable +323 · optimista +1.853 (TIR 49,4%)",
    "Variables críticas: velocidad de captura institucional y margen (precio + volumen de estudios)",
    "El piso del pesimista exige mitigación explícita: pilotos tempranos, contratos plurianuales, committed-use cloud",
    "Fase de factibilidad: simulación Monte Carlo (@Risk / Crystal Ball) con 5.000–10.000 iteraciones (guía, punto 19)",
], Inches(0.7), Inches(6.0), Inches(11.9), Inches(1.2), size=13)
pie(s, 15)
notas(s, "Supuestos de cada escenario (Excel): captura año 5 de 12/20/25 instituciones; precio 1.500/2.450/3.000; "
         "churn 20/10/5%; cloud 1,50/0,80/0,80. El diagnóstico original (11 personas) queda documentado en la hoja Escenarios.")

# ============================================================ 16. CONCLUSIONES
s = base("Conclusiones", "Capítulo 20 del informe — proyecto viable condicionado a las palancas")
bullets(s, [
    "Mercado creciente: salud digital +25,7% e IA-ECG +13,7% anual; SAM calificado ≈38 instituciones RM (a validar por catastro)",
    "Tecnología con fundamento: pipeline DSP+ML sobre dataset pediátrico público ZZU; stack open source reduce la inversión",
    "Modelo recurrente: SaaS B2B con suscripción, implementación y uso adicional; white-label/API desde año 3",
    "Evaluación favorable: VAN +323 k, TIR 21,9% (> Ke 14,9%), equilibrio operativo año 4 — con piso de riesgo definido (−1.685 k)",
], Inches(0.7), Inches(1.75), Inches(6.3), Inches(4.6), size=14)
bullets(s, [
    "Debilidades declaradas (cap. 20):",
    ("Sin canal comercial establecido → validar con pilotos del año 1", 1),
    ("Dataset de origen chino → convenios con Sótero del Río / Calvo Mackenna + PTB-XL, MIT-BIH", 1),
    ("Riesgo regulatorio ISP → asesor regulatorio desde el mes 1", 1),
    "Próximos pasos: catastro SAM, encuestas a 5 hospitales, posible 5º socio comercial con experiencia en venta médica",
], Inches(7.3), Inches(1.75), Inches(5.3), Inches(4.6), size=13.5)
pie(s, 16)
notas(s, "El análisis crítico (guía, punto 20) es requisito: debilidades + aspectos a mejorar. "
         "Viable 'condicionado' significa: las palancas del Anexo F son compromisos, no deseos.")

# ============================================================ 17. ENTREGABLES
s = base("Entregables y respaldo documental", "Entrega CANVAS — 9 de noviembre de 2026")
tabla(s, [
    ["Entregable", "Archivo", "Estado"],
    ["Informe Word/PDF (caps. 1–20)", "PedioLink_Informe_PEP_FINAL.docx / PedioLink_Informe.pdf", "Listo"],
    ["Excel con flujos y evaluación económica", "excel/PedioLink_Flujo_Caja.xlsx (Supuestos · Flujo · EERR · Balance · Evaluacion · Escenarios)", "Listo"],
    ["PowerPoint de presentación", "presentacion/PedioLink_Presentacion.pptx", "Listo"],
    ["Anexos con información soportante", "PedioLink_Anexos.docx (Anexos A–M)", "Listo"],
], Inches(0.7), Inches(1.8), Inches(11.9), Inches(2.6), font=12.5,
    col_w=[Inches(3.4), Inches(6.5), Inches(2.0)])
bullets(s, [
    "Anexos A–M: bibliografía APA por capítulo, ficha dataset ZZU, fichas de competidores, marco legal, licitación de referencia, supuestos y trazabilidad, detalle financiero, inversiones, financiamiento, costos, Gantt-PERT, referencias de precios y glosario",
], Inches(0.7), Inches(4.8), Inches(11.9), Inches(1.0), size=13.5)
pie(s, 17)
notas(s, "Trazabilidad: cada cifra de la presentación está en el informe (capítulo citado en el pie) y en el Excel "
         "(fórmulas vivas). Los anexos resuelven la 'información complementaria soportante' de la guía.")

# ============================================================ 18. CIERRE
s = prs.slides.add_slide(BLANK)
side = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
side.fill.solid(); side.fill.fore_color.rgb = PRIMARY
side.line.fill.background(); side.shadow.inherit = False
img_fit(s, G + "fig_logo.png", Inches(3.1), Inches(2.0), Inches(7.1), Inches(2.6))
tb = s.shapes.add_textbox(Inches(2.7), Inches(4.9), Inches(7.9), Inches(1.6))
tf = tb.text_frame; tf.word_wrap = True
for txt, sz, bold, col in [("Gracias — ¿preguntas?", 32, True, WHITE),
                           (GRUPO, 13, False, RGBColor(0xD7, 0xE3, 0xEE)),
                           (CURSO, 12, False, RGBColor(0xD7, 0xE3, 0xEE))]:
    p = tf.paragraphs[0] if bold else tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(6)
    r = p.add_run(); r.text = txt
    r.font.size = Pt(sz); r.font.bold = bold; r.font.color.rgb = col
    r.font.name = "Calibri"
notas(s, "Defensas individuales: 11, 17, 20 nov y 1, 4 dic. Tenida formal-casual. Máximo 25 min, "
         "empezando por el elevator pitch de 60 s.")

prs.save("presentacion/PedioLink_Presentacion.pptx")
print(f"OK presentacion/PedioLink_Presentacion.pptx ({len(prs.slides._sldIdLst)} láminas)")
