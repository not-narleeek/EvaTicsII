#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del modelo económico PedioLink — caso VIABLE (opción b).

Hipótesis (todas trazables al informe o a la guía):
- Horizonte 10 años (la guía permite "otro horizonte de interés").
- Precio 2.450 = mix ponderado del rango declarado 1.500-3.000 (30/50/20).
- 300 estudios/mes por institución (cupo 200 + adicionales a 8 USD).
- White-label/API desde año 3 = 10% de la suscripción (cap. 6 del informe).
- Expansión nacional desde año 6 (universo ~115 inst.; captura final 32%).
- Cloud 0,80 USD/estudio (valor optimista del informe, justificado por volumen).
- Estructura de costos AJUSTADA: 7 personas año 1 (socios con sueldo parcial),
  ~14 al año 10 (guía: "tratar de minimizar sus costos fijos").
- Financiamiento 785k: aportes 235k + CORFO 150k + Banca Desarrollo 400k
  (12% anual, 10 años, 3 de gracia). Sin deuda comercial al 12% corto plazo.
- Ke = 14,9% (CAPM con los insumos del informe, corregido).

Uso: python3 excel/generar_excel.py
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# ---------------------------------------------------------------- parámetros
H = 10                     # años de horizonte
COLS = 'CDEFGHIJKL'        # años 1..10 en la hoja Flujo
TC_CLP = 950
SAM_UNIV_RM, SAM_PCT = 128, 0.30          # SAM RM = 38
UNIV_NAC = 382                            # expansión nacional (BCN)
PRECIO, IMPL = 2450.0, 8000.0
ESTUDIOS, CUPO, EXTRA = 300, 200, 8.0
CLOUD_VAR, WL_PCT = 0.80, 0.10
M1_INST, F1_COSTOS = 3.5, 0.55            # año 1: meses promedio por institución, fracción de costos
AMORT_INTANG, AMORT_DIFERIDO = 31000.0, 16000.0   # 5 años (solo años 1-5)
WC = 500000.0
RECURRENTE = 70000.0
TASA_IMP = 0.27
APORTES, PRESTAMO, CORFO = 235000.0, 400000.0, 150000.0
TASA_PREST, PLAZO_MESES, GRACIA_MESES = 0.12, 120, 36

def serie(f0, g):  # crecimiento compuesto desde factor 1
    return [f0 * g ** t for t in range(H)]

COSTOS_ADOPTADA = {   # (base mensual, factores por año; año 1 ya incluye 0,55)
    'Remuneraciones':               (12500, [0.55, 1.28, 1.56, 1.716, 1.8876, 2.0764, 2.2840, 2.5124, 2.7636, 3.0400]),
    'Cloud base (infra)':           (2500,  serie(0.55, 1.05)),
    'Arriendo':                     (900,   [0.55, 1.00, 2.00, 2.04, 2.0816] + [2.0816 * 1.02 ** t for t in range(1, 6)]),
    'Marketing':                    (3000,  [0.55, 1.20, 1.40, 1.60, 1.80, 1.89, 1.9845, 2.0837, 2.1879, 2.2973]),
    'Servicios (legal, auditoria)': (1000,  serie(0.55, 1.05)),
    'Software y licencias dev':     (800,   serie(0.55, 1.05)),
    'Otros (seguros, internet)':    (900,   serie(0.55, 1.03)),
}
COSTOS_BASE = {       # estructura original cap. 12 (11 personas) — diagnóstico descartado
    'Remuneraciones':               (28000, [1.1 ** t for t in range(H)]),
    'Cloud base (infra)':           (2500,  [1.05 ** t for t in range(H)]),
    'Arriendo':                     (2500,  [1.02 ** t for t in range(H)]),
    'Marketing':                    (3000,  [1, 1.2, 1.4, 1.6, 1.8, 1.89, 1.9845, 2.0837, 2.1879, 2.2973]),
    'Servicios (legal, auditoria)': (1500,  [1.05 ** t for t in range(H)]),
    'Software y licencias dev':     (800,   [1.05 ** t for t in range(H)]),
    'Otros (seguros, internet)':    (1200,  [1.03 ** t for t in range(H)]),
}
FILA_FIJOS = list(COSTOS_ADOPTADA.keys())

ESCENARIOS = {
    'Pesimista':   dict(inst=[1, 2, 4, 6, 9, 12, 16, 19, 21, 22], precio=1500.0, impl=6000.0,
                        cloud_var=1.50, wl=0.05, estudios=250, inv=320000.0, rec=80000.0,
                        ke=0.149, estructura='ajustada', m1=2.5, f1=0.45),
    'Viable':      dict(inst=[2, 5, 9, 14, 20, 25, 30, 34, 36, 37], precio=2450.0, impl=8000.0,
                        cloud_var=0.80, wl=0.10, estudios=300, inv=285000.0, rec=70000.0,
                        ke=0.149, estructura='ajustada', m1=3.5, f1=0.55),
    'Optimista':   dict(inst=[3, 7, 12, 18, 25, 32, 38, 42, 44, 45], precio=3000.0, impl=8000.0,
                        cloud_var=0.80, wl=0.15, estudios=350, inv=260000.0, rec=70000.0,
                        ke=0.149, estructura='ajustada', m1=4.0, f1=0.60),
    'Diagnostico': dict(inst=[2, 4, 6, 8, 10, 10, 10, 10, 10, 10], precio=2200.0, impl=8000.0,
                        cloud_var=1.50, wl=0.00, estudios=230, inv=285000.0, rec=70000.0,
                        ke=0.149, estructura='base', m1=3.5, f1=1.00),
}
PROB = (0.25, 0.50, 0.25)   # pesimista, viable, optimista

# ---------------------------------------------------------------- motor
def meses_inst(inst, m1):
    return [inst[0] * m1] + [(inst[i - 1] + inst[i]) / 2 * 12 for i in range(1, H)]

def costos_fijos(struct):
    tabla = COSTOS_ADOPTADA if struct == 'ajustada' else COSTOS_BASE
    return {n: [tabla[n][0] * f for f in tabla[n][1]] for n in FILA_FIJOS}

def cronograma_prestamo():
    i = TASA_PREST / 12
    n_post = PLAZO_MESES - GRACIA_MESES
    cuota = PRESTAMO * i * (1 + i) ** n_post / ((1 + i) ** n_post - 1)
    saldo, filas = PRESTAMO, []
    for y in range(1, H + 1):
        inte = prin = 0.0
        for m in range(12):
            mes = (y - 1) * 12 + m
            if mes < GRACIA_MESES:
                inte += saldo * i
            else:
                ip = saldo * i
                pay = min(cuota, saldo + ip)
                inte += ip
                prin += pay - ip
                saldo -= pay - ip
        filas.append(dict(interes=inte, principal=prin, saldo=saldo, cuota=cuota * 12))
    return filas

def impuestos_con_arrastre(bases):
    out, acum = [], 0.0
    for b in bases:
        out.append(max(0.0, b + min(0.0, acum)) * TASA_IMP)
        acum += b
    return out

def flujo_proyecto(p, struct):
    inst, mi = p['inst'], meses_inst(p['inst'], p['m1'])
    fijos = costos_fijos(struct)
    fx = [sum(fijos[n][t] for n in FILA_FIJOS) for t in range(H)]
    amort = [AMORT_INTANG + AMORT_DIFERIDO if t < 5 else 0.0 for t in range(H)]
    ing, ebitda, var, bases, wls = [], [], [], [], []
    for t in range(H):
        nuevas = inst[t] - (inst[t - 1] if t else 0)
        susc = mi[t] * p['precio']
        extra = mi[t] * max(0, p['estudios'] - CUPO) * EXTRA
        wl = susc * p['wl'] if t >= 2 else 0.0
        wls.append(wl)
        ing.append(susc + extra + wl + nuevas * p['impl'])
        var.append(mi[t] * p['estudios'] * p['cloud_var'])
        ebitda.append(ing[t] - var[t] - fx[t] * 12)
        bases.append(ebitda[t] - amort[t])
    taxes = impuestos_con_arrastre(bases)
    fl = [-p['inv']] + [ebitda[t] - taxes[t] - p['rec'] for t in range(H)]
    fl[H] += WC
    acum, s = [], 0.0
    for f in fl:
        s += f
        acum.append(s)
    return dict(ing=ing, ebitda=ebitda, var=var, wls=wls, fijos_m=fx, meses=mi,
                taxes=taxes, flujo=fl, acumulado=acum, p=p, struct=struct)

def van(fl, r):
    return sum(f / (1 + r) ** t for t, f in enumerate(fl))

def tir(fl):
    lo, hi = -0.99, 10.0
    f = lambda r: van(fl, r)
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def pri_simple(fl):
    s = fl[0]
    for t in range(1, len(fl)):
        prev, s2 = s, s + fl[t]
        if s2 >= 0 > prev:
            return t - 1 + (-prev / fl[t])
        s = s2
    return None

def pri_descontado(fl, r):
    return pri_simple([f / (1 + r) ** t for t, f in enumerate(fl)])

def eerr(p, struct, anios=3):
    fl = flujo_proyecto(p, struct)
    cr = cronograma_prestamo()
    filas, acum = [], 0.0
    for t in range(anios):
        ebit = fl['ebitda'][t] - AMORT_INTANG - AMORT_DIFERIDO
        bt = ebit - cr[t]['interes']
        bt_fisc = bt + min(0.0, acum)
        imp = max(0.0, bt_fisc) * TASA_IMP
        acum += bt
        filas.append(dict(ingresos=fl['ing'][t], ebitda=fl['ebitda'][t],
                          amort=AMORT_INTANG + AMORT_DIFERIDO, ebit=ebit,
                          interes=cr[t]['interes'], bt=bt, imp=imp, neto=bt - imp))
    return filas

def balance(p, struct, anios=3):
    cr = cronograma_prestamo()
    er = eerr(p, struct, anios)
    caja = APORTES + PRESTAMO + CORFO - (AMORT_INTANG * 5 + AMORT_DIFERIDO * 5 + WC)
    pat = APORTES + CORFO
    filas = []
    for t in range(anios):
        caja += er[t]['ebitda'] - er[t]['imp'] - cr[t]['interes'] - cr[t]['principal']
        pat += er[t]['neto']
        activo = caja + WC + (80000 - AMORT_DIFERIDO * (t + 1)) + (155000 - AMORT_INTANG * (t + 1))
        filas.append(dict(caja=caja, wc=WC, diferido=80000 - AMORT_DIFERIDO * (t + 1),
                          intang=155000 - AMORT_INTANG * (t + 1), activo=activo,
                          deuda=cr[t]['saldo'], patrimonio=pat,
                          check=activo - (cr[t]['saldo'] + pat)))
    return filas

def punto_equilibrio(struct, precio, estudios=ESTUDIOS):
    fijos = costos_fijos(struct)
    fx5 = sum(fijos[n][4] for n in FILA_FIJOS)   # año 5, escala madura
    contrib = precio + max(0, estudios - CUPO) * EXTRA - estudios * 0.80
    return fx5 / contrib

# ---------------------------------------------------------------- estilos
B = Font(bold=True); IT = Font(italic=True, size=9)
FILL_H = PatternFill('solid', fgColor='1F4E79'); FILL_SEC = PatternFill('solid', fgColor='D9E2F3')
FILL_IN = PatternFill('solid', fgColor='FFF2CC')
NUM, PCT = '#,##0', '0.0%'

wb = Workbook(); wb.remove(wb.active)
wb.calculation.fullCalcOnLoad = True

def hoja(nombre, color):
    ws = wb.create_sheet(nombre)
    ws.sheet_properties.tabColor = color
    return ws

ws_sup = hoja('Supuestos', 'FFC000')
ws_flu = hoja('Flujo de Caja', '2E75B6')
ws_er = hoja('Estado Resultados', '70AD47')
ws_bal = hoja('Balance', '7030A0')
ws_ev = hoja('Evaluacion', 'C00000')
ws_esc = hoja('Escenarios', 'ED7D31')

# === Supuestos ============================================================
ws = ws_sup
ws['A1'] = 'SUPUESTOS — caso VIABLE (opción b) — única fuente de verdad del modelo'
ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = 'Celdas amarillas = editables (el modelo se recalcula). Montos en USD salvo indicación.'
S, r = {}, 4

def sec(titulo):
    global r
    c = ws.cell(row=r, column=1, value=titulo); c.font = B; c.fill = FILL_SEC
    r += 1

def put(label, value, fmt=NUM, key=None, nota=''):
    global r
    ws.cell(row=r, column=1, value=label)
    c = ws.cell(row=r, column=2, value=value)
    c.number_format = fmt
    if key:
        c.fill = FILL_IN; S[key] = r
    if nota:
        ws.cell(row=r, column=3, value=nota).font = IT
    r += 1

sec('Mercado')
put('Universo RM (hospitales + clínicas, BCN 2025)', SAM_UNIV_RM, key='univ', nota='45 hospitales + 83 clínicas (BCN, 2025, sección 4.4)')
put('% RM que cumple requisitos (pediatría + ECG digital)', SAM_PCT, PCT, key='sam_pct', nota='SUPUESTO a validar con catastro')
ws.cell(row=r, column=1, value='SAM calificado RM (instituciones)')
ws.cell(row=r, column=2, value=f'=ROUND(B{S["univ"]}*B{S["sam_pct"]},0)').number_format = NUM
S['sam'] = r; r += 1
put('Universo nacional (BCN 2025, expansión año 6+)', UNIV_NAC, key='univ_nac', nota='227 hospitales + 155 clínicas')
put('% nacional que cumple requisitos', SAM_PCT, PCT, key='sam_pct_nac', nota='mismo criterio declarado')

sec('Comercial (caso Viable)')
put('Precio suscripción (USD/mes) = mix 30/50/20 de 3.000/2.500/1.500', PRECIO, key='precio')
put('Cargo implementación (una vez)', IMPL, key='impl')
put('Estudios promedio por institución (mes)', ESTUDIOS, key='estudios', nota='hospital pediátrico referencial; SUPUESTO declarado')
put('Cupo base incluido (estudios/mes)', CUPO, key='cupo')
put('Precio estudio adicional (USD)', EXTRA, key='extra')
put('Costo cloud variable (USD/estudio)', CLOUD_VAR, key='cloud_var', nota='volumen: committed-use AWS (optimista del informe)')
put('White-label/API (% de la suscripción, desde año 3)', WL_PCT, PCT, key='wl', nota='línea declarada en cap. 6 del informe')
put('Meses promedio de actividad por institución, año 1', M1_INST, '0.0', key='m1', nota='lanzamiento mes 8-9 (carta Gantt)')
put('Fracción de costos fijos año 1 (operación parcial)', F1_COSTOS, PCT, key='f1', nota='costos completos solo desde el lanzamiento')

sec('Instituciones activas al cierre de año (escenarios)')
ws.cell(row=r, column=1, value='Escenario').font = B
for j in range(H):
    ws.cell(row=r, column=2 + j, value=f'Año {j + 1}').font = B
r += 1
for nom in ('Pesimista', 'Viable', 'Optimista', 'Diagnostico'):
    ws.cell(row=r, column=1, value=nom)
    for j, v in enumerate(ESCENARIOS[nom]['inst']):
        ws.cell(row=r, column=2 + j, value=v).fill = FILL_IN
    S[f'inst_{nom}'] = r
    r += 1
ws.cell(row=r, column=1, value='Captura año 10 Viable = 37 ≈ 32% del universo nacional calificado (~115); RM saturándose desde año 6.').font = IT
r += 2

sec('Costos fijos mensuales — ESTRUCTURA AJUSTADA adoptada (7 personas año 1; guía: minimizar fijos)')
ws.cell(row=r, column=1, value='Ítem').font = B
ws.cell(row=r, column=2, value='Base USD/mes').font = B
for j in range(H):
    ws.cell(row=r, column=3 + j, value=f'F. año {j + 1}').font = B
r += 1
FAC_ROWS = {}
for n in FILA_FIJOS:
    ws.cell(row=r, column=1, value=n)
    c = ws.cell(row=r, column=2, value=COSTOS_ADOPTADA[n][0]); c.fill = FILL_IN; c.number_format = NUM
    for j, f in enumerate(COSTOS_ADOPTADA[n][1]):
        c = ws.cell(row=r, column=3 + j, value=f); c.fill = FILL_IN; c.number_format = '0.000'
    FAC_ROWS[n] = r
    r += 1
S['fac_first'], S['fac_last'] = FAC_ROWS[FILA_FIJOS[0]], FAC_ROWS[FILA_FIJOS[-1]]
ws.cell(row=r, column=1, value='(Estructura BASE de 11 personas del cap. 12: diagnósticos en docs/excel-notas.md — VAN −1,9M, descartada)').font = IT
r += 2

sec('Inversión y financiamiento')
put('Inversión inicial (cap. 10)', 285000.0, key='inv')
put('Inversión recurrente anual', RECURRENTE, key='rec')
put('Capital de trabajo + reserva ramp-up (se recupera año 10)', WC, key='wc')
put('Aporte socios', APORTES, key='aportes')
put('CORFO (no reembolsable, a patrimonio)', CORFO, key='corfo')
put('Préstamo Banca Desarrollo (10 años, 3 de gracia)', PRESTAMO, key='prestamo', nota='banco comercial descartado: destruye valor en ramp-up (ex cap. 11)')
put('Tasa anual préstamo', TASA_PREST, PCT, key='tasa_p')
put('Gracia de capital (años)', 3, '0', key='gracia')

sec('Fiscal y CAPM')
put('Tasa impuesto (primera categoría)', TASA_IMP, PCT, key='tasa_imp')
put('Rf libre de riesgo Chile 10a', 0.05, PCT, key='rf')
put('Beta (Damodaran — citar fila y fecha exacta)', 1.15, '0.00', key='beta')
put('Prima de riesgo de mercado (Rm−Rf)', 0.06, PCT, key='mrp')
put('Prima de riesgo país (CDS Chile)', 0.03, PCT, key='prp')
ws.cell(row=r, column=1, value='Ke = Rf + β×(Rm−Rf) + PRP')
ws.cell(row=r, column=2, value=f'=B{S["rf"]}+B{S["beta"]}*B{S["mrp"]}+B{S["prp"]}').number_format = PCT
S['ke'] = r
r += 1
put('Tipo de cambio referencial (CLP/USD) — actualizar', TC_CLP, key='tc')

r += 1
ws.cell(row=r, column=1, value=('Notas: (1) Amortización 5 años: intangibles 155k (desarrollo 120k + certificación 35k) y gastos '
        'diferidos 80k (marketing 15k + setup cloud 15k + contratación 50k). (2) CORFO como donación a patrimonio. '
        '(3) Arrastre infinito de pérdidas tributarias. (4) El Balance muestra el déficit de caja del ramp-up (años 1-3): '
        'se cubre con línea de capital de trabajo comprometida, a declarar en el cap. 11 del informe.')).font = IT
ws.column_dimensions['A'].width = 52
ws.column_dimensions['B'].width = 14
for col in 'CDEFGHIJKL':
    ws.column_dimensions[col].width = 9
ws.column_dimensions['M'].width = 40
ws.freeze_panes = 'A4'

# === Flujo de Caja (fórmulas vivas, 10 años, caso Viable) ==================
ws = ws_flu
ws['A1'] = 'FLUJO DE CAJA PROYECTADO — caso Viable, estructura ajustada, horizonte 10 años'
ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = 'USD. Fórmulas vivas: editar Supuestos recalcula todo. La guía permite "otro horizonte que considere de interés".'
for j, lab in enumerate(['Concepto', 'Año 0'] + [f'Año {t + 1}' for t in range(H)]):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H

R, _r = {}, 4
def fr(key, label, vals, fmt=NUM, bold=False):
    global _r
    _r += 1
    ws.cell(row=_r, column=1, value=label).font = B if bold else Font()
    for j, v in enumerate(vals):
        c = ws.cell(row=_r, column=2 + j, value=v)
        if fmt and (not isinstance(v, str) or str(v).startswith('=')):
            c.number_format = fmt
        if bold: c.font = B
    R[key] = _r

iv = ESCENARIOS['Viable']
fr('inst', 'Instituciones activas (cierre)',
   ['—'] + [f'=Supuestos!{chr(66 + t)}{S["inst_Viable"]}' for t in range(H)], '0')
fr('meses', 'Meses-institución',
   ['—', f'=C{R["inst"]}*Supuestos!$B${S["m1"]}'] +
   [f'=({chr(65 + t)}{R["inst"]}+{chr(66 + t)}{R["inst"]})*12/2' for t in range(2, H + 1)])
fr('susc', 'Ingreso suscripción', ['—'] + [f'={c}{R["meses"]}*Supuestos!$B${S["precio"]}' for c in COLS])
fr('extra', 'Ingreso estudios adicionales',
   ['—'] + [f'={c}{R["meses"]}*MAX(0,Supuestos!$B${S["estudios"]}-Supuestos!$B${S["cupo"]})*Supuestos!$B${S["extra"]}' for c in COLS])
fr('wl', 'Ingreso white-label/API (desde año 3)',
   ['—', 0, 0] + [f'={c}{R["susc"]}*Supuestos!$B${S["wl"]}' for c in COLS[2:]])
fr('impl', 'Ingreso implementación',
   ['—', f'=C{R["inst"]}*Supuestos!$B${S["impl"]}'] +
   [f'=({chr(66 + t)}{R["inst"]}-{chr(65 + t)}{R["inst"]})*Supuestos!$B${S["impl"]}' for t in range(2, H + 1)])
fr('ing', 'INGRESOS TOTALES', [0] + [f'=SUM({c}{R["susc"]}:{c}{R["impl"]})' for c in COLS], NUM, True)
fr('var', 'Costo variable cloud',
   ['—'] + [f'={c}{R["meses"]}*Supuestos!$B${S["estudios"]}*Supuestos!$B${S["cloud_var"]}' for c in COLS])
for k, n in enumerate(FILA_FIJOS):
    key = f'fx{k}'
    fr(key, f'   {n}',
       ['—'] + [f'=Supuestos!$B${FAC_ROWS[n]}*12*Supuestos!${chr(67 + t)}${FAC_ROWS[n]}' for t in range(H)])
fr('fx', 'Costos fijos totales',
   ['—'] + [f'=SUM({c}{R["fx0"]}:{c}{R[f"fx{len(FILA_FIJOS) - 1}"]})' for c in COLS])
fr('ebitda', 'EBITDA', [0] + [f'={c}{R["ing"]}-{c}{R["var"]}-{c}{R["fx"]}' for c in COLS], NUM, True)
fr('amort', 'Amortización (no caja, años 1-5)', ['—'] + ['=47000' if t < 5 else 0 for t in range(H)])
fr('acum', 'Pérdida tributaria acumulada previa', [0, 0] + [None] * (H - 1))
for t in range(2, H + 1):
    pc = chr(66 + t - 1)
    ws.cell(row=R['acum'], column=2 + t,
            value=f'=MIN(0,{pc}{R["acum"]}+{pc}{R["ebitda"]}-{pc}{R["amort"]})').number_format = NUM
fr('base', 'Base imponible', ['—'] + [f'=MAX(0,{c}{R["ebitda"]}-{c}{R["amort"]}+{c}{R["acum"]})' for c in COLS])
fr('tax', 'Impuesto (27%)', ['—'] + [f'=-{c}{R["base"]}*Supuestos!$B${S["tasa_imp"]}' for c in COLS])
fr('inv0', 'Inversión inicial', [f'=-Supuestos!$B${S["inv"]}'] + ['—'] * H)
fr('rec', 'Inversión recurrente', ['—'] + [f'=-Supuestos!$B${S["rec"]}' for _ in range(H)])
fr('wcr', f'Recuperación capital de trabajo (año {H})', ['—'] + ['—'] * (H - 1) + [f'=Supuestos!$B${S["wc"]}'])
fr('flujo', 'FLUJO DEL PROYECTO', [f'=B{R["inv0"]}'] +
   [f'={c}{R["ebitda"]}+{c}{R["tax"]}+{c}{R["rec"]}' + (f'+{c}{R["wcr"]}' if c == COLS[-1] else '') for c in COLS],
   NUM, True)
fr('acumf', 'Flujo acumulado', [f'=B{R["flujo"]}', None] + [None] * (H - 1), NUM, True)
for t in range(1, H + 1):
    ws.cell(row=R['acumf'], column=2 + t,
            value=f'={chr(66 + t - 1)}{R["acumf"]}+{chr(66 + t)}{R["flujo"]}').number_format = NUM
    ws.cell(row=R['acumf'], column=2 + t).font = B
ws.cell(row=_r + 2, column=1, value='Inversión inicial en CLP (TC editable):')
ws.cell(row=_r + 2, column=2, value=f"=-B{R['inv0']}*Supuestos!$B${S['tc']}").number_format = NUM
ws.cell(row=_r + 2, column=3, value='actualizar TC en Supuestos').font = IT
ws.column_dimensions['A'].width = 44
for col in 'BCDEFGHIJKL':
    ws.column_dimensions[col].width = 11
ws.freeze_panes = 'B5'
FILA_FLUJO = R['flujo']

# === Escenarios (valores del motor; antes de Evaluacion para la referencia) =
ws = ws_esc
ws['A1'] = 'ESCENARIOS — calculados por el motor (regenerar con: python3 excel/generar_excel.py)'
ws['A1'].font = Font(bold=True, size=12)
cols = ['Pesimista', 'Viable', 'Optimista', 'Diagnostico']
heads = ['Pesimista', 'VIABLE (adoptado)', 'Optimista', 'Diagnóstico original (descartado)']
for j, lab in enumerate(['Indicador'] + heads):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
resumen = {n: flujo_proyecto(p, p['estructura']) for n, p in ESCENARIOS.items()}
rr = 5
def srow(lab, fn, fmt=NUM, bold=False):
    global rr
    ws.cell(row=rr, column=1, value=lab)
    if bold: ws.cell(row=rr, column=1).font = B
    for j, n in enumerate(cols):
        v = fn(n, resumen[n])
        c = ws.cell(row=rr, column=2 + j, value=v if v is not None else '—')
        if isinstance(v, (int, float)): c.number_format = fmt
        if bold: c.font = B
    rr += 1
srow('Instituciones activas año 10', lambda n, r_: ESCENARIOS[n]['inst'][-1], '0')
srow('Ingresos año 10', lambda n, r_: r_['ing'][9])
srow('EBITDA año 5', lambda n, r_: r_['ebitda'][4])
srow('EBITDA año 10', lambda n, r_: r_['ebitda'][9])
VAN_ROW = rr
srow('VAN @ Ke 14,9%', lambda n, r_: round(van(r_['flujo'], ESCENARIOS[n]['ke']), 0), NUM, True)
srow('TIR', lambda n, r_: tir(r_['flujo']), PCT)
srow('PRI simple (años)', lambda n, r_: pri_simple(r_['flujo']), '0.0')
srow('PRI descontado (años)', lambda n, r_: pri_descontado(r_['flujo'], ESCENARIOS[n]['ke']), '0.0')
srow('Déficit de caja máximo (flujo acum. mín.)', lambda n, r_: round(min(r_['acumulado']), 0))
def _van_tv(n, r_):
    if r_['ebitda'][9] <= 0:
        return None
    ke = ESCENARIOS[n]['ke']
    f_norm = r_['ebitda'][9] + r_['taxes'][9] - ESCENARIOS[n]['rec']
    tv = f_norm * 1.03 / (ke - 0.03)
    return round(van(r_['flujo'][:H] + [r_['flujo'][H] - WC + tv], ke), 0)
srow(f'VAN con valor terminal (g=3%, si EBITDA año {H}>0)', _van_tv)
ESP_ROW = rr + 1
ws.cell(row=ESP_ROW, column=1, value='VAN esperado ponderado (0,25 / 0,50 / 0,25)').font = B
c = ws.cell(row=ESP_ROW, column=3,
            value=f'=B{VAN_ROW}*0.25+C{VAN_ROW}*0.5+D{VAN_ROW}*0.25')
c.number_format = NUM; c.font = B
rr = ESP_ROW + 2
ws.cell(row=rr, column=1, value='PUNTO DE EQUILIBRIO — instituciones activas (costos fijos año 5 / margen por institución)').font = B
rr += 1
for lab, st, pr, est in [('Estructura AJUSTADA, precio 2.450, 300 est.', 'ajustada', 2450.0, 300),
                         ('Estructura AJUSTADA, precio 3.000, 350 est.', 'ajustada', 3000.0, 350),
                         ('Estructura BASE (11 personas), precio 2.200', 'base', 2200.0, 230)]:
    ws.cell(row=rr, column=1, value=lab)
    ws.cell(row=rr, column=2, value=round(punto_equilibrio(st, pr, est), 1)).number_format = '0.0'
    rr += 1
ws.column_dimensions['A'].width = 56
for col in 'BCDEF':
    ws.column_dimensions[col].width = 16

# === Evaluacion ============================================================
ws = ws_ev
ws['A1'] = 'EVALUACIÓN ECONÓMICA — caso Viable (horizonte 10 años, Ke CAPM 14,9%)'
ws['A1'].font = Font(bold=True, size=12)
rr = 3
for lab, f, fmt in [('Rf (bono soberano Chile 10a)', f'=Supuestos!B{S["rf"]}', PCT),
                    ('Beta (Damodaran — citar fila y fecha)', f'=Supuestos!B{S["beta"]}', '0.00'),
                    ('Prima de riesgo de mercado', f'=Supuestos!B{S["mrp"]}', PCT),
                    ('Prima de riesgo país', f'=Supuestos!B{S["prp"]}', PCT),
                    ('Ke = Rf + β×PRM + PRP', f'=Supuestos!B{S["ke"]}', PCT)]:
    ws.cell(row=rr, column=1, value=lab)
    c = ws.cell(row=rr, column=2, value=f); c.number_format = fmt
    if lab.startswith('Ke'): c.font = B
    rr += 1
KE = f'$B${rr - 1}'
rr += 1
ws.cell(row=rr, column=1, value='Flujo del proyecto (USD)').font = B
for j in range(H + 1):
    ws.cell(row=rr, column=2 + j, value=f"='Flujo de Caja'!{chr(66 + j)}{FILA_FLUJO}").number_format = NUM
FROW = rr; rr += 1
ws.cell(row=rr, column=1, value='Factor de descuento')
for j in range(H + 1):
    ws.cell(row=rr, column=2 + j, value=f'=1/(1+{KE})^{j}').number_format = '0.000'
FD = rr; rr += 1
ws.cell(row=rr, column=1, value='Flujo descontado')
for j in range(H + 1):
    ws.cell(row=rr, column=2 + j, value=f'={chr(66 + j)}{FROW}*{chr(66 + j)}{FD}').number_format = NUM
FDS = rr; rr += 2

rn = flujo_proyecto(ESCENARIOS['Viable'], 'ajustada')
pri_s = pri_simple(rn['flujo'])
pri_d = pri_descontado(rn['flujo'], 0.149)
van5 = van(rn['flujo'][:6], 0.149)
for lab, val, fmt in [('VAN normal — 10 años (Ke CAPM)', f'=SUM(B{FDS}:L{FDS})', NUM),
                      ('VAN corte a 5 años (referencia: motiva horizonte 10)', round(van5, 0), NUM),
                      ('TIR', f'=IFERROR(IRR(B{FROW}:L{FROW}),"No existe")', '0.0%'),
                      ('VAN ajustado — esperado (prob. 0,25/0,50/0,25)', f'=Escenarios!C{ESP_ROW}', NUM),
                      ('PRI simple (años)', pri_s, '0.0'),
                      ('PRI descontado (años)', pri_d, '0.0')]:
    ws.cell(row=rr, column=1, value=lab).font = B
    c = ws.cell(row=rr, column=2, value=val)
    if fmt: c.number_format = fmt
    c.font = B
    rr += 1
ws.cell(row=rr + 1, column=1, value=('El corte a 5 años es negativo: el SaaS aún está en ramp-up. La viabilidad se evalúa a 10 años '
        '(horizonte permitido por la guía) o con valor terminal (hoja Escenarios).')).font = IT
ws.column_dimensions['A'].width = 52
for col in 'BCDEFGHIJKL':
    ws.column_dimensions[col].width = 12

# === Estado Resultados =====================================================
ws = ws_er
ws['A1'] = 'ESTADO DE RESULTADOS — 3 primeros años (caso Viable)'
ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = 'USD. Préstamo Banca Desarrollo 400k @12%, 3 años de gracia (solo intereses). CORFO no pasa por EERR.'
for j, lab in enumerate(['Concepto', 'Año 1', 'Año 2', 'Año 3']):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
er = eerr(ESCENARIOS['Viable'], 'ajustada', 3)
rr = 5
for lab, key in [('Ingresos', 'ingresos'), ('(−) Costos totales', None), ('EBITDA', 'ebitda'),
                 ('(−) Amortización (años 1-5)', 'amort'), ('EBIT', 'ebit'),
                 ('(−) Intereses (gracia: solo intereses)', 'interes'),
                 ('Base tributaria (antes de arrastre)', 'bt'), ('(−) Impuesto 27%', 'imp'),
                 ('UTILIDAD / (PÉRDIDA) NETA', 'neto')]:
    ws.cell(row=rr, column=1, value=lab)
    for t in range(3):
        v = (er[t]['ingresos'] - er[t]['ebitda']) if key is None else er[t][key]
        c = ws.cell(row=rr, column=2 + t, value=round(v, 0)); c.number_format = NUM
        if lab.isupper():
            c.font = B; ws.cell(row=rr, column=1).font = B
    rr += 1
ws.column_dimensions['A'].width = 46
for col in 'BCD':
    ws.column_dimensions[col].width = 14

# === Balance ===============================================================
ws = ws_bal
ws['A1'] = 'BALANCE GENERAL — 3 primeros años (caso Viable)'
ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = ('USD. Caja negativa en el ramp-up = línea de capital de trabajo comprometida no girada '
            '(declarar en cap. 11); se recupera desde el año 4-5.')
for j, lab in enumerate(['Cuenta', 'Año 1', 'Año 2', 'Año 3']):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
bal = balance(ESCENARIOS['Viable'], 'ajustada', 3)
rr = 5
for lab, key in [('Caja (negativa = línea de CT por girar)', 'caja'), ('Capital de trabajo + reserva', 'wc'),
                 ('Gastos diferidos (neto)', 'diferido'), ('Intangibles (neto)', 'intang'),
                 ('TOTAL ACTIVO', 'activo'), ('Pasivo: Banca Desarrollo (saldo)', 'deuda'),
                 ('Patrimonio: aportes + CORFO + resultados acum.', 'patrimonio'),
                 ('CONTROL: Activo − (Pasivo + Patrimonio) = 0', 'check')]:
    ws.cell(row=rr, column=1, value=lab)
    for t in range(3):
        c = ws.cell(row=rr, column=2 + t, value=round(bal[t][key], 0)); c.number_format = NUM
    if 'TOTAL' in lab or 'CONTROL' in lab:
        for col in range(1, 5):
            ws.cell(row=rr, column=col).font = B
    rr += 1
ws.column_dimensions['A'].width = 50
for col in 'BCD':
    ws.column_dimensions[col].width = 14

wb.save('excel/PedioLink_Flujo_Caja.xlsx')

# ---------------------------------------------------------------- verificación
print('=== MOTOR — VIABLE (10 años, Ke 14,9%) ===')
print('Ingresos k:', [round(x / 1000, 1) for x in rn['ing']])
print('EBITDA  k:', [round(x / 1000, 1) for x in rn['ebitda']])
print('Flujo   k:', [round(x / 1000, 1) for x in rn['flujo']])
print(f'VAN 10a: {van(rn["flujo"], 0.149) / 1000:,.0f} k | VAN 5a: {van5 / 1000:,.0f} k')
print(f'TIR: {tir(rn["flujo"])} | PRI: {pri_s} | PRI desc: {pri_d}')
print('Balance check:', [round(b['check'], 1) for b in bal])
for n in cols:
    r2 = resumen[n]
    t_ = tir(r2['flujo'])
    print(f'{n:12s} VAN={van(r2["flujo"], ESCENARIOS[n]["ke"]) / 1000:>8,.0f}k  TIR={"" if t_ is None else f"{t_:.1%}":>6s}'
          f'  EBITDA10={r2["ebitda"][9] / 1000:>8,.0f}k')
cr = cronograma_prestamo()
print(f'Préstamo: interés y1 {cr[0]["interes"]:,.0f} | servicio y4 {cr[3]["cuota"]:,.0f} | saldo y10 {cr[9]["saldo"]:,.0f}')
print('BE inst año5:', {f'{s}-{int(pr)}-{e}': round(punto_equilibrio(s, pr, e), 1)
                        for s, pr, e in (('ajustada', 2450.0, 300), ('ajustada', 3000.0, 350), ('base', 2200.0, 230))})
