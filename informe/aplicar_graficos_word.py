#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica los 10 gráficos de informe/graficos/*.png en PedioLink_Informe_PEP(1).docx
e informe/PedioLink_Informe_PEP.docx con referencias y numeración consecutiva (Figuras 1 a 10).
"""
import os
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOCX_SRC = "PedioLink_Informe_PEP(1).docx"
GRAFICOS_DIR = "informe/graficos"

doc = docx.Document(DOCX_SRC)

def set_image_p(p, img_path, width_in):
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run()
    r.add_picture(os.path.join(GRAFICOS_DIR, img_path), width=Inches(width_in))

def set_caption_p(p, caption_text):
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(caption_text)
    r.italic = True
    r.font.size = Pt(10)

def insert_fig_before(target_p, img_path, width_in, caption_text):
    p_img = target_p.insert_paragraph_before()
    set_image_p(p_img, img_path, width_in)
    p_cap = target_p.insert_paragraph_before()
    set_caption_p(p_cap, caption_text)
    return p_img, p_cap

# =========================================================================
# 1. FIGURA 1: CANVAS (Cap. 3)
# =========================================================================
p_canvas_img = next(p for p in doc.paragraphs if any("image4" in r._r.xml for r in p.runs if hasattr(r, "_r")))
set_image_p(p_canvas_img, "fig1_canvas.png", 6.0)
p_canvas_cap = next(p for p in doc.paragraphs if "Figura 1. Modelo de Negocios Canvas" in p.text)
set_caption_p(p_canvas_cap, "Figura 1. Modelo de Negocios Canvas — PedioLink")
print("✓ Figura 1 actualizada (Canvas)")

# =========================================================================
# 2. FIGURA 2: TAM-SAM-SOM (Cap. 4)
# =========================================================================
p_som = next(p for p in doc.paragraphs if "Mercado objetivo a captar (SOM)" in p.text)
som_lead = p_som.runs[0].text if p_som.runs else "Mercado objetivo a captar (SOM)."
som_body = (
    " Como hipótesis inicial de planificación, se propone incorporar dos instituciones "
    "contratantes durante el primer año de operación. Esta meta deberá contrastarse con el "
    "número de establecimientos calificados, la disposición a pagar, la duración de los procesos "
    "de compra y la capacidad del equipo para implementar y prestar soporte al servicio. La "
    "participación esperada se calculará dividiendo las dos instituciones proyectadas por el "
    "número de establecimientos que conformen el SAM. La Figura 2 sintetiza el dimensionamiento "
    "de mercado bajo la metodología TAM–SAM–SOM del proyecto."
)
p_som.text = ""
r1 = p_som.add_run(som_lead)
r1.bold = True
r2 = p_som.add_run(som_body)

p_demanda = next(p for p in doc.paragraphs if "Los factores que sustentan la proyección de demanda" in p.text)
insert_fig_before(p_demanda, "fig_tam_sam_som.png", 5.8, "Figura 2. Dimensionamiento de mercado TAM–SAM–SOM — PedioLink")
print("✓ Figura 2 insertada (TAM-SAM-SOM)")

# =========================================================================
# 3. FIGURA 3: PARTICIPACIÓN PROYECTADA (Cap. 5)
# =========================================================================
p_part_text = next(p for p in doc.paragraphs if "Estos porcentajes expresan penetración respecto del universo general" in p.text)
p_part_text.text = (
    "Estos porcentajes expresan penetración respecto del universo general de establecimientos, "
    "no una cuota comprobada del mercado pediátrico. Deberán recalcularse una vez identificado "
    "el mercado calificado. La facturación anual dependerá de los meses efectivamente contratados "
    "por cada institución, además de los servicios de implementación y del consumo adicional. "
    "La Figura 3 ilustra la trayectoria de penetración institucional proyectada en el horizonte "
    "de diez años (etapa RM y posterior expansión nacional)."
)
p_ciclo = next(p for p in doc.paragraphs if "Ciclo de vida del producto" in p.text)
insert_fig_before(p_ciclo, "fig_participacion.png", 5.8, "Figura 3. Participación de mercado proyectada — instituciones activas por año (caso viable)")
print("✓ Figura 3 insertada (Participación)")

# =========================================================================
# 4. FIGURA 4: LOGO / MARCA (Cap. 6)
# =========================================================================
p_logo_text = next(p for p in doc.paragraphs if "La marca comercial del proyecto es PedioLink" in p.text)
p_logo_text.text = (
    'La marca comercial del proyecto es PedioLink, nombre compuesto que alude a "pediatría" '
    'y "link" (conexión). El isotipo propuesto consiste en un pulso cardíaco estilizado que '
    'se conecta con un símbolo de nube, simbolizando la conexión entre la señal cardíaca '
    'pediátrica y la plataforma cloud (ver Figura 4). El nombre es memorable, fácilmente '
    'pronunciable en español e inglés, y disponible para registro de marca en INAPI.'
)
p_cap7 = next(p for p in doc.paragraphs if p.text.strip() == "7. Plan Productivo / Operacional")
insert_fig_before(p_cap7, "fig_logo.png", 4.5, "Figura 4. Isotipo y marca comercial PedioLink")
print("✓ Figura 4 insertada (Logo)")

# =========================================================================
# 5 y 6. FIGURAS 5 Y 6: BPMN Y LAYOUT (Cap. 7)
# =========================================================================
p_bpmn_text = next(p for p in doc.paragraphs if "El modelo de proceso de negocio (BPMN) se simplifica" in p.text)
p_bpmn_text.text = (
    "El modelo de proceso de negocio (BPMN) se sintetiza en la Figura 5, comprendiendo desde "
    "la exportación del archivo ECG digital y su validación de integridad hasta el procesamiento "
    "DSP+ML en la nube, generación del reporte clínico y emisión de alertas tempranas ante "
    "arritmias críticas. Por su parte, la distribución física de la oficina (100 m² en Providencia "
    "a partir del año 3) se detalla en la Figura 6, contemplando open space técnico, sala de "
    "reuniones y sala de capacitación para simulación de flujos hospitalarios (el procesamiento "
    "y almacenamiento corren íntegramente en la nube de AWS, sin requerir bodega física ni sala "
    "de servidores)."
)
p_cap8 = next(p for p in doc.paragraphs if p.text.strip() == "8. Solución Técnica Requerida")
insert_fig_before(p_cap8, "fig_bpmn.png", 6.0, "Figura 5. Proceso de negocio (BPMN simplificado) — PedioLink")
insert_fig_before(p_cap8, "fig_layout.png", 5.8, "Figura 6. Layout de la operación — PedioLink (oficina 100 m²)")
print("✓ Figuras 5 y 6 insertadas (BPMN y Layout)")

# =========================================================================
# 7. FIGURA 7: GANTT (Cap. 9, antes Figura 2)
# =========================================================================
p_gantt_ref = next(p for p in doc.paragraphs if "presenta el cronograma de actividades con identificación de la ruta crítica" in p.text)
p_gantt_ref.text = (
    "La puesta en marcha de PedioLink se planifica en un horizonte de ocho meses desde la "
    "constitución de la sociedad hasta el lanzamiento comercial. La Figura 7 presenta el "
    "cronograma de actividades con identificación de la ruta crítica."
)
p_gantt_img = next(p for p in doc.paragraphs if any("image3" in r._r.xml for r in p.runs if hasattr(r, "_r")))
set_image_p(p_gantt_img, "fig2_gantt.png", 6.0)
p_gantt_cap = next(p for p in doc.paragraphs if "Carta Gantt — PedioLink hasta puesta en marcha" in p.text)
set_caption_p(p_gantt_cap, "Figura 7. Carta Gantt — Puesta en marcha de PedioLink (8 meses)")
print("✓ Figura 7 actualizada (Gantt)")

# =========================================================================
# 8. FIGURA 8: ORGANIGRAMA (Cap. 14, antes Figura 3)
# =========================================================================
p_org_ref = next(p for p in doc.paragraphs if "El equipo de PedioLink en su año 1 está compuesto por 7 personas" in p.text)
p_org_ref.text = (
    "El equipo de PedioLink en su año 1 está compuesto por 7 personas bajo la dirección del "
    "CEO; la dotación escala a ~14 al año 10 según la captura. La Figura 8 presenta el organigrama."
)
p_org_img = next(p for p in doc.paragraphs if any("image2" in r._r.xml for r in p.runs if hasattr(r, "_r")))
set_image_p(p_org_img, "fig3_organigrama.png", 6.0)
p_org_cap = next(p for p in doc.paragraphs if "Organigrama PedioLink — Año 1" in p.text)
set_caption_p(p_org_cap, "Figura 8. Organigrama PedioLink — Año 1 (Estructura ajustada)")
print("✓ Figura 8 actualizada (Organigrama)")

# =========================================================================
# 9. FIGURA 9: FLUJO DE CAJA (Cap. 17, antes Figura 4)
# =========================================================================
p_flujo_ref = next(p for p in doc.paragraphs if "EBITDA negativo durante el ramp-up" in p.text)
p_flujo_ref.text = (
    "La proyección muestra EBITDA negativo durante el ramp-up (años 1-3), punto de equilibrio "
    "operativo en el año 4 y equilibrio financiero (flujo acumulado positivo) en el año 7. "
    "El detalle mensual y las fórmulas de cada componente se encuentran en la hoja 'Flujo de Caja' "
    "del Excel adjunto. La Figura 9 ilustra gráficamente la evolución del flujo proyectado y acumulado."
)
p_flujo_img = next(p for p in doc.paragraphs if any("image1" in r._r.xml for r in p.runs if hasattr(r, "_r")))
set_image_p(p_flujo_img, "fig4_flujo.png", 6.0)
# Buscar especificamente la caption de Figura 4 (no la Tabla 6)
p_flujo_cap = next(p for p in doc.paragraphs if "Figura 4. Flujo de Caja proyectado" in p.text)
set_caption_p(p_flujo_cap, "Figura 9. Flujo de Caja proyectado — Caso viable (10 años)")
print("✓ Figura 9 actualizada (Flujo)")

# =========================================================================
# 10. FIGURA 10: ESCENARIOS (Cap. 19, antes Figura 5)
# =========================================================================
p_esc_ref = next(p for p in doc.paragraphs if "La sensibilización del proyecto evalúa la robustez" in p.text)
p_esc_ref.text = (
    "La sensibilización del proyecto evalúa la robustez de los indicadores económicos ante "
    "variaciones en las variables clave. Se construyen tres escenarios (Pesimista, Normal y "
    "Optimista) modificando las variables críticas: la velocidad de captura de instituciones, "
    "el precio de la suscripción, el volumen de estudios, el churn, el costo cloud y la inversión "
    "inicial. La Tabla 8 sintetiza los resultados y la Figura 10 compara gráficamente el VAN y "
    "la TIR por escenario frente a la tasa de descuento."
)
p_esc_img = next(p for p in doc.paragraphs if any("image5" in r._r.xml for r in p.runs if hasattr(r, "_r")))
set_image_p(p_esc_img, "fig5_escenarios.png", 6.0)
p_esc_cap = next(p for p in doc.paragraphs if "VAN y TIR por escenario — PedioLink" in p.text)
set_caption_p(p_esc_cap, "Figura 10. Sensibilización por escenarios (VAN y TIR) — PedioLink")
print("✓ Figura 10 actualizada (Escenarios)")

# Guardar en archivo raíz y en informe/
doc.save(DOCX_SRC)
os.makedirs("informe", exist_ok=True)
doc.save("informe/PedioLink_Informe_PEP.docx")
print("✓ Documento guardado exitosamente en PedioLink_Informe_PEP(1).docx e informe/PedioLink_Informe_PEP.docx")
