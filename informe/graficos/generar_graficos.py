#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los 10 gráficos del informe PedioLink en informe/graficos/*.png (200 dpi).
Datos desde el modelo viable (excel/generar_excel.py). Uso: python3 informe/graficos/generar_graficos.py
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle, Patch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
AZUL, CELESTE, VERDE, ROJO, AMBAR, GRIS = '#1F4E79', '#5B9BD5', '#70AD47', '#C00000', '#EDAE00', '#8496B0'
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'DejaVu Sans',
    'axes.edgecolor': '#444444',
    'axes.linewidth': 0.9,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches='tight', pad_inches=0.2, facecolor='white')
    plt.close(fig)
    print('  ✓', name)


# ---------------------------------------------------------- 1. CANVAS (color-coded)
def canvas():
    fig, ax = plt.subplots(figsize=(14.5, 8.0))
    ax.set_xlim(-0.15, 14.15)
    ax.set_ylim(-0.45, 7.35)
    ax.axis('off')

    # (x, y, w, h, titulo, items, color, highlight)
    blocks = [
        (0.0, 2.05, 2.68, 4.75, 'Socios clave', [
            'Universidades (dataset\n  y validación clínica)',
            'AWS (infraestructura\n  cloud)',
            'Asesor clínico pediátrico',
            'CORFO / ANID (fondos)',
            'Sociedades médicas\n  (SOCHICARDIO,\n  SOCHIPE)',
        ], GRIS, False),
        (2.82, 4.50, 2.68, 2.30, 'Actividades clave', [
            'Pipeline DSP + ML',
            'Validación retrospectiva\n  y piloto prospectivo',
            'Integración HIS /\n  HL7 v2 / FHIR R4',
        ], AZUL, False),
        (2.82, 2.05, 2.68, 2.30, 'Recursos clave', [
            'Dataset ECG pediátrico\n  (ZZU, Tan et al. 2025)',
            'Equipo salud + TIC\n  (7 personas en año 1)',
            'Plataforma cloud AWS',
        ], AZUL, False),
        (5.64, 2.05, 2.72, 4.75, 'Propuesta de valor', [
            'Apoyo a interpretación\n  de ECG pediátrico\n  (DSP + ML)',
            'Especialización por\n  arritmia y edad',
            'Compatible con equipos\n  ECG existentes',
            'Revisión centralizada y\n  alertas tempranas',
            'Acompañamiento e\n  implementación',
        ], VERDE, True),
        (8.50, 4.50, 2.68, 2.30, 'Relación con clientes', [
            'Venta consultiva B2B',
            'Soporte técnico dedicado',
            'Capacitación continua\n  al equipo clínico',
        ], CELESTE, False),
        (8.50, 2.05, 2.68, 2.30, 'Canales', [
            'Venta directa a\n  hospitales y clínicas',
            'Licitaciones públicas\n  (Mercado Público)',
            'Web y demostraciones',
        ], CELESTE, False),
        (11.32, 2.05, 2.68, 4.75, 'Segmentos de clientes', [
            'Hospitales públicos con\n  servicio de pediatría',
            'Clínicas privadas con\n  unidad pediátrica',
            'Centros de salud con\n  cardiólogo pediatra',
            'Fase 2: redes e ISAPRES',
            'Fase 2: licenciamiento\n  white-label / API',
        ], AMBAR, True),
        (0.0, 0.20, 6.90, 1.68, 'Estructura de costos', [
            'Costos fijos (USD 21,6 k/mes año 1): equipo de 7 personas (USD 12,5 k/mes),\n'
            '  cloud base AWS (USD 2,5 k/mes), coworking (USD 0,9 k/mes), marketing y servicios.',
            'Costos variables: USD 0,80 por estudio ECG procesado\n'
            '  (procesamiento cloud, almacenamiento y soporte técnico).',
        ], '#D64545', False),
        (7.10, 0.20, 6.90, 1.68, 'Fuentes de ingresos', [
            'Suscripción institucional: USD 2.450/mes promedio (mix USD 1.500 / 2.500 / 3.000).',
            'Implementación inicial: USD 8.000 (una vez) · Estudios adicionales: USD 8 c/u.',
            'White-label / API desde el año 3 (~10% adicional sobre la suscripción).',
        ], '#2E8B57', False),
    ]

    for x, y, w, h, titulo, items, color, highlight in blocks:
        # Fondo del bloque
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.0,rounding_size=0.12',
            fc='#FAFCFF' if not highlight else '#F9FFF6' if color == VERDE else '#FFFDF4',
            ec=color,
            lw=2.8 if highlight else 1.6,
            zorder=2
        )
        ax.add_patch(box)

        # Cabecera del bloque
        header_h = 0.50
        header = FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle='round,pad=0.0,rounding_size=0.12',
            fc=color,
            ec=color,
            lw=1.0,
            alpha=0.95 if highlight else 0.22,
            zorder=3
        )
        ax.add_patch(header)

        ax.text(
            x + w / 2, y + h - header_h / 2, titulo,
            ha='center', va='center',
            fontsize=10.2, fontweight='bold',
            color='white' if highlight else '#1A2536',
            zorder=4
        )

        # Texto de viñetas
        body = '\n'.join(f'• {item}' for item in items)
        ax.text(
            x + 0.14, y + h - header_h - 0.15, body,
            fontsize=8.3, va='top', ha='left',
            color='#222222', linespacing=1.28,
            zorder=4
        )

    ax.text(
        7.0, -0.22,
        'Código de color: Verde = Propuesta de Valor  ·  Ámbar = Segmentos de Clientes (el par central define el ajuste problema–solución)',
        ha='center', va='center', fontsize=9.5, style='italic', fontweight='bold', color='#2E6B34'
    )
    ax.set_title('Modelo de Negocios Canvas — PedioLink', fontsize=14, fontweight='bold', pad=12, color='#1A2536')
    save(fig, 'fig1_canvas.png')


# ---------------------------------------------------------- 2. GANTT
def gantt():
    acts = [  # (nombre, mes_inicio, mes_fin, crítica, holgura_semanas)
        ('1. Constitución SPA + levantamiento capital', 1, 2, True, 0),
        ('2. Desarrollo plataforma cloud + multi-tenancy', 1, 6, True, 0),
        ('3. Dataset ZZU + validación retrospectiva', 2, 5, True, 0),
        ('4. Convenios piloto (hospitales/clínicas RM)', 3, 6, False, 2),
        ('5. Piloto clínico prospectivo (50 pacientes)', 6, 7, True, 0),
        ('6. Preparación comercial + marketing B2B', 5, 8, False, 3),
        ('7. Lanzamiento comercial e inicio operación', 8, 8, True, 0),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    n = len(acts)

    for i, (nom, a, b, crit, holg) in enumerate(acts):
        y = n - i
        color = ROJO if crit else CELESTE
        dur = b - a + 1
        left = a - 0.42
        width = dur - 0.16

        ax.barh(y, width, left=left, height=0.55, color=color, alpha=0.90, edgecolor=color, lw=1.2, zorder=3)
        ax.text(left + width / 2, y, f'{dur} {"mes" if dur == 1 else "meses"}',
                ha='center', va='center', color='white', fontsize=8.5, fontweight='bold', zorder=4)

        if holg:
            holg_w = holg / 4.33
            ax.barh(y, holg_w, left=left + width + 0.06, height=0.55,
                    color='none', edgecolor=GRIS, hatch='///', lw=1.2, zorder=3)
            ax.text(left + width + 0.14 + holg_w, y, f'+{holg} sem. holgura',
                    va='center', ha='left', fontsize=8.5, color='#556677', fontweight='bold')

    ax.set_yticks(range(1, n + 1))
    ax.set_yticklabels([a[0] for a in reversed(acts)], fontsize=9.8)
    for ticklabel, (_, _, _, crit, _) in zip(ax.get_yticklabels(), reversed(acts)):
        if crit:
            ticklabel.set_fontweight('bold')
            ticklabel.set_color('#1A2536')

    ax.set_xlim(0.4, 9.6)
    ax.set_ylim(0.3, n + 0.7)
    ax.set_xticks(range(1, 9))
    ax.set_xticklabels([f'Mes {m}' for m in range(1, 9)], fontsize=9.8, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.45, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#888888')
    ax.tick_params(axis='y', length=0, pad=8)

    ax.legend(
        handles=[
            Patch(fc=ROJO, label='Ruta crítica (1 → 2 → 3 → 5 → 7) — sin holgura'),
            Patch(fc=CELESTE, label='Actividades no críticas (con holgura)'),
            Patch(fc='white', ec=GRIS, hatch='///', label='Holgura disponible (semanas)'),
        ],
        loc='upper center', bbox_to_anchor=(0.5, -0.11), ncols=3,
        fontsize=9.5, frameon=False
    )
    ax.set_title('Carta Gantt — Puesta en marcha de PedioLink (8 meses)', fontsize=13.5, fontweight='bold', pad=12, color='#1A2536')
    save(fig, 'fig2_gantt.png')


# ---------------------------------------------------------- 3. ORGANIGRAMA (estructura ajustada, 7 personas)
def organigrama():
    fig, ax = plt.subplots(figsize=(13.0, 5.8))
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0.2, 5.6)
    ax.axis('off')

    def caja(x, y, w, h, titulo, subtitulo, color, bg='#FFFFFF', fs_t=9.6):
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle='round,pad=0.0,rounding_size=0.10',
            fc=bg, ec=color, lw=2.2, zorder=3
        )
        ax.add_patch(box)
        # Barra superior de color
        top_bar = FancyBboxPatch(
            (x - w / 2, y + h / 2 - 0.12), w, 0.12,
            boxstyle='round,pad=0.0,rounding_size=0.05',
            fc=color, ec=color, lw=0.5, zorder=4
        )
        ax.add_patch(top_bar)
        if subtitulo:
            ax.text(x, y + 0.10, titulo, ha='center', va='center', fontsize=fs_t, fontweight='bold', color='#1A2536', zorder=5)
            ax.text(x, y - 0.18, subtitulo, ha='center', va='center', fontsize=8.3, color='#445566', zorder=5)
        else:
            ax.text(x, y - 0.03, titulo, ha='center', va='center', fontsize=fs_t, fontweight='bold', color='#1A2536', zorder=5)

    def conectar(x1, y1, x2, y2, y_mid):
        ax.plot([x1, x1, x2, x2], [y1, y_mid, y_mid, y2], color=GRIS, lw=1.8, zorder=1, solid_capstyle='round')

    # Nivel 1: CEO
    caja(6.3, 4.75, 4.2, 0.86, 'CEO (Socio · Sueldo parcial)', 'Estrategia, levantamiento de capital y clientes clave', AZUL, '#F7FAFC', fs_t=9.8)

    # Nivel 2: Directores
    caja(2.6, 3.10, 3.4, 0.86, 'CTO (Socio)', 'Arquitectura cloud, ML y seguridad', AZUL, fs_t=9.8)
    caja(6.3, 3.10, 3.4, 0.86, 'Director Comercial (Socio)', 'Ventas B2B, licitaciones y convenios', CELESTE, fs_t=9.8)
    caja(10.0, 3.10, 3.4, 0.86, 'Director Médico MT (Socio)', 'Validación clínica y sociedades médicas', VERDE, fs_t=9.8)

    # Nivel 3: Equipo técnico bajo CTO (centrados en x=2.6 -> 1.30 y 3.90)
    caja(1.30, 1.55, 2.38, 0.78, 'Desarrolladores ML ×2', 'Pipeline DSP + modelos IA', AZUL, fs_t=9.1)
    caja(3.90, 1.55, 2.38, 0.78, 'Ing. Cloud / DevOps ×1', 'Infraestructura AWS y HL7', AZUL, fs_t=9.1)

    # Conexiones Nivel 1 -> Nivel 2
    for x_dest in (2.6, 6.3, 10.0):
        conectar(6.3, 4.75 - 0.43, x_dest, 3.10 + 0.43, 3.95)

    # Conexiones Nivel 2 (CTO) -> Nivel 3
    for x_dest in (1.30, 3.90):
        conectar(2.6, 3.10 - 0.43, x_dest, 1.55 + 0.39, 2.32)

    # Nota explicativa
    ax.add_patch(FancyBboxPatch(
        (5.45, 1.16), 6.50, 0.78,
        boxstyle='round,pad=0.0,rounding_size=0.08',
        fc='#F8F9FA', ec='#D0D7DE', lw=1.2, zorder=2
    ))
    ax.text(
        8.70, 1.55,
        'Dotación Año 1: 7 personas = 4 socios (sueldo parcial) + 3 contrataciones técnicas.\n'
        'Escala gradualmente a ~14 personas al año 10 según crecimiento de instituciones activas.\n'
        'Outsourcing: contabilidad y asesoría legal/regulatoria externa (sin personal administrativo fijo).',
        ha='center', va='center', fontsize=8.3, style='italic', color='#334455', linespacing=1.3
    )

    ax.set_title('Organigrama PedioLink — Año 1 (Estructura ajustada del caso viable)',
                 fontsize=13.5, fontweight='bold', pad=10, color='#1A2536')
    save(fig, 'fig3_organigrama.png')


# ---------------------------------------------------------- 4. FLUJO DE CAJA (Figura 4 corregida)
def flujo():
    anios = list(range(0, 11))
    fl = [-285.0, -175.5, -201.5, -108.2, 42.8, 230.4, 301.7, 391.1, 484.0, 525.7, 1027.4]
    acum, s = [], 0.0
    for f in fl:
        s += f
        acum.append(s)

    fig, ax = plt.subplots(figsize=(12.8, 5.6))
    colores = [ROJO if f < 0 else VERDE for f in fl]
    ax.bar(anios, fl, width=0.62, color=colores, alpha=0.88, zorder=3, label='Flujo de caja anual')
    ax.plot(anios, acum, 'o-', color=AZUL, lw=2.5, ms=6.5, zorder=5, label='Flujo de caja acumulado')
    ax.axhline(0, color='#333333', lw=1.0, zorder=2)

    # Etiquetas en las barras
    for a, f in zip(anios, fl):
        if a in (0, 1):
            y_pos = 55
        elif f >= 0:
            y_pos = f + 55
        else:
            y_pos = f - 90
        ax.text(a, y_pos, f'{f:+.0f}' if f > 0 else f'{f:.0f}',
                ha='center', va='center', fontsize=8.3, fontweight='bold',
                color='#1B5E20' if f >= 0 else '#8B0000', zorder=6)

    # Etiquetas seleccionadas del acumulado (en posiciones despejadas)
    acum_labels = [
        (3, -155),   # debajo del mínimo (-770 k)
        (6, -165),   # debajo de Año 6 (-195 k)
        (8, 165),    # encima de Año 8 (+680 k)
        (10, 140),   # encima de Año 10 (+2233 k)
    ]
    for a, dy in acum_labels:
        val = acum[a]
        ax.text(a, val + dy, f'Acum: {val:+.0f} k',
                ha='center', va='center', fontsize=8.0, fontweight='bold', color=AZUL,
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec=AZUL, lw=0.8, alpha=0.92), zorder=6)

    # Punto de payback (PRI = 6,5 años)
    ax.plot([6.39], [0], marker='D', ms=8.5, color=AMBAR, mec='#333', mew=1.2, zorder=7)
    ax.annotate('PRI simple ≈ 6,5 años\n(equilibrio acumulado)',
                xy=(6.39, 0), xytext=(4.4, -520),
                ha='center', fontsize=8.5, fontweight='bold', color='#333333',
                bbox=dict(boxstyle='round,pad=0.3', fc='#FFFDF0', ec=AMBAR, lw=1.2),
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.3), zorder=7)

    # Cuadro resumen en zona despejada (arriba a la izquierda/centro)
    resumen = (
        'Indicadores del Caso Viable (Horizonte 10 años)\n'
        '• Tasa de descuento (CAPM): Ke = 14,9%\n'
        '• VAN (10 años): +323 k USD  (corte a 5 años: −522 k USD)\n'
        '• TIR: 21,9% (+7,0 pp sobre Ke)\n'
        '• PRI simple: 6,5 años  ·  PRI descontado: 8,6 años'
    )
    ax.text(0.15, 1480, resumen, fontsize=9.2, va='top', ha='left', color='#1A2536',
            linespacing=1.38,
            bbox=dict(boxstyle='round,pad=0.5', fc='#F4F8FC', ec=AZUL, lw=1.5), zorder=6)

    ax.set_xticks(anios)
    ax.set_xticklabels([f'Año {a}' for a in anios], fontsize=9.5, fontweight='bold')
    ax.set_ylim(-1050, 2550)
    ax.set_ylabel('Miles de USD', fontsize=10.5, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.35, zorder=0)
    ax.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=9.8, frameon=True, facecolor='white', edgecolor='#DDD', loc='upper left')
    ax.set_title('Flujo de Caja Proyectado — Caso Viable (10 años; incluye valor residual en año 10)',
                 fontsize=13.5, fontweight='bold', pad=12, color='#1A2536')
    save(fig, 'fig4_flujo.png')


# ---------------------------------------------------------- 5. ESCENARIOS (Figura 5)
def escenarios():
    nombres = ['Pesimista', 'VIABLE\n(Adoptado)', 'Optimista', 'Diagnóstico\nOriginal']
    vans = [-1685, 323, 1853, -2968]
    colores = [ROJO, VERDE, CELESTE, GRIS]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2), gridspec_kw={'width_ratios': [1.1, 1]})

    # Panel 1: VAN
    b1 = ax1.bar(nombres, vans, width=0.58, color=colores, alpha=0.90, zorder=3)
    ax1.axhline(0, color='#333333', lw=1.0, zorder=2)
    for rect, v in zip(b1, vans):
        offset = 110 if v >= 0 else -190
        txt = f'{v:+,} k USD'.replace(',', '.')
        ax1.text(rect.get_x() + rect.get_width() / 2, v + offset, txt,
                 ha='center', va='center', fontsize=9.5, fontweight='bold',
                 color='#1B5E20' if v > 0 else '#8B0000' if v > -2000 else '#445566')

    ax1.set_ylim(-3500, 2350)
    ax1.set_ylabel('VAN (miles de USD) @ Ke = 14,9%', fontsize=10, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.35, zorder=0)
    ax1.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax1.spines[sp].set_visible(False)
    ax1.set_title('VAN por escenario (Horizonte 10 años)', fontsize=12, fontweight='bold', pad=10, color='#1A2536')

    # Panel 2: TIR
    tir_vals = [0, 21.9, 49.4, 0]
    tir_labels = ['N/R\n(flujo < 0)', '21,9%', '49,4%', 'N/R\n(flujo < 0)']
    b2 = ax2.bar(nombres, tir_vals, width=0.58, color=colores, alpha=0.90, zorder=3)
    ax2.axhline(14.9, color=ROJO, lw=1.8, ls='--', zorder=4)
    ax2.text(3.38, 16.5, 'Costo de capital\nKe = 14,9%', color=ROJO, fontsize=8.8, fontweight='bold',
             ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=ROJO, lw=0.8, alpha=0.95), zorder=5)

    for rect, v, lab in zip(b2, tir_vals, tir_labels):
        x_c = rect.get_x() + rect.get_width() / 2
        if v > 0:
            ax2.text(x_c, v + 2.2, lab, ha='center', va='center', fontsize=10, fontweight='bold', color='#1A2536')
        else:
            ax2.text(x_c, 3.8, lab, ha='center', va='center', fontsize=8.5, style='italic', color='#666666')

    ax2.set_ylim(0, 57)
    ax2.set_ylabel('TIR anual (%)', fontsize=10, fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.35, zorder=0)
    ax2.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax2.spines[sp].set_visible(False)
    ax2.set_title('TIR por escenario vs. Tasa de descuento (Ke)', fontsize=12, fontweight='bold', pad=10, color='#1A2536')

    fig.suptitle('Sensibilización por Escenarios — PedioLink (VAN esperado ponderado: +204 k USD)',
                 fontsize=13.5, fontweight='bold', y=1.02, color='#1A2536')
    fig.tight_layout()
    save(fig, 'fig5_escenarios.png')


# ---------------------------------------------------------- 6. BPMN (cap. 7)
def bpmn():
    fig, ax = plt.subplots(figsize=(14.2, 4.3))
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0.2, 4.1)
    ax.axis('off')

    # Pista 1: Hospital / clínica
    ax.add_patch(FancyBboxPatch((0.15, 1.15), 3.75, 2.35, boxstyle='round,pad=0.0,rounding_size=0.08',
                                fc='#F4F6F8', ec=GRIS, lw=1.5, zorder=1))
    ax.text(0.35, 3.25, 'Hospital / Clínica (Cliente)', ha='left', va='center',
            fontsize=9.8, fontweight='bold', color='#334455', zorder=2)

    # Pista 2: Plataforma PedioLink
    ax.add_patch(FancyBboxPatch((4.10, 1.15), 10.25, 2.35, boxstyle='round,pad=0.0,rounding_size=0.08',
                                fc='#EDF4FC', ec=AZUL, lw=1.5, zorder=1))
    ax.text(4.30, 3.25, 'Plataforma PedioLink (SaaS Cloud AWS)', ha='left', va='center',
            fontsize=9.8, fontweight='bold', color=AZUL, zorder=2)

    y_mid = 2.25

    # Evento de inicio
    start_x = 0.75
    ax.add_patch(Circle((start_x, y_mid), 0.25, fc=VERDE, ec='#2E6B34', lw=2.0, zorder=3))
    ax.text(start_x, 1.58, 'ECG realizado\nal paciente', ha='center', va='center',
            fontsize=8.2, fontweight='bold', color='#2E6B34', zorder=3)

    # Tareas: (x_centro, ancho, etiqueta, en_plataforma)
    tareas = [
        (2.55, 2.10, 'Exportar archivo digital\nWFDB / DICOM-ECG\n(HTTPS TLS 1.3)', False),
        (5.30, 1.95, '1. Recepción y\nvalidación de\nintegridad del archivo', True),
        (7.60, 1.95, '2. Filtrado DSP,\nextracción de ondas y\nclasificación ML', True),
        (9.90, 1.95, '3. Generación de\nreporte + nivel de\ncerteza en dashboard', True),
        (12.20, 1.95, '4. Notificación y\nalerta temprana si\narritmia es crítica', True),
    ]

    prev_right = start_x + 0.25
    for x, w, lab, in_pf in tareas:
        color = AZUL if in_pf else '#556677'
        box = FancyBboxPatch(
            (x - w / 2, y_mid - 0.52), w, 1.04,
            boxstyle='round,pad=0.0,rounding_size=0.08',
            fc='white', ec=color, lw=2.0, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y_mid, lab, ha='center', va='center', fontsize=8.4, color='#1A2536', linespacing=1.25, zorder=4)

        # Flecha desde el elemento anterior
        ax.add_patch(FancyArrowPatch(
            (prev_right + 0.04, y_mid), (x - w / 2 - 0.04, y_mid),
            arrowstyle='-|>', mutation_scale=14, color='#444444', lw=1.6, zorder=4
        ))
        prev_right = x + w / 2

    # Evento de término
    end_x = 13.80
    ax.add_patch(Circle((end_x, y_mid), 0.25, fc=ROJO, ec='#800000', lw=2.0, zorder=3))
    ax.add_patch(Circle((end_x, y_mid), 0.15, fc='white', ec=ROJO, lw=1.2, zorder=4))
    ax.text(end_x, 1.58, 'Reporte disponible\n(Dashboard / HIS)', ha='center', va='center',
            fontsize=8.0, fontweight='bold', color='#800000', zorder=3)

    ax.add_patch(FancyArrowPatch(
        (prev_right + 0.04, y_mid), (end_x - 0.25 - 0.04, y_mid),
        arrowstyle='-|>', mutation_scale=14, color='#444444', lw=1.6, zorder=4
    ))

    ax.text(
        7.25, 0.62,
        'Nota clínica y técnica: La revisión y decisión diagnóstica final corresponden siempre al médico tratante (el reporte de PedioLink es de apoyo,\n'
        'con indicadores de certeza y limitaciones explícitas). Interoperabilidad mediante estándares HL7 v2 / FHIR R4 con el registro clínico electrónico.',
        ha='center', va='center', fontsize=8.6, style='italic', color='#334455', linespacing=1.3
    )
    ax.set_title('Proceso de Negocio (BPMN Simplificado) — Flujo de Procesamiento PedioLink',
                 fontsize=13.5, fontweight='bold', pad=8, color='#1A2536')
    save(fig, 'fig_bpmn.png')


# ---------------------------------------------------------- 7. LAYOUT (cap. 7)
def layout():
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 6.4)
    ax.axis('off')

    # Contorno general de la oficina
    ax.add_patch(Rectangle((0.4, 0.65), 11.7, 4.85, fc='#F8FAFC', ec='#223344', lw=2.5, zorder=1))
    ax.text(6.25, 5.75, 'Planta referencial oficina 100 m² — Providencia (desde Año 3; Años 1–2 en coworking)',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334455')

    # Pasillo central
    ax.text(6.25, 2.92, 'Pasillo de circulación interna', ha='center', va='center',
            fontsize=8.2, style='italic', color='#778899')

    # Zonas: (titulo, subtitulo, x, y, w, h, color, bg)
    zonas = [
        ('Open Space Técnico (36 m²)', '6 puestos de trabajo\n(Devs ML, Cloud/DevOps, CTO)', 0.65, 3.25, 4.80, 2.00, AZUL, '#EFF6FC'),
        ('Sala de Reuniones (20 m²)', 'Demostraciones comerciales B2B\ny sesiones con hospitales', 5.65, 3.25, 3.00, 2.00, CELESTE, '#F2F8FD'),
        ('Sala de Capacitación (18 m²)', 'Simulación de flujo clínico\ny onboarding de usuarios', 8.85, 3.25, 3.00, 2.00, VERDE, '#F2FAF0'),
        ('Dirección y Comercial (10 m²)', 'CEO y Director Comercial\n(gestión y licitaciones)', 0.65, 0.90, 3.10, 1.70, CELESTE, '#F2F8FD'),
        ('Coordinación Clínica (10 m²)', 'Director Médico MT\n(convenios y pilotos clínicos)', 3.95, 0.90, 3.10, 1.70, VERDE, '#F2FAF0'),
        ('Kitchenette (3 m²)', 'Área de descanso\ny comedor', 7.25, 0.90, 2.20, 1.70, GRIS, '#F5F7F9'),
        ('Recepción (3 m²)', 'Control de acceso\ny espera', 9.65, 0.90, 2.20, 1.70, GRIS, '#F5F7F9'),
    ]

    for titulo, sub, x, y, w, h, c, bg in zonas:
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.0,rounding_size=0.06',
            fc=bg, ec=c, lw=2.0, zorder=2
        ))
        ax.text(x + w / 2, y + h / 2 + 0.26, titulo, ha='center', va='center',
                fontsize=9.2, fontweight='bold', color='#1A2536', zorder=3)
        ax.text(x + w / 2, y + h / 2 - 0.22, sub, ha='center', va='center',
                fontsize=8.2, color='#445566', linespacing=1.25, zorder=3)

    # Puerta de acceso principal
    ax.plot([10.4, 11.1], [0.65, 0.65], color='white', lw=4.0, zorder=2)
    ax.annotate('Acceso principal', xy=(10.75, 0.68), xytext=(10.75, 0.15),
                ha='center', va='center', fontsize=8.8, fontweight='bold', color='#223344',
                arrowprops=dict(arrowstyle='-|>', color='#223344', lw=1.6))

    ax.set_title('Layout de la Operación — PedioLink (Modelo 100% SaaS: procesamiento en AWS, sin bodega ni servidores físicos)',
                 fontsize=12.5, fontweight='bold', pad=14, color='#1A2536')
    save(fig, 'fig_layout.png')


# ---------------------------------------------------------- 8. TAM-SAM-SOM (cap. 4)
def mercado():
    fig, ax = plt.subplots(figsize=(12.2, 5.2))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(-0.3, 4.4)
    ax.axis('off')

    niveles = [
        ('TAM — Chile (con pediatría y ECG digital)', 115, AZUL,
         '≈ 30% de 382 establecimientos públicos y privados (BCN, 2025) · USD 3,38 M/año'),
        ('SAM — Región Metropolitana calificada', 38, CELESTE,
         '≈ 30% de 128 establecimientos RM (45 hospitales + 83 clínicas) · USD 1,12 M/año'),
        ('SOM Año 5 — Clientes activos (Caso Viable)', 20, VERDE,
         '≈ 52,6% del SAM RM calificado · Expansión a regiones desde Año 6'),
        ('SOM Año 10 — Madurez nacional', 37, '#2E8B57',
         '≈ 32,2% del TAM nacional calificado · Ingresos régimen USD 1,35 M/año'),
    ]

    maxv = 115
    bar_x0 = 5.45
    max_bar_w = 6.2

    for i, (nom, v, c, nota) in enumerate(niveles):
        y = 3.35 - i * 0.98
        w = max(max_bar_w * v / maxv, 0.45)

        # Textos a la izquierda, perfectamente alineados con la barra
        ax.text(bar_x0 - 0.20, y + 0.44, nom, ha='right', va='center',
                fontsize=9.6, fontweight='bold', color='#1A2536')
        ax.text(bar_x0 - 0.20, y + 0.16, nota, ha='right', va='center',
                fontsize=8.0, style='italic', color='#556677')

        # Barra horizontal
        ax.add_patch(FancyBboxPatch(
            (bar_x0, y), w, 0.62,
            boxstyle='round,pad=0.0,rounding_size=0.08',
            fc=c, ec='none', alpha=0.90, zorder=3
        ))

        # Etiqueta de valor a la derecha de la barra
        ax.text(bar_x0 + w + 0.18, y + 0.31, f'{v} instituciones',
                ha='left', va='center', fontsize=10.2, fontweight='bold', color=c)

    ax.set_title('Dimensionamiento de Mercado (TAM – SAM – SOM) — PedioLink',
                 fontsize=13.5, fontweight='bold', pad=10, color='#1A2536')
    save(fig, 'fig_tam_sam_som.png')


# ---------------------------------------------------------- 9. PARTICIPACIÓN (cap. 5)
def participacion():
    anios = list(range(1, 11))
    inst = [2, 5, 9, 14, 20, 25, 30, 34, 36, 37]
    pct_sam = [v / 38 * 100 for v in inst[:5]]
    pct_tam = [v / 115 * 100 for v in inst]

    fig, ax = plt.subplots(figsize=(11.8, 5.4))
    colores = [CELESTE if a <= 5 else VERDE for a in anios]
    ax.bar(anios, inst, width=0.62, color=colores, alpha=0.90, zorder=3)

    for i, (a, v) in enumerate(zip(anios, inst)):
        pct_txt = f'({pct_sam[i]:.0f}% SAM)' if a <= 5 else f'({pct_tam[i]:.0f}% TAM)'
        ax.text(a, v + 2.3, f'{v}', ha='center', va='center', fontsize=10, fontweight='bold', color='#1A2536')
        ax.text(a, v + 0.85, pct_txt, ha='center', va='center', fontsize=7.6, color='#556677')

    ax.axvline(5.5, color=GRIS, ls='--', lw=1.6, zorder=2)
    ax.text(5.32, 29.0, '← Etapa 1: Foco RM\n(Años 1–5)',
            fontsize=8.6, fontweight='bold', color='#2B5B84', ha='right', va='center',
            bbox=dict(boxstyle='round,pad=0.28', fc='#F2F8FD', ec=CELESTE, lw=1.0))
    ax.text(5.68, 42.2, 'Etapa 2: Expansión Nacional (Años 6–10) →',
            fontsize=8.6, fontweight='bold', color='#2E6B34', ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.28', fc='#F2FAF0', ec=VERDE, lw=1.0))

    ax.set_xticks(anios)
    ax.set_xticklabels([f'Año {a}' for a in anios], fontsize=9.5, fontweight='bold')
    ax.set_xlabel('Año de operación', fontsize=10, fontweight='bold', labelpad=6)
    ax.set_ylabel('Instituciones activas al cierre del año', fontsize=10, fontweight='bold')
    ax.set_ylim(0, 46)
    ax.grid(axis='y', linestyle='--', alpha=0.35, zorder=0)
    ax.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)

    ax.legend(
        handles=[
            Patch(fc=CELESTE, label='Años 1–5: Foco RM (SAM = 38 inst. → 52,6% en Año 5)'),
            Patch(fc=VERDE, label='Años 6–10: RM + Regiones (TAM = 115 inst. → 32,2% en Año 10)'),
        ],
        fontsize=8.8, frameon=True, facecolor='white', edgecolor='#DDD', loc='upper left'
    )
    ax.set_title('Participación de Mercado Proyectada — Instituciones Activas por Año (Caso Viable)',
                 fontsize=13.5, fontweight='bold', pad=12, color='#1A2536')
    save(fig, 'fig_participacion.png')


# ---------------------------------------------------------- 10. LOGO (cap. 6)
def logo():
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    ax.set_xlim(0, 8.0)
    ax.set_ylim(0, 3.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Dibujar nube vectorial limpia en la derecha (alrededor de x=5.8, y=2.35)
    cloud_color = AZUL
    c_parts = [
        Circle((5.15, 2.15), 0.42, fc=cloud_color, ec='none', zorder=2),
        Circle((5.65, 2.52), 0.56, fc=cloud_color, ec='none', zorder=2),
        Circle((6.30, 2.60), 0.62, fc=cloud_color, ec='none', zorder=2),
        Circle((6.90, 2.22), 0.45, fc=cloud_color, ec='none', zorder=2),
    ]
    for cp in c_parts:
        ax.add_patch(cp)
    ax.add_patch(FancyBboxPatch(
        (4.75, 1.73), 2.58, 0.55,
        boxstyle='round,pad=0.0,rounding_size=0.26',
        fc=cloud_color, ec='none', zorder=2
    ))

    # Pequeño corazón / nodo blanco dentro de la nube
    ax.plot([5.85, 6.05, 6.20, 6.35, 6.50, 6.75],
            [2.22, 2.22, 2.55, 1.98, 2.22, 2.22],
            color='white', lw=2.4, solid_capstyle='round', solid_joinstyle='round', zorder=4)

    # Trazo de pulso ECG (rojo) que conecta hacia la nube
    xs = [0.55, 1.55, 1.80, 2.00, 2.22, 2.50, 2.75, 3.05, 3.30, 3.60, 3.85, 4.55]
    ys = [1.95, 1.95, 2.20, 1.95, 1.55, 3.10, 1.15, 1.95, 1.95, 2.30, 1.95, 2.22]
    ax.plot(xs, ys, color=ROJO, lw=3.8, solid_capstyle='round', solid_joinstyle='round', zorder=3)
    ax.add_patch(FancyArrowPatch(
        (4.35, 2.15), (4.95, 2.35),
        arrowstyle='-|>', mutation_scale=20, color=ROJO, lw=3.8, zorder=4
    ))

    # Wordmark "PedioLink" y bajada
    ax.text(0.55, 0.72, 'Pedio', fontsize=31, fontweight='bold', color=AZUL, va='center', ha='left')
    ax.text(2.38, 0.72, 'Link', fontsize=31, fontweight='bold', color=CELESTE, va='center', ha='left')
    ax.text(0.57, 0.26, 'Soporte diagnóstico cloud de arritmias pediátricas',
            fontsize=10.5, color='#445566', style='italic', va='center', ha='left')

    save(fig, 'fig_logo.png')


if __name__ == '__main__':
    canvas()
    gantt()
    organigrama()
    flujo()
    escenarios()
    bpmn()
    layout()
    mercado()
    participacion()
    logo()
    print("Listo: 10 gráficos en", OUT)
