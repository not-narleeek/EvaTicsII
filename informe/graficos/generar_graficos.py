#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los 9 gráficos del informe PedioLink en informe/graficos/*.png (200 dpi).
Datos desde el modelo viable (excel/generar_excel.py). Uso: python3 informe/graficos/generar_graficos.py
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle, Polygon

OUT = os.path.join(os.path.dirname(__file__))
AZUL, CELESTE, VERDE, ROJO, AMBAR, GRIS = '#1F4E79', '#5B9BD5', '#70AD47', '#C00000', '#FFC000', '#8496B0'
plt.rcParams.update({'font.size': 10, 'font.family': 'DejaVu Sans'})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('  ✓', name)

# ---------------------------------------------------------- 1. CANVAS (color-coded)
def canvas():
    fig, ax = plt.subplots(figsize=(13, 7.2))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')
    blocks = {  # (x, y, w, h, titulo, items, color)
        'Socios clave': (0, 3.6, 2.4, 3.3, ['Universidades (dataset, validación)', 'AWS (cloud)', 'Asesor clínico pediátrico',
                                            'CORFO/ANID (fondo)', 'Sociedades médicas (SOCHICARDIO, SOCHIPE)'], GRIS),
        'Actividades clave': (2.55, 3.6, 2.4, 1.58, ['Pipeline DSP + ML', 'Validación clínica', 'Onboarding e integración HIS/HL7'], AZUL),
        'Recursos clave': (2.55, 1.85, 2.4, 1.58, ['Dataset ECG pediátrico', 'Equipo salud + TIC', 'Plataforma cloud certificable'], AZUL),
        'Propuesta de valor': (5.1, 3.6, 2.8, 3.3, ['Apoyo a interpretación de ECG pediátrico',
                                                    'Especialización por arritmia y edad', 'Usa los equipos ECG existentes',
                                                    'Revisión centralizada + alertas tempranas', 'Acompañamiento e implementación'],
                              VERDE, True),
        'Relación con clientes': (8.05, 3.6, 2.4, 1.58, ['Venta consultiva B2B', 'Soporte dedicado', 'Capacitación continua'], CELESTE),
        'Canales': (8.05, 1.85, 2.4, 1.58, ['Venta directa a hospitales/clínicas', 'Licitaciones públicas', 'Web y demostraciones'], CELESTE),
        'Segmentos de clientes': (10.6, 3.6, 2.4, 3.3, ['Hospitales públicos con pediatría', 'Clínicas privadas con pediatría',
                                                        'Complejos con cardiólogo pediatra', '(fase 2: ISAPRES y redes)',
                                                        '(fase 2: white-label/API)'], AMBAR, True),
        'Estructura de costos': (0, 0.15, 6.3, 1.5, ['Fijos: equipo (7), cloud base, coworking/oficina, marketing',
                                                     'Variables: USD 0,80 por estudio; licencias; soporte'], '#D64545'),
        'Fuentes de ingresos': (6.45, 0.15, 6.55, 1.5, ['Suscripción institucional: USD 2.450/mes (mix 3.000/2.500/1.500)',
                                                        'Implementación: USD 8.000 una vez · Estudios adicionales: USD 8',
                                                        'White-label/API desde año 3 (~10% de la suscripción)'], '#2E8B57'),
    }
    for titulo, (x, y, w, h, items, color, *resto) in blocks.items():
        highlight = bool(resto and resto[0])
        box = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.06',
                             fc='white', ec=color, lw=3 if highlight else 1.6)
        ax.add_patch(box)
        ax.add_patch(Rectangle((x, y + h - 0.52), w, 0.52, fc=color, ec='none', alpha=0.92 if highlight else 0.25))
        ax.text(x + w / 2, y + h - 0.26, titulo, ha='center', va='center',
                fontsize=9.2 if len(titulo) > 18 else 10.5, fontweight='bold',
                color='white' if highlight else '#1a1a2e')
        ax.text(x + 0.14, y + h - 0.72, '\n'.join(f'• {i}' for i in items), fontsize=8.1, va='top')
    ax.text(6.5, -0.15, 'Color-coded: verde = Propuesta de Valor · ámbar = Segmentos de clientes '
                        '(el par define el ajuste problema-solución)',
            ha='center', fontsize=9, style='italic', color=VERDE)
    ax.set_title('Modelo de Negocios Canvas — PedioLink', fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig1_canvas.png')

# ---------------------------------------------------------- 2. GANTT
def gantt():
    acts = [  # (nombre, mes_inicio, mes_fin, crítica, holgura_semanas)
        ('1. Constitución SPA + capital', 1, 2, True, 0),
        ('2. Desarrollo plataforma + multi-tenancy', 1, 6, True, 0),
        ('3. Dataset + validación retrospectiva pipeline', 2, 5, True, 0),
        ('4. Convenios piloto (hospital RM)', 3, 6, False, 2),
        ('5. Piloto clínico 50 pacientes', 6, 7, True, 0),
        ('6. Preparación comercial + marketing', 5, 8, False, 3),
        ('7. Lanzamiento comercial', 8, 8, True, 0),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    for i, (nom, a, b, crit, holg) in enumerate(acts):
        y = len(acts) - i
        color = ROJO if crit else CELESTE
        ax.barh(y, b - a + 0.72, left=a - 0.36, height=0.56, color=color, alpha=0.88, zorder=3)
        if holg:
            ax.barh(y, holg / 4.33, left=b + 0.4, height=0.56, color='none', ec=GRIS,
                    hatch='///', zorder=3)
            ax.text(b + 0.45 + holg / 4.33, y, f' {holg} sem holgura', va='center', fontsize=8, color=GRIS)
        ax.text(a - 0.5, y, nom, ha='right', va='center', fontsize=9.2,
                fontweight='bold' if crit else 'normal')
    ax.set_xlim(-6.8, 10.5); ax.set_ylim(0.3, len(acts) + 0.7)
    ax.set_xticks(range(1, 9)); ax.set_xticklabels([f'M{m}' for m in range(1, 9)])
    ax.grid(axis='x', alpha=0.3, zorder=0); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.set_yticks([])
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=ROJO, label='Ruta crítica (1→2→3→5→7)'),
                       Patch(fc=CELESTE, label='Con holgura')],
              loc='upper center', bbox_to_anchor=(0.5, -0.09), ncols=2,
              fontsize=9.5, frameon=False)
    ax.set_title('Carta Gantt — puesta en marcha de PedioLink (8 meses)', fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig2_gantt.png')

# ---------------------------------------------------------- 3. ORGANIGRAMA (estructura ajustada, 7 personas)
def organigrama():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.4); ax.axis('off')

    def caja(x, y, w, h, texto, color, fs=9.3):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.05',
                                    fc='white', ec=color, lw=2))
        ax.text(x, y, texto, ha='center', va='center', fontsize=fs, fontweight='bold')

    def linea(x1, y1, x2, y2):
        ax.plot([x1, x1, x2, x2], [y1, (y1 + y2) / 2, (y1 + y2) / 2, y2], color=GRIS, lw=1.4, zorder=1)

    caja(6, 4.8, 3.2, 0.75, 'CEO\n(estrategia, capital, clientes clave)', AZUL)
    caja(2.0, 3.3, 2.6, 0.72, 'CTO\n(arquitectura, ML, seguridad)', AZUL)
    caja(5.6, 3.3, 2.6, 0.72, 'Director Comercial\n(ventas, convenios)', CELESTE)
    caja(8.9, 3.3, 2.6, 0.72, 'Director Médico (MT)\n(validación clínica, sociedades)', VERDE)
    caja(11.1, 4.8, 1.7, 0.75, 'Admin. y Finanzas\n(1, part-time)', GRIS, 8.3)
    caja(0.9, 1.9, 1.8, 0.7, 'Dev ML ×2', AZUL)
    caja(2.9, 1.9, 1.9, 0.7, 'Ing. Cloud/DevOps ×1', AZUL)
    caja(5.6, 1.9, 1.9, 0.7, 'Ejecutivo/a comercial ×1', CELESTE)
    linea(6, 4.42, 6, 4.1); linea(2, 4.1, 11.1, 4.1)
    for x in (2.0, 5.6, 8.9, 11.1):
        linea(x, 4.1, x, 3.66)
    linea(0.9, 2.94, 2.9, 2.94); linea(2, 2.94, 2, 2.25); linea(2.9, 2.94, 2.9, 2.25)
    linea(5.6, 2.94, 5.6, 2.25)
    ax.text(6, 0.7, 'Estructura año 1: 7 personas (socios con sueldo parcial). Escala a ~14 al año 10.\n'
                    'Outsourcing: contabilidad y asesoría legal (ver cap. 12/14).',
            ha='center', fontsize=9, style='italic', color='#444')
    ax.set_title('Organigrama PedioLink — año 1 (estructura ajustada del caso viable)',
                 fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig3_organigrama.png')

# ---------------------------------------------------------- 4. FLUJO DE CAJA (Figura 4 corregida)
def flujo():
    anios = list(range(0, 11))
    fl = [-285, -175.5, -201.5, -108.2, 42.8, 230.4, 301.7, 391.1, 484.0, 525.7, 1027.4]
    acum, s = [], 0
    for f in fl:
        s += f; acum.append(s)
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    colores = [ROJO if f < 0 else VERDE for f in fl]
    ax.bar(anios, fl, color=colores, alpha=0.85, zorder=3, label='Flujo del año')
    ax.plot(anios, acum, 'o-', color=AZUL, lw=2.2, ms=5, zorder=4, label='Flujo acumulado')
    ax.axhline(0, color='#333', lw=0.8)
    ax.annotate('VAN (10 años, Ke 14,9%)\n= +323 k USD · TIR 21,9%\nPRI 6,5 años', xy=(10, 1027),
                xytext=(6.6, 880), fontsize=9.5, fontweight='bold', color=AZUL,
                bbox=dict(fc='white', ec='none', alpha=0.85),
                arrowprops=dict(arrowstyle='->', color=AZUL))
    ax.set_xticks(anios); ax.set_xticklabels([f'Año {a}' for a in anios], fontsize=9)
    ax.set_ylabel('Miles de USD'); ax.grid(axis='y', alpha=0.3, zorder=0); ax.set_axisbelow(True)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.legend(fontsize=9.5, frameon=False, loc='upper left')
    ax.set_title('Flujo de caja proyectado — caso viable (10 años; corte a 5 años: −522 k)',
                 fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig4_flujo.png')

# ---------------------------------------------------------- 5. ESCENARIOS (Figura 5)
def escenarios():
    nombres = ['Pesimista', 'VIABLE\n(adoptado)', 'Optimista', 'Diagnóstico\noriginal']
    vans = [-1685, 323, 1853, -2968]
    colores = [ROJO, VERDE, CELESTE, GRIS]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={'width_ratios': [1.15, 1]})
    b = ax1.bar(nombres, vans, color=colores, alpha=0.88, zorder=3)
    ax1.axhline(0, color='#333', lw=0.9)
    for rect, v in zip(b, vans):
        ax1.text(rect.get_x() + rect.get_width() / 2, v + (60 if v > 0 else -140),
                 f'{v:+,} k'.replace(',', '.'), ha='center', fontsize=9.5, fontweight='bold')
    ax1.set_ylabel('VAN (miles USD) @ Ke 14,9%')
    ax1.grid(axis='y', alpha=0.3, zorder=0); ax1.set_axisbelow(True)
    for sp in ('top', 'right'): ax1.spines[sp].set_visible(False)
    ax1.set_title('VAN por escenario', fontsize=12, fontweight='bold')
    tir_n = ['—', '21,9%', '49,4%', '—']
    b2 = ax2.bar(nombres, [0, 21.9, 49.4, 0], color=colores, alpha=0.88, zorder=3)
    ax2.axhline(14.9, color=ROJO, lw=1.8, ls='--')
    ax2.text(3.42, 15.8, 'Ke = 14,9%', color=ROJO, fontsize=9, ha='right')
    for rect, t in zip(b2, tir_n):
        ax2.text(rect.get_x() + rect.get_width() / 2, 1.5, t, ha='center', fontsize=9.5,
                 fontweight='bold', color='white' if t != '—' else '#666')
    ax2.set_ylabel('TIR (%)')
    ax2.grid(axis='y', alpha=0.3, zorder=0); ax2.set_axisbelow(True)
    for sp in ('top', 'right'): ax2.spines[sp].set_visible(False)
    ax2.set_title('TIR por escenario (vs. tasa de descuento)', fontsize=12, fontweight='bold')
    fig.suptitle('Sensibilización — PedioLink (VAN esperado ponderado: +204 k USD)',
                 fontsize=13, fontweight='bold')
    fig.tight_layout()
    save(fig, 'fig5_escenarios.png')

# ---------------------------------------------------------- 6. BPMN (cap. 7)
def bpmn():
    fig, ax = plt.subplots(figsize=(13, 3.7))
    ax.set_xlim(0, 13.5); ax.set_ylim(0, 3.75); ax.axis('off')
    # pistas
    ax.add_patch(Rectangle((0.15, 1.9), 3.35, 1.45, fc='#F2F2F2', ec=GRIS, lw=1))
    ax.text(0.3, 3.16, 'Hospital / clínica', ha='left', fontsize=9, fontweight='bold', color='#444')
    ax.add_patch(Rectangle((3.65, 1.9), 9.5, 1.45, fc='#EDF3FA', ec=AZUL, lw=1))
    ax.text(3.8, 3.16, 'Plataforma PedioLink (cloud)', ha='left', fontsize=9, fontweight='bold', color=AZUL)
    # inicio
    ax.add_patch(Circle((0.85, 2.5), 0.26, fc=VERDE, ec='#3d7a2a', lw=1.5))
    ax.text(0.85, 1.42, 'ECG realizado\na paciente', ha='center', va='top', fontsize=7.8)
    tareas = [  # (x, ancho, etiqueta, dentro_plataforma)
        (2.25, 1.95, 'Exportar archivo\nWFDB / DICOM-ECG', False),
        (4.75, 1.9, '1. Recepción y\nvalidación de archivo', True),
        (7.0, 1.9, '2. Filtrado DSP +\ncaracterísticas + ML', True),
        (9.25, 1.9, '3. Reporte + nivel de\ncerteza al dashboard', True),
        (11.5, 1.9, '4. Alerta temprana si\narritmia crítica', True),
    ]
    prev_x = 1.11
    for x, w, lab, in_pf in tareas:
        color = AZUL if in_pf else GRIS
        ax.add_patch(FancyBboxPatch((x - w / 2, 2.02), w, 0.96, boxstyle='round,pad=0.04',
                                    fc='white', ec=color, lw=1.8))
        ax.text(x, 2.5, lab, ha='center', va='center', fontsize=7.9)
        ax.add_patch(FancyArrowPatch((prev_x, 2.5), (x - w / 2 - 0.05, 2.5),
                                     arrowstyle='-|>', mutation_scale=13, color='#555', lw=1.3))
        prev_x = x + w / 2
    # fin
    ax.add_patch(Circle((13.15, 2.5), 0.24, fc=ROJO, ec='#8b0000', lw=1.5))
    ax.add_patch(Circle((13.15, 2.5), 0.15, fc='white', ec=ROJO, lw=1.2))
    ax.add_patch(FancyArrowPatch((prev_x, 2.5), (12.87, 2.5), arrowstyle='-|>',
                                 mutation_scale=13, color='#555', lw=1.3))
    ax.text(6.75, 0.95, 'Revisión y decisión clínica: siempre del médico tratante (el reporte es de apoyo, con certeza\n'
                        'y limitaciones indicadas). Integración HL7 v2 / FHIR R4 al registro electrónico cuando exista.',
            ha='center', va='top', fontsize=8.3, style='italic', color='#444')
    ax.set_title('Proceso de negocio (BPMN simplificado) — PedioLink', fontsize=13, fontweight='bold', pad=8)
    save(fig, 'fig_bpmn.png')

# ---------------------------------------------------------- 7. LAYOUT (cap. 7)
def layout():
    fig, ax = plt.subplots(figsize=(11.5, 6))
    ax.set_xlim(0, 11.5); ax.set_ylim(0, 6); ax.axis('off')
    ax.add_patch(Rectangle((0.4, 0.5), 10.7, 5.0, fc='#FAFBFD', ec='#333', lw=2))
    ax.text(5.75, 5.72, 'Oficina 100 m² — Providencia (coworking año 1-2; sin bodega: no hay hardware)',
            ha='center', fontsize=11.5, fontweight='bold')
    zonas = [
        ('Open space técnico\n6 puestos (devs, cloud, CTO)', 0.75, 3.0, 4.6, 2.1, AZUL),
        ('Sala de reuniones /\ndemostraciones a clientes', 5.6, 3.0, 2.6, 2.1, CELESTE),
        ('Sala de capacitación\n(mock-up de flujo hospital)', 8.45, 3.0, 2.4, 2.1, VERDE),
        ('Dirección y venta\n(CEO, comercial)', 0.75, 0.85, 3.0, 1.7, CELESTE),
        ('Coordinación clínica\n(médico MT, pilotajes)', 3.95, 0.85, 3.0, 1.7, VERDE),
        ('Kitchenette /\ninformal', 7.15, 0.85, 1.8, 1.7, GRIS),
        ('Recepción', 9.15, 0.85, 1.7, 1.7, GRIS),
    ]
    for nom, x, y, w, h, c in zonas:
        ax.add_patch(Rectangle((x, y), w, h, fc='white', ec=c, lw=2))
        ax.text(x + w / 2, y + h / 2, nom, ha='center', va='center', fontsize=8.8)
    ax.annotate('entrada', xy=(10.0, 0.5), xytext=(10.0, 0.14), ha='center', fontsize=8,
                arrowprops=dict(arrowstyle='->', color='#333'))
    ax.set_title('Layout de la operación — PedioLink (SaaS: el "hub" de procesamiento es AWS, no una sala de servidores)',
                 fontsize=12, fontweight='bold', pad=10)
    save(fig, 'fig_layout.png')

# ---------------------------------------------------------- 8. TAM-SAM-SOM (cap. 4)
def mercado():
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    niveles = [
        ('TAM — hospitales y clínicas de Chile con pediatría y ECG digital', 115, AZUL,
         '≈ 30% de 382 establecimientos (BCN 2025); SUPUESTO a validar'),
        ('SAM — Región Metropolitana calificada', 38, CELESTE,
         '≈ 30% de 128 RM (45 hospitales + 83 clínicas)'),
        ('SOM año 5 — clientes activos (caso viable)', 20, VERDE,
         '≈ 53% del SAM RM; expansión nacional desde año 6'),
        ('SOM año 10', 37, '#2E8B57', '≈ 32% del universo nacional calificado'),
    ]
    maxv = 115
    for i, (nom, v, c, nota) in enumerate(niveles):
        y = 3.6 - i * 1.0
        w = 8.6 * v / maxv
        ax.add_patch(FancyBboxPatch((1.7, y), max(w, 0.5), 0.62, boxstyle='round,pad=0.03',
                                    fc=c, ec='none', alpha=0.85))
        ax.text(1.55, y + 0.31, nom, ha='right', va='center', fontsize=9.2)
        ax.text(1.8 + max(w, 0.5) + 0.12, y + 0.31, f'{v} inst.', va='center', fontsize=10,
                fontweight='bold', color=c)
        ax.text(1.55, y - 0.13, nota, ha='right', fontsize=7.6, color='#666', style='italic')
    ax.set_xlim(0, 11); ax.set_ylim(-0.6, 4.5); ax.axis('off')
    ax.set_title('Dimensionamiento de mercado TAM–SAM–SOM — PedioLink', fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig_tam_sam_som.png')

# ---------------------------------------------------------- 9. PARTICIPACIÓN (cap. 5)
def participacion():
    anios = list(range(1, 11))
    inst = [2, 5, 9, 14, 20, 25, 30, 34, 36, 37]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    colores = [CELESTE if a <= 5 else VERDE for a in anios]
    ax.bar(anios, inst, color=colores, alpha=0.88, zorder=3)
    for a, v in zip(anios, inst):
        ax.text(a, v + 0.5, str(v), ha='center', fontsize=9, fontweight='bold')
    ax.axvline(5.5, color=GRIS, ls='--', lw=1.2)
    ax.text(5.65, 34.5, 'expansión nacional\n(desde año 6)', fontsize=8.5, color=GRIS)
    ax.set_xticks(anios); ax.set_xlabel('Año de operación')
    ax.set_ylabel('Instituciones activas al cierre')
    ax.set_ylim(0, 42)
    ax.grid(axis='y', alpha=0.3, zorder=0); ax.set_axisbelow(True)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=CELESTE, label='RM (SAM 38; año 5 = 53% del SAM)'),
                       Patch(fc=VERDE, label='RM + regiones (≈32% del universo nacional calificado)')],
              fontsize=9, frameon=False, loc='upper left')
    ax.set_title('Participación proyectada — instituciones activas por año (caso viable)',
                 fontsize=13, fontweight='bold', pad=10)
    save(fig, 'fig_participacion.png')

# ---------------------------------------------------------- 10. LOGO (cap. 6)
def logo():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.set_xlim(0, 7); ax.set_ylim(0, 3.2); ax.axis('off')
    # nube (glifo limpio)
    ax.text(5.75, 2.5, '☁', fontsize=110, color=AZUL, ha='center', va='center', zorder=2)
    # trazo de pulso que conecta con la nube
    xs = [0.4, 1.5, 1.9, 2.15, 2.4, 2.9, 3.3, 3.55, 3.8, 4.55]
    ys = [1.55, 1.55, 1.15, 2.45, 0.85, 1.55, 1.55, 1.75, 1.55, 2.1]
    ax.plot(xs, ys, color=ROJO, lw=3.2, solid_capstyle='round', zorder=3)
    ax.add_patch(FancyArrowPatch((4.55, 2.1), (5.05, 2.42), arrowstyle='-|>',
                                 mutation_scale=18, color=ROJO, lw=3.4))
    ax.text(0.4, 0.55, 'PedioLink', fontsize=26, fontweight='bold', color=AZUL)
    ax.text(2.62, 0.62, '', fontsize=12)
    ax.text(0.42, 0.25, 'soporte diagnóstico de arritmias pediátricas', fontsize=9, color='#555', style='italic')
    save(fig, 'fig_logo.png')

canvas(); gantt(); organigrama(); flujo(); escenarios(); bpmn(); layout(); mercado(); participacion(); logo()
print("Listo: 10 gráficos en", OUT)
