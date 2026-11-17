#!/usr/bin/env python3
"""Modelo financiero de Quickexpense (capítulo 8).

Genera en Markdown las tablas que se copian a las secciones Respuesta del
capítulo 8. Todos los supuestos están en SUPUESTOS y en las funciones de
escenario; cambiarlos acá y volver a correr:

    python3 herramientas/modelo_financiero.py > /tmp/modelo.md

Moneda: USD. Horizonte: año 0 (oct. 2026 a may. 2027, etapa preoperativa)
y años 1 a 3 (jun. 2027 a may. 2030).
"""

from dataclasses import dataclass, replace
from math import floor

TIPO_DE_CAMBIO = 1540.0  # ARS por USD, BNA minorista (20/10/2026)
# IVA sobre servicios digitales del exterior (RG 4240), no recuperable para un
# monotributista. Se supone que se pagan con dólares propios: sin la percepción del 30%.
IVA_EXTERIOR = 1.21


def ars(monto: float) -> float:
    return monto / TIPO_DE_CAMBIO


# --- Costo de IA por mensaje (precios oficiales, USD por millón de tokens) ---
HAIKU_IN, HAIKU_CACHE, HAIKU_OUT = 0.10, 0.01, 0.50
SONNET_IN, SONNET_CACHE, SONNET_OUT = 2.00, 0.10, 10.00
JEV_IN, JEV_OUT = 0.042, 0.0  # TypeSafe Jev: USD 42 por mil millones de tokens de entrada, salida gratis
WHISPER_MIN = 0.006


def costo_llamada(tokens_in, prop_cache, tokens_out, p_in, p_cache, p_out):
    cache = tokens_in * prop_cache
    nuevo = tokens_in - cache
    return (cache * p_cache + nuevo * p_in + tokens_out * p_out) / 1e6


# Mensaje simple (Haiku 5.5): 3 llamadas por mensaje (tool calling),
# 12.000 tokens de entrada (50% en caché) y 400 de salida por llamada.
# Las decisiones menores con Jev dentro del chat son despreciables.
COSTO_MENSAJE = 3 * costo_llamada(12_000, 0.5, 400, HAIKU_IN, HAIKU_CACHE, HAIKU_OUT)
# Operación compleja (Sonnet 5.5: conciliación, carga masiva): 4 llamadas
# de 40.000 tokens de entrada (50% en caché) y 1.500 de salida.
COSTO_OPERACION = 4 * costo_llamada(40_000, 0.5, 1_500, SONNET_IN, SONNET_CACHE, SONNET_OUT)
COSTO_AUDIO = 0.5 * WHISPER_MIN  # audio promedio de 30 segundos
# Categorización automática y sugerencias de conciliación sin chat (Jev):
# 5.000 tokens de entrada por movimiento.
COSTO_MOVIMIENTO_JEV = costo_llamada(5_000, 0, 0, JEV_IN, JEV_IN, JEV_OUT)

# Uso mensual supuesto
USO = {
    # plan: (mensajes al asistente, operaciones complejas, audios)
    "premium": (150, 5, 15),
    # Asistente en Telegram con tope de 15 mensajes por día, solo para cargar gastos
    # y consultar el saldo (texto y audios, con Haiku 5.5).
    "gratuito": (120, 0, 12),
}
MOVIMIENTOS_WEB_GRATUITO = 60  # cargados desde la web y categorizados con Jev


def costo_ia_usuario(plan: str) -> float:
    msj, ops, audios = USO[plan]
    costo = msj * COSTO_MENSAJE + ops * COSTO_OPERACION + audios * COSTO_AUDIO
    if plan == "gratuito":
        costo += MOVIMIENTOS_WEB_GRATUITO * COSTO_MOVIMIENTO_JEV
    return costo


@dataclass(frozen=True)
class Supuestos:
    nombre: str = "Base"
    precio: float = 6.99
    factor_precio_usd: float = 1.0  # <1 si el precio en pesos se atrasa frente al dólar
    comision_mp: float = 0.0642 * 1.21  # Mercado Pago, Santa Fe, acreditación al instante, + IVA
    descuento_temprano: float = 0.30  # Alpha y Beta, durante el primer año
    prop_tempranos: float = 0.5  # suscriptores del año 1 que vienen de Alpha/Beta
    prop_activos: float = 0.30
    conversion: float = 0.05  # desde el año 2
    registrados_a1: tuple = (40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150)
    pagos_a1: tuple = (1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8)
    altas_anuales: float = 150  # años 2 y 3
    factor_ia: float = 1.0
    ia_premium: float = costo_ia_usuario("premium") * IVA_EXTERIOR
    ia_gratuito: float = costo_ia_usuario("gratuito") * IVA_EXTERIOR
    ia_desarrollo: float = 50.0 * IVA_EXTERIOR  # consumo de IA del desarrollo y las pruebas
    # Prueba obligatoria de un mes del plan premium, sin tarjeta, para cada usuario
    # nuevo desde el lanzamiento (los de Alpha y Beta ya lo conocen). Usa la IA y WhatsApp
    # como un suscriptor.
    prueba: bool = True
    # WhatsApp solo para el plan premium y la prueba (el gratuito usa Telegram, con tope, y la web).
    whatsapp_msj: float = 0.026 * IVA_EXTERIOR  # servicio y utilidad, Argentina, desde 01/10/2026
    whatsapp_gratis: float = 1000  # mensajes de servicio sin cargo por mes y por número
    whatsapp_plantillas: float = 52 / 12  # aviso semanal por suscriptor
    whatsapp_mensajes: float = USO["premium"][0]  # respuestas por WhatsApp por suscriptor y mes
    servidor: float = 30.0 * IVA_EXTERIOR
    contador: float = 45.0
    monotributo: float = ars(49_527.18)  # categoría A, ago. 2026
    iibb: float = ars(12_269)  # Santa Fe, régimen simplificado, categoría I
    drei: float = ars(34 * 526)  # Rosario, régimen simplificado, categoría I
    horas_fundador_mes: float = 10 * 52 / 12
    valor_hora: float = 10.0
    meses_preoperativos: int = 8
    marca_inpi: float = ars(100 * 360)  # 100 UMAPI (valor inicial, Res. INPI 75/2026)
    tasa: float = 0.0510 + 0.1394  # rf (bono a 10 años de EE. UU.) + prima total de Argentina (Damodaran), beta 1


def costo_whatsapp(s: Supuestos, usuarios: float) -> float:
    """Usuarios con WhatsApp: suscriptores más usuarios en prueba activos."""
    servicio = max(usuarios * s.whatsapp_mensajes - s.whatsapp_gratis, 0)
    return (servicio + usuarios * s.whatsapp_plantillas) * s.whatsapp_msj


def prueba_mensual(s: Supuestos) -> float:
    """Usuarios en prueba activos por mes, en régimen (años 2 y 3)."""
    return s.altas_anuales / 12 * s.prop_activos if s.prueba else 0.0


def fundador_mes(s: Supuestos) -> float:
    return s.horas_fundador_mes * s.valor_hora


def redondear(x: float) -> int:
    return floor(x + 0.5)


def meses(s: Supuestos):
    """Una fila por mes operativo (1 a 36)."""
    filas = []
    for m in range(1, 37):
        if m <= 12:
            reg = s.registrados_a1[m - 1]
            pagos = s.pagos_a1[m - 1]
            altas = reg - s.registrados_a1[m - 2] if m > 1 else 0  # el mes 1 son los de Alpha y Beta
        else:
            reg = s.registrados_a1[-1] + s.altas_anuales * (m - 12) / 12
            pagos = redondear(s.conversion * reg)
            altas = s.altas_anuales / 12
        activos = s.prop_activos * reg
        en_prueba = altas * s.prop_activos if s.prueba else 0.0
        gratis_activos = max(activos - pagos - en_prueba, 0)
        precio = s.precio * s.factor_precio_usd
        if m <= 12:
            precio *= 1 - s.prop_tempranos * s.descuento_temprano
        bruto = pagos * precio
        comision = bruto * s.comision_mp
        ia_var = (pagos * s.ia_premium + gratis_activos * s.ia_gratuito) * s.factor_ia
        filas.append(dict(
            mes=m, registrados=reg, activos=activos, pagos=pagos,
            en_prueba=en_prueba, gratis_activos=gratis_activos,
            ingreso_bruto=bruto, comision=comision,
            ia_variable=ia_var,
            ia_prueba=en_prueba * s.ia_premium * s.factor_ia,
            whatsapp=costo_whatsapp(s, pagos + en_prueba),
            ia_desarrollo=s.ia_desarrollo * s.factor_ia,
            servidor=s.servidor,
            contador=s.contador,
            monotributo=s.monotributo, iibb=s.iibb, drei=s.drei,
            fundador=fundador_mes(s),
        ))
    return filas


def anual(filas, clave, anio):
    return sum(f[clave] for f in filas[(anio - 1) * 12: anio * 12])


def inversion(s: Supuestos):
    n = s.meses_preoperativos
    items = {
        "Desarrollo del software (tiempo del fundador)": n * fundador_mes(s),
        "Servidor durante Alpha y Beta": n * s.servidor,
        "IA durante el desarrollo, Alpha y Beta": n * s.ia_desarrollo,
        "Registro de la marca (INPI, una clase)": s.marca_inpi,
    }
    return items


def capital_trabajo(s: Supuestos, filas):
    """Método del desfase: un mes de egresos de caja del primer mes operativo."""
    f = filas[0]
    claves = ["comision", "ia_variable", "ia_prueba", "whatsapp", "ia_desarrollo", "servidor",
              "contador", "monotributo", "iibb", "drei"]
    return sum(f[k] for k in claves)


def flujo(s: Supuestos, incluir_fundador=True):
    filas = meses(s)
    inv = sum(inversion(s).values())
    if not incluir_fundador:
        inv -= s.meses_preoperativos * fundador_mes(s)
    ct = capital_trabajo(s, filas)
    flujos = [-(inv + ct)]
    detalle = []
    for a in (1, 2, 3):
        d = {k: anual(filas, k, a) for k in filas[0]
             if k not in ("mes", "registrados", "activos", "pagos", "en_prueba", "gratis_activos")}
        egresos = (d["comision"] + d["ia_variable"] + d["ia_prueba"] + d["whatsapp"] + d["ia_desarrollo"]
                   + d["servidor"] + d["contador"] + d["monotributo"] + d["iibb"] + d["drei"])
        if incluir_fundador:
            egresos += d["fundador"]
        neto = d["ingreso_bruto"] - egresos
        if a == 3:
            neto += ct
        flujos.append(neto)
        detalle.append(d)
    return flujos, detalle, inv, ct


def van(tasa, flujos):
    return sum(f / (1 + tasa) ** t for t, f in enumerate(flujos))


def tir(flujos):
    if all(f <= 0 for f in flujos) or all(f >= 0 for f in flujos):
        return None
    lo, hi = -0.99, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if van(mid, flujos) > 0:
            lo = mid
        else:
            hi = mid
    return mid


def repago(flujos):
    acum = 0.0
    for t, f in enumerate(flujos):
        acum += f
        if t > 0 and acum >= 0:
            return t
    return None


def margen_por_pago(s: Supuestos):
    """Contribución mensual de un suscriptor una vez agotado el cupo gratuito de WhatsApp,
    incluidos los usuarios gratuitos activos que lo acompañan. No incluye la prueba,
    que depende de las altas y se trata como un costo de adquisición."""
    return s.precio * s.factor_precio_usd * (1 - s.comision_mp) - costo_var_por_pago(s)


def costo_var_por_pago(s: Supuestos):
    gratis_por_pago = (s.prop_activos - s.conversion) / s.conversion
    return (s.ia_premium * s.factor_ia
            + gratis_por_pago * s.ia_gratuito * s.factor_ia
            + (s.whatsapp_mensajes + s.whatsapp_plantillas) * s.whatsapp_msj)


def precio_equilibrio(s: Supuestos, pagos: float, con_fundador: bool):
    """Precio en USD que cubre los costos con una cantidad dada de suscriptores."""
    fijos = fijos_caja(s) + (fundador_mes(s) if con_fundador else 0)
    fijos += prueba_mensual(s) * s.ia_premium * s.factor_ia
    wa = costo_whatsapp(s, pagos + prueba_mensual(s))
    gratis = pagos * (s.prop_activos - s.conversion) / s.conversion
    var = pagos * s.ia_premium * s.factor_ia + gratis * s.ia_gratuito * s.factor_ia + wa
    return (fijos + var) / (pagos * (1 - s.comision_mp))


def equilibrio(s: Supuestos, con_fundador: bool, hasta: int = 5000):
    """Suscriptores que cubren los costos de un mes en régimen, aprovechando el cupo
    gratuito de WhatsApp e incluida la prueba de los usuarios nuevos."""
    prueba = prueba_mensual(s)
    for n in range(1, hasta):
        ingreso = n * s.precio * s.factor_precio_usd * (1 - s.comision_mp)
        gratis = n * (s.prop_activos - s.conversion) / s.conversion
        costo = (fijos_caja(s) + (fundador_mes(s) if con_fundador else 0)
                 + (n + prueba) * s.ia_premium * s.factor_ia + gratis * s.ia_gratuito * s.factor_ia
                 + costo_whatsapp(s, n + prueba))
        if ingreso >= costo:
            return n
    return None


def fijos_caja(s: Supuestos):
    return (s.ia_desarrollo * s.factor_ia + s.servidor + s.contador
            + s.monotributo + s.iibb + s.drei)


# --- Salida -----------------------------------------------------------------

def usd(x):
    if x is None:
        return "—"
    signo = "−" if x < 0 else ""
    entero, dec = f"{abs(x):,.0f}", ""
    return f"{signo}{entero.replace(',', '.')}{dec}"


def usd2(x):
    s = f"{abs(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + s


def pct(x):
    return "—" if x is None else f"{x * 100:.1f}%".replace(".", ",")


def tabla(encabezado, filas):
    out = ["| " + " | ".join(encabezado) + " |",
           "| " + " | ".join("---" for _ in encabezado) + " |"]
    out += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def escenarios():
    base = Supuestos()
    opt = replace(base, nombre="Optimista",
                  registrados_a1=tuple(round(r * 200 / 150) for r in base.registrados_a1),
                  pagos_a1=tuple(round(p * 200 / 150) for p in base.pagos_a1),
                  altas_anuales=300, conversion=0.07)
    pes_dem = replace(base, nombre="Pesimista 1: baja demanda",
                      registrados_a1=tuple(round(r * 100 / 150) for r in base.registrados_a1),
                      pagos_a1=tuple(redondear(0.021 * r * 100 / 150) for r in base.registrados_a1),
                      altas_anuales=100, conversion=0.021)
    pes_cos = replace(base, nombre="Pesimista 2: suba de costos y atraso del precio",
                      factor_ia=3.0, factor_precio_usd=0.8)
    return [opt, base, pes_dem, pes_cos]


def contingencia(s: Supuestos):
    """Precio del Premium de Gasti y tope de 60 respuestas mensuales por WhatsApp
    (el resto del uso premium sigue por Telegram y la web)."""
    return replace(s, nombre=f"Contingencia sobre {s.nombre.lower()}", precio=9.99, whatsapp_mensajes=60)


def main():
    s = Supuestos()
    filas = meses(s)

    print("## Costo de IA por usuario\n")
    print(tabla(["Concepto", "USD"], [
        ["Mensaje simple (Haiku 5.5)", f"{COSTO_MENSAJE:.4f}".replace(".", ",")],
        ["Operación compleja (Sonnet 5.5)", f"{COSTO_OPERACION:.4f}".replace(".", ",")],
        ["Audio de 30 s (Whisper)", f"{COSTO_AUDIO:.4f}".replace(".", ",")],
        ["Movimiento categorizado (Jev)", f"{COSTO_MOVIMIENTO_JEV:.6f}".replace(".", ",")],
        ["Usuario premium por mes", usd2(s.ia_premium)],
        ["Usuario gratuito activo por mes", usd2(s.ia_gratuito)],
    ]))

    print("\n## Usuarios y ingresos por trimestre\n")
    rows = []
    for q in range(12):
        bloque = filas[q * 3:(q + 1) * 3]
        rows.append([f"A{q // 4 + 1} T{q % 4 + 1}", usd(bloque[-1]["registrados"]),
                     usd(bloque[-1]["activos"]), bloque[-1]["pagos"],
                     usd(sum(f["ingreso_bruto"] for f in bloque)),
                     usd(sum(f["comision"] for f in bloque)),
                     usd(sum(f["ingreso_bruto"] - f["comision"] for f in bloque))])
    print(tabla(["Trimestre", "Registrados", "Activos", "Pagos", "Ingreso bruto", "Comisión MP", "Ingreso neto"], rows))
    print("\n## Usuarios al cierre de cada año\n")
    print(tabla(["Año", "Registrados", "Activos", "Suscriptores", "En prueba (activos)", "Gratuitos activos", "Suscriptores promedio"],
                [[a, usd(filas[a * 12 - 1]["registrados"]), usd(filas[a * 12 - 1]["activos"]), filas[a * 12 - 1]["pagos"],
                  usd2(filas[a * 12 - 1]["en_prueba"]), usd(filas[a * 12 - 1]["gratis_activos"]),
                  usd2(anual(filas, "pagos", a) / 12)] for a in (1, 2, 3)]))

    flujos, det, inv, ct = flujo(s)
    print("\n## Egresos anuales\n")
    conceptos = [("Servidor dedicado (fijo)", "servidor"), ("IA de desarrollo y pruebas (fijo)", "ia_desarrollo"),
                 ("IA por uso de suscriptores y gratuitos (variable)", "ia_variable"),
                 ("IA de la prueba gratuita (variable)", "ia_prueba"), ("WhatsApp (variable)", "whatsapp"),
                 ("Comisión de Mercado Pago (variable)", "comision"), ("Honorarios contables (fijo)", "contador"),
                 ("Monotributo (fijo)", "monotributo"), ("IIBB Santa Fe (fijo)", "iibb"), ("DReI Rosario (fijo)", "drei"),
                 ("Tiempo del fundador, imputado (fijo)", "fundador")]
    print(tabla(["Concepto", "Año 1", "Año 2", "Año 3"],
                [[n] + [usd(d[k]) for d in det] for n, k in conceptos]))

    print("\n## Inversión\n")
    print(tabla(["Rubro", "USD"], [[k, usd(v)] for k, v in inversion(s).items()] +
                [["Capital de trabajo (un mes de egresos de caja)", usd(ct)], ["Total", usd(inv + ct)]]))
    print(f"\nAmortización anual del intangible (3 años): {usd2(inv / 3)}")

    print("\n## Flujo de fondos\n")
    ingresos = [0] + [d["ingreso_bruto"] for d in det]
    print(tabla(["Concepto", "Año 0", "Año 1", "Año 2", "Año 3"], [
        ["Ingresos por suscripciones"] + [usd(x) for x in ingresos],
        ["Flujo neto"] + [usd(x) for x in flujos],
        ["Flujo acumulado"] + [usd(sum(flujos[:i + 1])) for i in range(4)],
    ]))
    f_sin, _, _, _ = flujo(s, incluir_fundador=False)
    print(f"\nTasa: {pct(s.tasa)} · VAN: {usd(van(s.tasa, flujos))} · TIR: {pct(tir(flujos))} · repago: {repago(flujos) or 'no se alcanza'}")
    print(f"Sin tiempo imputado: flujos {[usd(x) for x in f_sin]} · VAN {usd(van(s.tasa, f_sin))} · TIR {pct(tir(f_sin))}")

    m = margen_por_pago(s)
    print(f"\nMargen por suscriptor (sin cupo gratis de WhatsApp): {usd2(m)} · costo variable por suscriptor: {usd2(costo_var_por_pago(s))}")
    print(f"Fijos de caja: {usd2(fijos_caja(s))} · fundador: {usd2(fundador_mes(s))}")
    cupo = s.whatsapp_gratis * s.whatsapp_msj
    print(f"Cupo gratis de WhatsApp: {usd2(cupo)}/mes; margen dentro del cupo: {usd2(m + s.whatsapp_mensajes * s.whatsapp_msj)}")
    for n in (8, 23, 50, 100):
        print(f"Precio de equilibrio con {n} suscriptores: caja {usd2(precio_equilibrio(s, n, False))}, con tiempo {usd2(precio_equilibrio(s, n, True))}")
    n = equilibrio(s, False)
    print(f"Equilibrio de caja: {n} suscriptores" if n else "Equilibrio de caja: no se alcanza con menos de 5.000 suscriptores")
    print(f"Prueba: {usd2(prueba_mensual(s))} usuarios activos por mes en régimen")

    print("\n## Escenarios\n")
    rows = []
    for e in escenarios():
        fl, d, _, _ = flujo(e)
        fl_sin, _, _, _ = flujo(e, incluir_fundador=False)
        fin = meses(e)[-1]
        rows.append([e.nombre, usd(fin["registrados"]), fin["pagos"], usd(sum(x["ingreso_bruto"] for x in d)),
                     usd(van(e.tasa, fl)), pct(tir(fl)), usd(van(e.tasa, fl_sin)), pct(tir(fl_sin))])
    print(tabla(["Escenario", "Registrados año 3", "Pagos año 3", "Ingresos 3 años", "VAN", "TIR",
                 "VAN sin tiempo imputado", "TIR sin tiempo imputado"], rows))
    for e in escenarios():
        fl, _, _, _ = flujo(e)
        print(f"{e.nombre}: flujos {[usd(x) for x in fl]}; margen {usd2(margen_por_pago(e))}")

    print("\n## Plan de contingencia\n")
    rows = []
    for e in [contingencia(x) for x in escenarios()]:
        fl, d, _, _ = flujo(e)
        fl_sin, _, _, _ = flujo(e, incluir_fundador=False)
        rows.append([e.nombre, usd2(margen_por_pago(e)), usd(sum(x["ingreso_bruto"] for x in d)),
                     usd(van(e.tasa, fl)), usd(van(e.tasa, fl_sin)), [usd(x) for x in fl_sin]])
    print(tabla(["Escenario", "Margen por suscriptor", "Ingresos 3 años", "VAN", "VAN sin tiempo", "Flujos sin tiempo"], rows))
    c = contingencia(s)
    for con, texto in ((False, "Equilibrio de caja con contingencia"), (True, "Equilibrio con tiempo imputado y contingencia")):
        n = equilibrio(c, con)
        print(f"{texto}: {n} suscriptores ({n / c.conversion:.0f} registrados)" if n else f"{texto}: no se alcanza")

if __name__ == "__main__":
    main()
