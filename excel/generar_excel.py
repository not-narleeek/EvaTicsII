#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del modelo económico PedioLink (excel/PedioLink_Flujo_Caja.xlsx).

Motor único de supuestos -> flujo de caja, EERR, balance, evaluación y escenarios.
Hoja 'Flujo de Caja' y 'Evaluacion' con fórmulas vivas referenciando 'Supuestos';
'EERR', 'Balance' y 'Escenarios' con valores calculados por este motor.

Uso: python3 generar_excel.py   (regenera el xlsx e imprime verificación)
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# ---------------------------------------------------------------- supuestos
TC_CLP = 950            # CLP/USD referencial (editable en Supuestos)
SAM_UNIV_RM = 128       # 45 hospitales + 83 clínicas RM (BCN 2025)
SAM_PCT = 0.30          # % que cumple requisitos pediátricos + ECG digital (supuesto)

ESTUDIOS, CUPO, EXTRA = 230, 200, 8.0

COSTOS_BASE = {   # fijos mensuales: (base_año1, factores por año)
    'Remuneraciones':               (28000, [1.00, 1.10, 1.21, 1.331, 1.4641]),
    'Cloud base (infra)':           (2500,  [1.00, 1.05, 1.1025, 1.157625, 1.21550625]),
    'Arriendo':                     (2500,  [1.00, 1.02, 1.0404, 1.061208, 1.08243216]),
    'Marketing':                    (3000,  [1.00, 1.20, 1.40, 1.60, 1.80]),
    'Servicios (legal, auditoria)': (1500,  [1.00, 1.05, 1.1025, 1.157625, 1.21550625]),
    'Software y licencias dev':     (800,   [1.00, 1.05, 1.1025, 1.157625, 1.21550625]),
    'Otros (seguros, internet)':    (1200,  [1.00, 1.03, 1.0609, 1.092727, 1.12550881]),
}
COSTOS_AJUSTADA = {  # 7 personas; socios con sueldo parcial año 1-2; coworking año 1-2
    'Remuneraciones':               (12500, [1.00, 1.28, 1.56, 1.716, 1.8876]),
    'Cloud base (infra)':           COSTOS_BASE['Cloud base (infra)'],
    'Arriendo':                     (900,   [1.00, 1.00, 2.00, 2.04, 2.0816]),
    'Marketing':                    COSTOS_BASE['Marketing'],
    'Servicios (legal, auditoria)': (1000,  [1.00, 1.05, 1.1025, 1.157625, 1.21550625]),
    'Software y licencias dev':     COSTOS_BASE['Software y licencias dev'],
    'Otros (seguros, internet)':    (900,   [1.00, 1.03, 1.0609, 1.092727, 1.12550881]),
}
FILA_FIJOS = list(COSTOS_BASE.keys())
CRECIMIENTO = {n: (None if n == 'Marketing' else COSTOS_BASE[n][1]) for n in FILA_FIJOS}

AMORT_INTANG, AMORT_DIFERIDO, WC, RECURRENTE, TASA_IMP = 31000.0, 16000.0, 50000.0, 70000.0, 0.27
APORTES, PRESTAMO, CORFO, TASA_PREST, PLAZO = 99750.0, 99750.0, 85500.0, 0.12, 60

ESCENARIOS = {
    'Pesimista':          dict(inst=[1, 2, 3, 4, 5],   precio=1500.0, impl=6000.0, cloud_var=3.00, inversion=320000.0, rec=80000.0, ke=0.14,  estructura='base'),
    'Normal':             dict(inst=[2, 4, 6, 8, 10],  precio=2200.0, impl=8000.0, cloud_var=1.50, inversion=285000.0, rec=70000.0, ke=0.149, estructura='base'),
    'Optimista':          dict(inst=[3, 6, 10, 13, 16], precio=3000.0, impl=8000.0, cloud_var=0.80, inversion=260000.0, rec=70000.0, ke=0.10,  estructura='base'),
    'Normal-Ajustada':    dict(ESCENARIOS := None or {}, **{}) if False else dict(inst=[2, 4, 6, 8, 10],  precio=2200.0, impl=8000.0, cloud_var=1.50, inversion=285000.0, rec=70000.0, ke=0.149, estructura='ajustada'),
    'Optimista-Ajustada': dict(inst=[3, 6, 10, 13, 16], precio=3000.0, impl=8000.0, cloud_var=0.80, inversion=260000.0, rec=70000.0, ke=0.10,  estructura='ajustada'),
}
PROB = (0.25, 0.50, 0.25)  # pesimista, normal, optimista

# ---------------------------------------------------------------- motor
def meses_inst(inst):
    out, prev = [], 0.0
    for a in inst:
        out.append((prev + a) / 2 * 12)
        prev = a
    return out

def costos_fijos(struct):
    tabla = COSTOS_BASE if struct == 'base' else COSTOS_AJUSTADA
    return {n: [tabla[n][0] * f for f in tabla[n][1]] for n in FILA_FIJOS}

def cronograma_prestamo():
    i = TASA_PREST / 12
    cuota = PRESTAMO * i * (1 + i) ** PLAZO / ((1 + i) ** PLAZO - 1)
    saldo, filas = PRESTAMO, []
    for _ in range(5):
        inte = prin = 0.0
        for _m in range(12):
            ip = saldo * i
            inte += ip
            prin += cuota - ip
            saldo -= cuota - ip
        filas.append(dict(interes=inte, principal=prin, saldo=saldo, cuota=cuota * 12))
    return filas

def impuestos_con_arrastre(bases):
    out, acum = [], 0.0
    for b in bases:
        out.append(max(0.0, b + min(0.0, acum)) * TASA_IMP)
        acum += b
    return out

def flujo_proyecto(p, struct):
    mi = meses_inst(p['inst'])
    fijos = costos_fijos(struct)
    fx = [sum(fijos[n][t] for n in FILA_FIJOS) for t in range(5)]
    ing, ebitda, var, bases = [], [], [], []
    for t in range(5):
        nuevas = p['inst'][t] - (p['inst'][t - 1] if t else 0)
        i_susc = mi[t] * p['precio']
        i_extra = mi[t] * max(0, ESTUDIOS - CUPO) * EXTRA
        i_impl = nuevas * p['impl']
        ing.append(i_susc + i_extra + i_impl)
        var.append(mi[t] * ESTUDIOS * p['cloud_var'])
        ebitda.append(ing[t] - var[t] - fx[t] * 12)
        bases.append(ebitda[t] - AMORT_INTANG - AMORT_DIFERIDO)
    taxes = impuestos_con_arrastre(bases)
    fl = [-p['inversion']] + [ebitda[t] - taxes[t] - p['rec'] for t in range(5)]
    fl[5] += WC
    acum, s = [], 0.0
    for f in fl:
        s += f
        acum.append(s)
    return dict(ing=ing, ebitda=ebitda, var=var, fijos_m=fx, meses=mi, taxes=taxes,
                flujo=fl, acumulado=acum, p=p, struct=struct)

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
        bt = ebit - cr[t]['interes']                       # base contable
        bt_fisc = bt + min(0.0, acum)                      # base fiscal con arrastre
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
        pas = cr[t]['saldo']
        filas.append(dict(caja=caja, wc=WC, diferido=80000 - AMORT_DIFERIDO * (t + 1),
                          intang=155000 - AMORT_INTANG * (t + 1), activo=activo,
                          deuda=pas, patrimonio=pat, check=activo - (pas + pat)))
    return filas

def punto_equilibrio(struct, precio):
    fijos = costos_fijos(struct)
    fx3 = sum(fijos[n][2] for n in FILA_FIJOS)  # año 3
    contrib = precio + max(0, ESTUDIOS - CUPO) * EXTRA - ESTUDIOS * COSTOS_BASE['Cloud base (infra)'][0] * 0 - ESTUDIOS * 1.50
    return fx3 / contrib

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

# === Supuestos ============================================================
ws = hoja('Supuestos', 'FFC000')
ws['A1'] = 'SUPUESTOS — única fuente de verdad del modelo'; ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = 'Celdas amarillas = editables (el modelo se recalcula). Montos en USD salvo indicación.'
S, r = {}, 4

def sec(titulo):
    global r
    ws.cell(row=r, column=1, value=titulo).font = B
    ws.cell(row=r, column=1).fill = FILL_SEC
    r += 1

def put(label, value, fmt=NUM, key=None, nota=''):
    global r
    ws.cell(row=r, column=1, value=label)
    c = ws.cell(row=r, column=2, value=value)
    c.number_format = fmt
    if key:
        c.fill = FILL_IN
        S[key] = r
    if nota:
        ws.cell(row=r, column=3, value=nota).font = IT
    r += 1

sec('Mercado')
put('Universo RM (hospitales + clínicas, BCN 2025)', SAM_UNIV_RM, key='univ', nota='45 hospitales + 83 clínicas (BCN, 2025, sección 4.4)')
put('% que cumple requisitos (pediatría + ECG digital)', SAM_PCT, PCT, key='sam_pct', nota='SUPUESTO a validar con catastro')
ws.cell(row=r, column=1, value='SAM calificado (instituciones)')
ws.cell(row=r, column=2, value=f'=ROUND(B{S["univ"]}*B{S["sam_pct"]},0)').number_format = NUM
S['sam'] = r; r += 1

sec('Comercial')
put('Precio suscripción (USD/mes) — Normal', 2200.0, key='precio')
put('Cargo implementación (una vez)', 8000.0, key='impl')
put('Estudios promedio por institución (mes)', ESTUDIOS, key='estudios')
put('Cupo base incluido (estudios/mes)', CUPO, key='cupo')
put('Precio estudio adicional (USD)', EXTRA, key='extra')
put('Costo cloud variable (USD/estudio) — Normal', 1.50, key='cloud_var')

sec('Instituciones activas al cierre de año')
ws.cell(row=r, column=1, value='Escenario').font = B
for j, lab in enumerate(['Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5']):
    ws.cell(row=r, column=2 + j, value=lab).font = B
r += 1
for nom in ('Pesimista', 'Normal', 'Optimista'):
    ws.cell(row=r, column=1, value=nom)
    for j, v in enumerate(ESCENARIOS[nom]['inst']):
        ws.cell(row=r, column=2 + j, value=v).fill = FILL_IN
    S[f'inst_{nom}'] = r
    r += 1

sec('Costos fijos mensuales (estructura BASE, cap. 12: 11 personas)')
for j, lab in enumerate(['Ítem', 'Año 1 (USD/mes)', 'Crecimiento anual']):
    ws.cell(row=r, column=1 + j, value=lab).font = B
r += 1
for n in FILA_FIJOS:
    put(n, COSTOS_BASE[n][0], key=f'fx_{FILA_FIJOS.index(n)}')
    fac = CRECIMIENTO[n]
    c = ws.cell(row=r - 1, column=3, value='serie 1,0–1,8× año 1' if fac is None else fac[1] - 1)
    c.number_format = '0.0%' if fac else '@'
    c.font = IT

sec('Inversión y financiamiento')
put('Inversión inicial (cap. 10)', 285000.0, key='inv')
put('Inversión recurrente anual (años 1-5, cap. 10)', RECURRENTE, key='rec')
put('Capital de trabajo (se recupera año 5)', WC, key='wc')
put('Aporte socios', APORTES, key='aportes')
put('Préstamo BancEstado', PRESTAMO, key='prestamo')
put('Tasa anual préstamo', TASA_PREST, PCT, key='tasa_p')
put('Plazo préstamo (años)', 5, '0', key='plazo')
put('Subsidio CORFO (no reembolsable, a patrimonio)', CORFO, key='corfo')

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
ws.cell(row=r, column=1, value=('Notas: (1) Cloud = base 2.500/mes + variable 1,50/estudio (cap. 12 unificaba 3.500 sin separar). '
        '(2) CORFO como donación a patrimonio, no pasa por EERR. (3) Arrastre infinito de pérdidas tributarias. '
        '(4) Amortización: intangibles 155k/5a (desarrollo 120k + certificación 35k) y gastos diferidos 80k/5a '
        '(marketing 15k + setup cloud 15k + contratación 50k).')).font = IT
ws.column_dimensions['A'].width = 52
ws.column_dimensions['B'].width = 14
ws.column_dimensions['C'].width = 40
ws.freeze_panes = 'A4'

# === Flujo de Caja (fórmulas vivas) =======================================
ws = hoja('Flujo de Caja', '2E75B6')
ws['A1'] = 'FLUJO DE CAJA PROYECTADO — Normal, estructura BASE (caps. 10-12)'; ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = 'USD. Fórmulas vivas: editar Supuestos recalcula todo.'
for j, lab in enumerate(['Concepto', 'Año 0', 'Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5']):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H

R, _r = {}, 4
def fr(key, label, vals, fmt=NUM, bold=False):
    global _r
    _r += 1
    ws.cell(row=_r, column=1, value=label).font = B if bold else Font()
    for j, v in enumerate(vals):
        c = ws.cell(row=_r, column=2 + j, value=v)
        if fmt and not isinstance(v, str) or (fmt and isinstance(v, str) and v.startswith('=')):
            c.number_format = fmt
        if bold: c.font = B
    R[key] = _r

fr('inst', 'Instituciones activas (cierre)', ['—', 2, 4, 6, 8, 10], '0')
fr('meses', 'Meses-institución (activación uniforme)',
   ['—', f'=C{R["inst"]}*12/2'] +
   [f'=({chr(66+t-1)}{R["inst"]}+{chr(67+t-1)}{R["inst"]})*12/2' for t in range(2, 6)])
fr('susc', 'Ingreso suscripción', ['—'] + [f'={c}{R["meses"]}*Supuestos!$B${S["precio"]}' for c in 'CDEFG'])
fr('extra', 'Ingreso estudios adicionales',
   ['—'] + [f'={c}{R["meses"]}*MAX(0,Supuestos!$B${S["estudios"]}-Supuestos!$B${S["cupo"]})*Supuestos!$B${S["extra"]}' for c in 'CDEFG'])
fr('impl', 'Ingreso implementación',
   ['—', f'=C{R["inst"]}*Supuestos!$B${S["impl"]}', f'=(D{R["inst"]}-C{R["inst"]})*Supuestos!$B${S["impl"]}',
    f'=(E{R["inst"]}-D{R["inst"]})*Supuestos!$B${S["impl"]}', f'=(F{R["inst"]}-E{R["inst"]})*Supuestos!$B${S["impl"]}',
    f'=(G{R["inst"]}-F{R["inst"]})*Supuestos!$B${S["impl"]}'])
fr('ing', 'INGRESOS TOTALES', [0] + [f'=SUM({c}{R["susc"]}:{c}{R["impl"]})' for c in 'CDEFG'], NUM, True)
fr('var', 'Costo variable cloud',
   ['—'] + [f'={c}{R["meses"]}*Supuestos!$B${S["estudios"]}*Supuestos!$B${S["cloud_var"]}' for c in 'CDEFG'])
for k, n in enumerate(FILA_FIJOS):
    row = f'fxbase{k}'
    fr(row, f'   {n}', ['—', f'=Supuestos!$B${S[f"fx_{k}"]}*12'])
    for t in range(1, 5):
        col, prev = chr(67 + t), chr(66 + t)
        if CRECIMIENTO[n] is None:
            f = f'=$C{R[row]}*{[1.2, 1.4, 1.6, 1.8][t - 1]}'
        else:
            g = CRECIMIENTO[n][t] / CRECIMIENTO[n][t - 1]
            f = f'={prev}{R[row]}*{g:.6f}'
        ws.cell(row=R[row], column=3 + t, value=f).number_format = NUM
fr('fx', 'Costos fijos totales', ['—'] + [f'=SUM({c}{R["fxbase0"]}:{c}{R[f"fxbase{len(FILA_FIJOS)-1}"]})' for c in 'CDEFG'])
fr('ebitda', 'EBITDA', [0] + [f'={c}{R["ing"]}-{c}{R["var"]}-{c}{R["fx"]}' for c in 'CDEFG'], NUM, True)
fr('amort', 'Amortización (no caja)', ['—'] + ['=31000+16000'] * 5)
fr('acum', 'Pérdida tributaria acumulada previa', [0, 0, None, None, None, None])
for t in range(2, 6):
    pc = chr(66 + t - 1)
    ws.cell(row=R['acum'], column=2 + t,
            value=f'=MIN(0,{pc}{R["acum"]}+{pc}{R["ebitda"]}-{pc}{R["amort"]})').number_format = NUM
fr('base', 'Base imponible', ['—'] + [f'=MAX(0,{c}{R["ebitda"]}-{c}{R["amort"]}+{c}{R["acum"]})' for c in 'CDEFG'])
fr('tax', 'Impuesto (27%)', ['—'] + [f'=-{c}{R["base"]}*Supuestos!$B${S["tasa_imp"]}' for c in 'CDEFG'])
fr('inv0', 'Inversión inicial', [f'=-Supuestos!$B${S["inv"]}'] + ['—'] * 5)
fr('rec', 'Inversión recurrente', ['—'] + [f'=-Supuestos!$B${S["rec"]}' for _ in range(5)])
fr('wcr', 'Recuperación capital de trabajo', ['—', '—', '—', '—', '—', f'=Supuestos!$B${S["wc"]}'])
fr('flujo', 'FLUJO DEL PROYECTO', [f'=B{R["inv0"]}'] +
   [f'={c}{R["ebitda"]}+{c}{R["tax"]}+{c}{R["rec"]}' + (f'+{c}{R["wcr"]}' if c == 'G' else '') for c in 'CDEFG'], NUM, True)
fr('acumf', 'Flujo acumulado', [f'=B{R["flujo"]}', None, None, None, None, None], NUM, True)
for t in range(5):
    ws.cell(row=R['acumf'], column=3 + t,
            value=f'={chr(66+t)}{R["acumf"]}+{chr(67+t)}{R["flujo"]}').number_format = NUM
    ws.cell(row=R['acumf'], column=3 + t).font = B
ws.cell(row=_r + 2, column=1, value='Inversión inicial en CLP (TC editable):')
ws.cell(row=_r + 2, column=2, value=f"=-B{R['inv0']}*Supuestos!$B${S['tc']}").number_format = NUM
ws.cell(row=_r + 2, column=3, value='actualizar TC en Supuestos').font = IT
ws.column_dimensions['A'].width = 44
for col in 'BCDEFG':
    ws.column_dimensions[col].width = 13
ws.freeze_panes = 'B5'
FILA_FLUJO = R['flujo']

# === Estado Resultados =====================================================
ws = hoja('Estado Resultados', '70AD47')
ws['A1'] = 'ESTADO DE RESULTADOS — 3 primeros años (Normal, estructura BASE)'; ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = 'USD. Préstamo 99.750 @12% mensual, 60 cuotas (≈2.219/mes). CORFO no pasa por EERR (donación a patrimonio).'
for j, lab in enumerate(['Concepto', 'Año 1', 'Año 2', 'Año 3']):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
er = eerr(ESCENARIOS['Normal'], 'base', 3)
rr = 5
for lab, key in [('Ingresos', 'ingresos'), ('(−) Costos totales', None), ('EBITDA', 'ebitda'),
                 ('(−) Amortización intangibles + diferidos', 'amort'), ('EBIT', 'ebit'),
                 ('(−) Intereses', 'interes'), ('Base tributaria (antes de arrastre)', 'bt'),
                 ('(−) Impuesto 27%', 'imp'), ('UTILIDAD / (PÉRDIDA) NETA', 'neto')]:
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
ws = hoja('Balance', '7030A0')
ws['A1'] = 'BALANCE GENERAL — 3 primeros años (Normal, estructura BASE)'; ws['A1'].font = Font(bold=True, size=12)
ws['A2'] = 'USD. Caja negativa = DÉFICIT de financiamiento: la estructura de capital cubre solo la inversión inicial (285k).'
for j, lab in enumerate(['Cuenta', 'Año 1', 'Año 2', 'Año 3']):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
bal = balance(ESCENARIOS['Normal'], 'base', 3)
rr = 5
for lab, key in [('Caja (negativa = déficit de financiamiento)', 'caja'), ('Capital de trabajo', 'wc'),
                 ('Gastos diferidos (neto)', 'diferido'), ('Intangibles (neto)', 'intang'),
                 ('TOTAL ACTIVO', 'activo'), ('Pasivo: préstamo BancEstado (saldo)', 'deuda'),
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

# === Evaluacion ============================================================
ws = hoja('Evaluacion', 'C00000')
ws['A1'] = 'EVALUACIÓN ECONÓMICA — escenario Normal'; ws['A1'].font = Font(bold=True, size=12)
ws['A3'] = 'CAPM — corrección: el informe declaraba Ke 11,4%, pero sus propios insumos dan 14,9%'; ws['A3'].font = B
rr = 4
for lab, f, fmt in [('Rf (bono soberano Chile 10a)', f'=Supuestos!B{S["rf"]}', PCT),
                    ('Beta (Damodaran — citar fila y fecha)', f'=Supuestos!B{S["beta"]}', '0.00'),
                    ('Prima de riesgo de mercado', f'=Supuestos!B{S["mrp"]}', PCT),
                    ('Prima de riesgo país', f'=Supuestos!B{S["prp"]}', PCT),
                    ('Ke = Rf + β×PRM + PRP', f'=Supuestos!B{S["ke"]}', PCT)]:
    ws.cell(row=rr, column=1, value=lab)
    c = ws.cell(row=rr, column=2, value=f); c.number_format = fmt
    if lab.startswith('Ke'):
        c.font = B
    rr += 1
KE = f'$B${rr - 1}'
rr += 1
ws.cell(row=rr, column=1, value='Flujo del proyecto (USD)').font = B
for j in range(6):
    ws.cell(row=rr, column=2 + j, value=f"='Flujo de Caja'!{chr(66 + j)}{FILA_FLUJO}").number_format = NUM
FROW = rr; rr += 1
ws.cell(row=rr, column=1, value='Factor de descuento')
for j in range(6):
    ws.cell(row=rr, column=2 + j, value=f'=1/(1+{KE})^{j}').number_format = '0.000'
FD = rr; rr += 1
ws.cell(row=rr, column=1, value='Flujo descontado')
for j in range(6):
    ws.cell(row=rr, column=2 + j, value=f'={chr(66 + j)}{FROW}*{chr(66 + j)}{FD}').number_format = NUM
FDS = rr; rr += 2

rn = flujo_proyecto(ESCENARIOS['Normal'], 'base')
cr = cronograma_prestamo()
# escudo tributario: solo año 1 genera beneficio (años 2-5 sin base tributaria positiva)
escudo = TASA_IMP * cr[0]['interes'] / (1 + TASA_PREST)
apv = van(rn['flujo'], 0.149) + escudo
pri_s = pri_simple(rn['flujo'])
pri_d = pri_descontado(rn['flujo'], 0.149)
for lab, val, fmt in [('VAN normal (Ke CAPM)', f'=SUM(B{FDS}:G{FDS})', NUM),
                      ('TIR', f'=IFERROR(IRR(B{FROW}:G{FROW}),"No existe: flujos siempre negativos")', '0.0%'),
                      ('VAN ajustado — esperado (prob. 0,25/0,50/0,25)', '=Escenarios!C31', NUM),
                      ('VAN ajustado — APV (VAN + VA escudo tributario)', round(apv, 0), NUM),
                      ('PRI simple (años)', pri_s if pri_s else 'No recupera', '0.00'),
                      ('PRI descontado (años)', pri_d if pri_d else 'No recupera', '0.00')]:
    ws.cell(row=rr, column=1, value=lab).font = B
    c = ws.cell(row=rr, column=2, value=val)
    if fmt:
        c.number_format = fmt
    c.font = B
    rr += 1
ws.column_dimensions['A'].width = 50
for col in 'BCDEFG':
    ws.column_dimensions[col].width = 14

# === Escenarios ============================================================
ws = hoja('Escenarios', 'ED7D31')
ws['A1'] = 'ESCENARIOS — calculados por el motor (regenerar con: python3 excel/generar_excel.py)'; ws['A1'].font = Font(bold=True, size=12)
cols = ['Pesimista', 'Normal', 'Optimista', 'Normal-Ajustada', 'Optimista-Ajustada']
for j, lab in enumerate(['Indicador'] + cols):
    c = ws.cell(row=4, column=1 + j, value=lab); c.font = B; c.fill = FILL_H
resumen = {n: flujo_proyecto(p, p['estructura']) for n, p in ESCENARIOS.items()}
rr = 5
def srow(lab, fn, fmt=NUM, bold=False):
    global rr
    ws.cell(row=rr, column=1, value=lab)
    if bold:
        ws.cell(row=rr, column=1).font = B
    for j, n in enumerate(cols):
        v = fn(n, resumen[n])
        c = ws.cell(row=rr, column=2 + j, value=v if v is not None else '—')
        if isinstance(v, (int, float)):
            c.number_format = fmt
        if bold:
            c.font = B
    rr += 1
srow('Instituciones activas año 5', lambda n, r_: ESCENARIOS[n]['inst'][-1], '0')
srow('Ingresos año 5', lambda n, r_: r_['ing'][4])
srow('EBITDA año 5', lambda n, r_: r_['ebitda'][4])
VAN_ROW = rr
srow('VAN (a Ke del escenario)', lambda n, r_: round(van(r_['flujo'], ESCENARIOS[n]['ke']), 0), NUM, True)
srow('TIR', lambda n, r_: tir(r_['flujo']), PCT)
srow('PRI simple (años)', lambda n, r_: pri_simple(r_['flujo']), '0.00')
srow('Déficit de caja máximo (flujo acum. mín.)', lambda n, r_: round(min(r_['acumulado']), 0))
def _van_tv(n, r_):
    if r_['ebitda'][4] <= 0:
        return None
    ke = ESCENARIOS[n]['ke']
    f_norm = r_['ebitda'][4] + r_['taxes'][4] - ESCENARIOS[n]['rec']   # flujo normalized sin WC
    tv = f_norm * 1.03 / (ke - 0.03)
    return round(van(r_['flujo'][:5] + [r_['flujo'][5] - WC + tv], ke), 0)  # reemplaza recup. WC por TV
srow('VAN con valor terminal (g=3%, solo si EBITDA5>0)', _van_tv)
# VAN esperado en fila 31 (referenciada por Evaluacion): col B=Pes, C=Nor, D=Opt
ws.cell(row=31, column=1, value='VAN esperado ponderado (0,25 / 0,50 / 0,25) sobre Pesimista-Normal-Optimista')
ws.cell(row=31, column=3, value=f'=B{VAN_ROW}*0.25+C{VAN_ROW}*0.5+D{VAN_ROW}*0.25').number_format = NUM
ws.cell(row=31, column=1).font = B
ws.cell(row=31, column=3).font = B
rr = 33
ws.cell(row=rr, column=1, value='PUNTO DE EQUILIBRIO — instituciones activas (costos fijos año 3 / margen por institución)').font = B
rr += 1
for lab, st, pr in [('Estructura BASE (11 personas), precio 2.200', 'base', 2200.0),
                    ('Estructura BASE, precio 3.000', 'base', 3000.0),
                    ('Estructura AJUSTADA (7 personas), precio 2.200', 'ajustada', 2200.0),
                    ('Estructura AJUSTADA, precio 3.000', 'ajustada', 3000.0)]:
    ws.cell(row=rr, column=1, value=lab)
    ws.cell(row=rr, column=2, value=round(punto_equilibrio(st, pr), 1)).number_format = '0.0'
    rr += 1
rr += 1
ws.cell(row=rr, column=1, value=('Lectura: con las hipótesis declaradas del informe (2→10 instituciones, 2.200 USD/mes, equipo de 11), '
        'el punto de equilibrio exige ≈2× las instituciones capturables → sin equilibrio operativo en 5 años. '
        'Condiciones de viabilidad y cifras para los caps. 17-20 en docs/excel-notas.md.')).font = IT
ws.column_dimensions['A'].width = 60
for col in 'BCDEF':
    ws.column_dimensions[col].width = 17

wb.save('excel/PedioLink_Flujo_Caja.xlsx')

# ---------------------------------------------------------------- verificación
print('=== MOTOR — Normal / BASE ===')
print('Ingresos k:', [round(x / 1000, 1) for x in rn['ing']])
print('EBITDA  k:', [round(x / 1000, 1) for x in rn['ebitda']])
print('Flujo   k:', [round(x / 1000, 1) for x in rn['flujo']])
print(f'VAN @14,9%: {van(rn["flujo"], 0.149) / 1000:,.0f} k | TIR: {tir(rn["flujo"])} | PRI: {pri_simple(rn["flujo"])} | PRI desc: {pri_d}')
print(f'APV: {apv / 1000:,.0f} k (escudo y1 {escudo / 1000:,.1f} k)')
for n in cols:
    r2 = resumen[n]
    print(f'{n:22s} VAN={van(r2["flujo"], ESCENARIOS[n]["ke"]) / 1000:>9,.0f}k  EBITDA5={r2["ebitda"][4] / 1000:>8,.0f}k  minCaja={min(r2["acumulado"]) / 1000:>8,.0f}k')
print('Balance check:', [round(b['check'], 1) for b in bal])
print('BE inst año3:', {f'{s}-{int(p)}': round(punto_equilibrio(s, p), 1) for s in ('base', 'ajustada') for p in (2200.0, 3000.0)})
print(f'Cuota préstamo anual: {cr[0]["cuota"]:,.0f} | interés y1: {cr[0]["interes"]:,.0f} | saldo y3: {cr[2]["saldo"]:,.0f}')
