"""
Motor de cálculo técnico para el Estimador de Corrosión.
Implementa: severidad ambiental, diagnóstico, ME, VR, IF, PoF, CoF y riesgo.
"""

# ---------------------------------------------------------------------------
# SEVERIDAD AMBIENTAL
# ---------------------------------------------------------------------------

FACTOR_AMBIENTAL = {
    "humedad_alta":        {"peso": 2, "label": "Humedad alta / lluvia frecuente"},
    "ambiente_marino":     {"peso": 3, "label": "Ambiente marino / salino"},
    "cloruros":            {"peso": 3, "label": "Presencia de cloruros"},
    "polvo_cemento":       {"peso": 2, "label": "Polvo de cemento / concreto"},
    "ciclos_humedo_seco":  {"peso": 2, "label": "Ciclos húmedo-seco frecuentes"},
    "recubrimiento_danado":{"peso": 3, "label": "Recubrimiento dañado o ausente"},
    "depositos":           {"peso": 2, "label": "Acumulación de depósitos / lodos"},
    "zonas_ocluidas":      {"peso": 2, "label": "Zonas ocluidas / hendiduras"},
    "contacto_suelo":      {"peso": 2, "label": "Contacto con suelo o concreto"},
    "temperatura_alta":    {"peso": 1, "label": "Temperatura de operación elevada (>60 °C)"},
    "contaminantes_so2":   {"peso": 1, "label": "Contaminantes industriales / SO₂"},
    "h2s_acidos":          {"peso": 2, "label": "H₂S, ácidos u otros agresivos"},
    "cascarilla_particulas":{"peso": 2, "label": "Cascarilla de laminación o partículas metálicas"},
}

def calcular_severidad_ambiental(factores_activos: list[str]) -> dict:
    """
    factores_activos: lista de claves de FACTOR_AMBIENTAL seleccionadas.
    Retorna: {"score": int, "nivel": str, "iso_categoria": str}
    """
    score = sum(FACTOR_AMBIENTAL[f]["peso"] for f in factores_activos if f in FACTOR_AMBIENTAL)
    max_score = sum(v["peso"] for v in FACTOR_AMBIENTAL.values())
    pct = score / max_score if max_score else 0

    if pct < 0.20:
        nivel, iso = "Baja", "C1-C2"
    elif pct < 0.40:
        nivel, iso = "Media", "C2-C3"
    elif pct < 0.60:
        nivel, iso = "Alta", "C3-C4"
    elif pct < 0.80:
        nivel, iso = "Muy Alta", "C4-C5"
    else:
        nivel, iso = "Extrema", "C5-CX"

    return {"score": score, "max_score": max_score, "porcentaje": round(pct * 100, 1),
            "nivel": nivel, "iso_categoria": iso}


# ---------------------------------------------------------------------------
# DIAGNÓSTICO DE MECANISMO
# ---------------------------------------------------------------------------

MORFOLOGIAS = {
    "adelgazamiento_general":   "Adelgazamiento generalizado / óxidos extendidos",
    "picaduras":                "Picaduras profundas o hemiesféricas",
    "hendidura":                "Ataque en rendijas, juntas, solapes, empaques, bajo tornillos",
    "bajo_depositos":           "Ataque bajo depósitos, lodos, incrustaciones o sedimentos",
    "galvanica_contacto":       "Ataque cerca de unión entre metales / contacto eléctrico",
    "erosion_surcos":           "Surcos, ranuras, dirección del flujo, forma de herradura",
    "cavitacion":               "Cráteres por cavitación o impacto de burbujas",
    "desgaste_contacto":        "Desgaste por contacto, vibración o movimiento relativo",
    "grietas_ramificadas":      "Grietas ramificadas o intergranulares (SCC / IGC)",
    "grietas_finas":            "Grietas finas con poca deformación plástica (HE / SCC)",
    "ampollas":                 "Ampollas, laminaciones, abultamientos o fisuración interna (HIC)",
    "ataque_limites_grano":     "Ataque preferente en límites de grano / ZAC",
    "exfoliacion":              "Exfoliación",
    "color_cobreoso":           "Color rojizo/cobreoso o pérdida selectiva de fase",
    "cascarilla_alta_temp":     "Cascarilla, óxidos adheridos, sulfuros a alta temperatura",
    "biopelícula":              "Biopelícula, limo, depósitos negros, olor sulfuroso (MIC)",
    "fisuras_concreto":         "Fisuras o armadura expuesta en concreto armado",
    "erosion_abrasiva":         "Erosión — pérdida de material por partículas, abrasión o impacto",
}

UBICACIONES = {
    "sup_horizontales":         "Superficies horizontales / fondos con acumulación",
    "soldaduras_zac":           "Soldaduras, ZAC o cordones",
    "tornillos_bridas":         "Tornillos, bridas, empaques o remaches",
    "codos_cambios":            "Codos, reducciones, tees o cambios de dirección",
    "impulsores_bombas":        "Impulsores, bombas, válvulas o boquillas",
    "linea_agua":               "Línea de agua, salpicadura o zona de marea",
    "bajo_aislamiento":         "Bajo aislamiento, chaquetas o recubrimientos dañados",
    "interfase_suelo":          "Interfase suelo-aire, fondo de tanque o tubería enterrada",
    "zona_traccion":            "Zona bajo tracción, flexión, presión cíclica o vibración",
    "zona_caliente":            "Zona calentada, quemadores, hornos o gases calientes",
    "armadura_concreto":        "Armadura embebida en hormigón",
}

CONDICIONES = {
    "cloruros_presentes":       "Cloruros, agua de mar, salmueras o hipoclorito",
    "ph_bajo":                  "Medio ácido o pH bajo (< 6)",
    "ph_alto":                  "Medio alcalino fuerte (pH > 10)",
    "diferencial_aireacion":    "Diferencias de aireación, zonas ocluidas o estancamiento",
    "metales_disimiles":        "Metales disímiles en contacto eléctrico",
    "anodo_pequeno":            "Ánodo pequeño acoplado a cátodo grande",
    "recubrimiento_poros":      "Recubrimiento con poros, daños o discontinuidades",
    "alta_velocidad":           "Alta velocidad, turbulencia, sólidos o gotas impactando",
    "cargas_ciclicas":          "Cargas cíclicas, vibración, fatiga o presión pulsante",
    "esfuerzo_traccion":        "Esfuerzo de tracción, residual, soldadura o formado en frío",
    "h2s_hidrogeno":            "H₂S, ácido, decapado, soldadura — posible hidrógeno",
    "sensibilizacion_termica":  "Sensibilización térmica en inoxidables / tratamiento inadecuado",
    "bacteria_sulfatos":        "Agua estancada, bacterias, sulfatos, ambiente anaerobio (MIC)",
    "carbonatacion_concreto":   "Carbonatación o cloruros en concreto armado",
    "oxigeno_azufre_alta_temp": "Oxígeno, azufre, vanadio, sales fundidas, gases calientes",
}

MECANISMOS = {
    "corrosion_uniforme": {
        "nombre": "Corrosión Uniforme / Atmosférica",
        "desc": "Pérdida de material distribuida sobre la superficie expuesta, favorecida por humedad, oxígeno y contaminantes.",
        "morfologias_clave": ["adelgazamiento_general"],
        "condiciones_clave": ["diferencial_aireacion", "recubrimiento_poros"],
        "ubicaciones_clave": ["sup_horizontales", "bajo_aislamiento"],
        "mitigacion": ["Sistema de recubrimiento anticorrosivo", "Control de humedad y limpieza periódica",
                       "Inhibidores de corrosión en medio"],
    },
    "corrosion_picadura": {
        "nombre": "Corrosión por Picaduras (Pitting)",
        "desc": "Ataque localizado muy agresivo, genera cavidades profundas. Favorecido por cloruros y ruptura de película pasiva.",
        "morfologias_clave": ["picaduras"],
        "condiciones_clave": ["cloruros_presentes", "ph_bajo"],
        "ubicaciones_clave": ["sup_horizontales"],
        "mitigacion": ["Eliminar cloruros del medio", "Acero inoxidable de mayor aleación o aleaciones resistentes",
                       "Inspección periódica con UT para detección temprana"],
    },
    "corrosion_hendidura": {
        "nombre": "Corrosión en Hendidura (Crevice)",
        "desc": "Ataque intenso en espacios confinados donde el electrolito queda atrapado y el oxígeno se agota.",
        "morfologias_clave": ["hendidura"],
        "condiciones_clave": ["diferencial_aireacion", "cloruros_presentes"],
        "ubicaciones_clave": ["tornillos_bridas", "soldaduras_zac"],
        "mitigacion": ["Sellado de hendiduras con sellante compatible", "Diseño sin huecos ni solapas",
                       "Drenaje de líquidos estancados"],
    },
    "corrosion_galvanica": {
        "nombre": "Corrosión Galvánica",
        "desc": "Par galvánico entre metales disímiles: el más anódico se corroe preferentemente.",
        "morfologias_clave": ["galvanica_contacto"],
        "condiciones_clave": ["metales_disimiles", "anodo_pequeno", "cloruros_presentes"],
        "ubicaciones_clave": ["tornillos_bridas"],
        "mitigacion": ["Separar metales con aislamiento eléctrico", "Seleccionar metales compatibles en la serie galvánica",
                       "Protección catódica o anodos de sacrificio"],
    },
    "erosion_corrosion": {
        "nombre": "Erosión-Corrosión",
        "desc": "Sinergia entre ataque electroquímico y desgaste mecánico por flujo de alta velocidad, sólidos o turbulencia.",
        "morfologias_clave": ["erosion_surcos"],
        "condiciones_clave": ["alta_velocidad"],
        "ubicaciones_clave": ["codos_cambios", "impulsores_bombas"],
        "mitigacion": ["Reducir velocidad de flujo", "Materiales resistentes a erosión",
                       "Recubrimientos duros o revestimientos"],
    },
    "cavitacion": {
        "nombre": "Cavitación",
        "desc": "Colapso de burbujas de vapor cerca de la superficie metálica genera impactos de alta presión.",
        "morfologias_clave": ["cavitacion"],
        "condiciones_clave": ["alta_velocidad"],
        "ubicaciones_clave": ["impulsores_bombas"],
        "mitigacion": ["Rediseño hidráulico para evitar zonas de baja presión",
                       "Materiales de alta dureza", "Recubrimientos elastoméricos"],
    },
    "corrosion_bajo_tension": {
        "nombre": "Corrosión Bajo Tensión (SCC)",
        "desc": "Fisuración intergranular o transgranular bajo esfuerzo de tracción en medio corrosivo específico.",
        "morfologias_clave": ["grietas_ramificadas", "grietas_finas"],
        "condiciones_clave": ["esfuerzo_traccion", "cloruros_presentes", "ph_alto"],
        "ubicaciones_clave": ["soldaduras_zac", "zona_traccion"],
        "mitigacion": ["Alivio de tensiones residuales (PWHT)", "Cambio de material",
                       "Eliminación del agente agresivo"],
    },
    "dano_hidrogeno": {
        "nombre": "Daño por Hidrógeno (HE / HIC / SOHIC)",
        "desc": "Absorción de hidrógeno atómico que fragiliza el acero o genera ampollas internas.",
        "morfologias_clave": ["ampollas", "grietas_finas"],
        "condiciones_clave": ["h2s_hidrogeno", "ph_bajo"],
        "ubicaciones_clave": ["soldaduras_zac"],
        "mitigacion": ["Aceros resistentes a HIC (NACE MR0175)", "Control de pH > 5.5",
                       "Eliminación o reducción de H₂S"],
    },
    "mic": {
        "nombre": "Corrosión Microbiológica (MIC)",
        "desc": "Bacterias reductoras de sulfatos (SRB) u otras producen metabolitos agresivos bajo biopelícula.",
        "morfologias_clave": ["biopelícula", "bajo_depositos"],
        "condiciones_clave": ["bacteria_sulfatos"],
        "ubicaciones_clave": ["sup_horizontales", "interfase_suelo"],
        "mitigacion": ["Biocidas periódicos", "Limpieza mecánica / hidrodinámica",
                       "Drenaje completo de fluidos estancados"],
    },
    "corrosion_intergranular": {
        "nombre": "Corrosión Intergranular / Sensibilización",
        "desc": "Ataque preferente en límites de grano por empobrecimiento de Cr en inoxidables sensibilizados.",
        "morfologias_clave": ["ataque_limites_grano", "exfoliacion"],
        "condiciones_clave": ["sensibilizacion_termica"],
        "ubicaciones_clave": ["soldaduras_zac"],
        "mitigacion": ["Solución de recocido", "Aceros con bajo carbono (304L/316L)",
                       "Tratamiento térmico post-soldadura adecuado"],
    },
    "corrosion_alta_temperatura": {
        "nombre": "Corrosión a Alta Temperatura / Oxidación",
        "desc": "Reacción directa con oxígeno, azufre u otros gases a temperatura elevada.",
        "morfologias_clave": ["cascarilla_alta_temp"],
        "condiciones_clave": ["oxigeno_azufre_alta_temp"],
        "ubicaciones_clave": ["zona_caliente"],
        "mitigacion": ["Aleaciones resistentes a alta temperatura", "Recubrimientos cerámicos o difusión",
                       "Control de atmósfera"],
    },
    "bajo_depositos": {
        "nombre": "Corrosión Bajo Depósitos (Under-Deposit)",
        "desc": "La acumulación de sólidos crea celdas de aireación diferencial y atrapa humedad agresiva.",
        "morfologias_clave": ["bajo_depositos"],
        "condiciones_clave": ["diferencial_aireacion", "depositos"],
        "ubicaciones_clave": ["sup_horizontales", "bajo_aislamiento"],
        "mitigacion": ["Limpieza regular de depósitos", "Diseño con drenaje libre",
                       "Recubrimientos resistentes bajo depósitos"],
    },
}

def diagnosticar_mecanismo(morfologias: list[str], ubicaciones: list[str], condiciones: list[str]) -> dict:
    puntajes = {}
    for key, m in MECANISMOS.items():
        score = 0
        score += sum(3 for morf in m["morfologias_clave"] if morf in morfologias)
        score += sum(2 for cond in m["condiciones_clave"] if cond in condiciones)
        score += sum(1 for ub in m["ubicaciones_clave"] if ub in ubicaciones)
        if score > 0:
            puntajes[key] = score

    if not puntajes:
        return {
            "principal": None,
            "nombre_principal": "Indeterminado — datos insuficientes",
            "confianza": "Baja",
            "justificacion": "No se identificaron indicadores suficientes. Ampliar inspección.",
            "secundarios": [],
            "mitigacion": [],
        }

    ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    principal_key, principal_score = ordenados[0]
    max_posible = (3 * len(MECANISMOS[principal_key]["morfologias_clave"]) +
                   2 * len(MECANISMOS[principal_key]["condiciones_clave"]) +
                   1 * len(MECANISMOS[principal_key]["ubicaciones_clave"]))
    max_posible = max(max_posible, 1)
    confianza_pct = min(principal_score / max_posible * 100, 100)

    if confianza_pct >= 70:
        confianza = "Alta"
    elif confianza_pct >= 40:
        confianza = "Media"
    else:
        confianza = "Baja"

    secundarios = [{"key": k, "nombre": MECANISMOS[k]["nombre"], "score": s}
                   for k, s in ordenados[1:4] if s > 0]

    return {
        "principal": principal_key,
        "nombre_principal": MECANISMOS[principal_key]["nombre"],
        "confianza": confianza,
        "confianza_pct": round(confianza_pct, 1),
        "justificacion": MECANISMOS[principal_key]["desc"],
        "secundarios": secundarios,
        "mitigacion": MECANISMOS[principal_key]["mitigacion"],
    }


# ---------------------------------------------------------------------------
# MARGEN DE ESPESOR Y VIDA REMANENTE
# ---------------------------------------------------------------------------

def calcular_espesor_vida(t_actual: float, t_minimo: float, cr: float, datos_estimados: bool) -> dict:
    errores = []
    advertencias = []

    if t_actual <= 0:
        errores.append("El espesor actual debe ser mayor que 0.")
    if t_minimo <= 0:
        errores.append("El espesor mínimo debe ser mayor que 0.")
    if cr <= 0:
        errores.append("La velocidad de corrosión debe ser mayor que 0.")
    if t_actual <= t_minimo and not errores:
        advertencias.append("ALERTA: El espesor actual es <= al espesor mínimo. El componente puede estar fuera de servicio.")

    if errores:
        return {"errores": errores}

    ME = round(t_actual - t_minimo, 3)
    VR = round(ME / cr, 2) if ME > 0 else 0.0

    if datos_estimados:
        advertencias.append(
            "Resultado PRELIMINAR — espesor estimado. Requiere medición por ultrasonido (UT) para confirmar."
        )
    if VR < 1:
        advertencias.append("ALERTA CRÍTICA: Vida remanente < 1 año. Acción inmediata requerida.")
    elif VR < 3:
        advertencias.append("ALERTA: Vida remanente < 3 años. Planificar intervención a corto plazo.")

    return {
        "ME": ME,
        "VR": VR,
        "t_actual": t_actual,
        "t_minimo": t_minimo,
        "cr": cr,
        "advertencias": advertencias,
        "errores": [],
    }


# ---------------------------------------------------------------------------
# FACTOR DE INSPECCIÓN (IF)
# ---------------------------------------------------------------------------

IF_TABLA = {
    "visual_solo":          {"IF": 1.5, "label": "Inspección visual únicamente"},
    "visual_fotos":         {"IF": 1.25, "label": "Visual + registro fotográfico"},
    "visual_ut_parcial":    {"IF": 1.0,  "label": "Visual + ultrasonido (UT) parcial"},
    "ut_completo":          {"IF": 0.7,  "label": "UT completo o NDT confiable"},
    "inspeccion_completa":  {"IF": 0.5,  "label": "Inspección interna/externa completa y documentada"},
}

def obtener_IF(calidad_inspeccion: str) -> dict:
    if calidad_inspeccion not in IF_TABLA:
        return {"IF": 1.5, "label": "Desconocido — se asume inspección visual", "advertencia": True}
    entry = IF_TABLA[calidad_inspeccion]
    return {"IF": entry["IF"], "label": entry["label"], "advertencia": False}


# ---------------------------------------------------------------------------
# POF — PROBABILIDAD DE FALLA (1-5)
# ---------------------------------------------------------------------------

PESO_POF = {
    "severidad":    0.25,
    "dano_visual":  0.20,
    "vr_score":     0.20,
    "me_score":     0.15,
    "mecanismo":    0.10,
    "if_score":     0.10,
}

SEVERIDAD_SCORE = {"Baja": 1, "Media": 2, "Alta": 3, "Muy Alta": 4, "Extrema": 5}

DANO_VISUAL_SCORE = {
    "sin_dano":          1,
    "pintura_deteriorada": 2,
    "oxido_superficial": 3,
    "oxido_avanzado":    4,
    "perdida_seccion":   5,
}

DANO_VISUAL_LABELS = {
    "sin_dano":          "Sin daño visible",
    "pintura_deteriorada": "Pintura deteriorada / burbujas",
    "oxido_superficial": "Óxido superficial / herrumbre leve",
    "oxido_avanzado":    "Óxido avanzado / pérdida de recubrimiento significativa",
    "perdida_seccion":   "Pérdida de sección visible / perforación",
}

MECANISMO_SCORE = {
    "corrosion_uniforme":       2,
    "bajo_depositos":           2,
    "corrosion_picadura":       4,
    "corrosion_hendidura":      3,
    "corrosion_galvanica":      3,
    "erosion_corrosion":        3,
    "cavitacion":               4,
    "corrosion_bajo_tension":   5,
    "dano_hidrogeno":           5,
    "mic":                      3,
    "corrosion_intergranular":  4,
    "corrosion_alta_temperatura": 3,
}

def calcular_pof(severidad_nivel: str, dano_visual: str, vr: float, me: float,
                 mecanismo_key: str, if_valor: float) -> dict:
    s_sev   = SEVERIDAD_SCORE.get(severidad_nivel, 3)
    s_dano  = DANO_VISUAL_SCORE.get(dano_visual, 3)

    # VR -> score inverso (< vida = mayor PoF)
    if vr <= 0:
        s_vr = 5
    elif vr < 1:
        s_vr = 5
    elif vr < 3:
        s_vr = 4
    elif vr < 7:
        s_vr = 3
    elif vr < 15:
        s_vr = 2
    else:
        s_vr = 1

    # ME -> score inverso
    if me <= 0:
        s_me = 5
    elif me < 1:
        s_me = 4
    elif me < 3:
        s_me = 3
    elif me < 6:
        s_me = 2
    else:
        s_me = 1

    s_mec = MECANISMO_SCORE.get(mecanismo_key, 3)

    # IF alto -> mayor incertidumbre -> mayor PoF
    if if_valor >= 1.5:
        s_if = 5
    elif if_valor >= 1.25:
        s_if = 4
    elif if_valor >= 1.0:
        s_if = 3
    elif if_valor >= 0.7:
        s_if = 2
    else:
        s_if = 1

    raw = (s_sev  * PESO_POF["severidad"]  +
           s_dano * PESO_POF["dano_visual"] +
           s_vr   * PESO_POF["vr_score"]   +
           s_me   * PESO_POF["me_score"]   +
           s_mec  * PESO_POF["mecanismo"]  +
           s_if   * PESO_POF["if_score"])

    pof = max(1, min(5, round(raw)))

    labels = {1: "Muy Baja", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy Alta"}
    return {
        "PoF": pof,
        "label": labels[pof],
        "detalle": {"severidad": s_sev, "dano_visual": s_dano, "vr": s_vr,
                    "me": s_me, "mecanismo": s_mec, "if": s_if, "raw": round(raw, 2)},
    }


# ---------------------------------------------------------------------------
# COF — CONSECUENCIA DE FALLA (1-5)
# ---------------------------------------------------------------------------

COF_SEGURIDAD_LABELS = {
    1: "Sin riesgo personal",
    2: "Lesiones leves posibles",
    3: "Lesiones graves posibles",
    4: "Fatalidad posible / evacuación",
    5: "Múltiples fatalidades / colapso estructural",
}
COF_AMBIENTAL_LABELS = {
    1: "Sin impacto ambiental",
    2: "Impacto local leve",
    3: "Impacto local significativo",
    4: "Derrame / contaminación mayor",
    5: "Desastre ambiental",
}
COF_OPERATIVO_LABELS = {
    1: "Sin pérdida operativa",
    2: "Parada < 8 h",
    3: "Parada 8-72 h",
    4: "Parada > 3 días",
    5: "Pérdida total del activo",
}
COF_COSTO_LABELS = {
    1: "< $1,000",
    2: "$1,000 – $10,000",
    3: "$10,000 – $100,000",
    4: "$100,000 – $1,000,000",
    5: "> $1,000,000",
}

def calcular_cof(seg: int, amb: int, oper: int, costo: int) -> dict:
    # CoF = máximo de las categorías (enfoque conservador)
    cof = max(seg, amb, oper, costo)
    labels = {1: "Muy Baja", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy Alta"}
    return {
        "CoF": cof,
        "label": labels[cof],
        "detalle": {
            "seguridad": seg, "ambiental": amb, "operativo": oper, "costo": costo
        },
    }


# ---------------------------------------------------------------------------
# RIESGO Y MATRIZ
# ---------------------------------------------------------------------------

def calcular_riesgo(pof: int, cof: int) -> dict:
    riesgo = pof * cof
    if riesgo <= 4:
        nivel, color = "Bajo",    "green"
    elif riesgo <= 9:
        nivel, color = "Medio",   "yellow"
    elif riesgo <= 16:
        nivel, color = "Alto",    "orange"
    else:
        nivel, color = "Crítico", "red"
    return {"riesgo": riesgo, "nivel": nivel, "color": color, "pof": pof, "cof": cof}


# ---------------------------------------------------------------------------
# CONCLUSIÓN AUTOMÁTICA
# ---------------------------------------------------------------------------

ACCIONES_BASE = [
    "Inspección visual detallada con registro fotográfico.",
    "Medición de espesores por ultrasonido (UT) en zonas críticas.",
    "Limpieza mecánica o abrasiva del óxido existente.",
    "Preparación superficial según norma aplicable (SSPC / ISO 8501).",
    "Verificación de sales solubles antes de pintar (máx. 20 µg/cm² Cl⁻).",
    "Control de punto de rocío y humedad relativa antes de aplicar recubrimiento.",
    "Aplicación de primario anticorrosivo de alta adherencia.",
    "Capa intermedia de alta impedancia eléctrica si aplica.",
    "Capa final barrera resistente a intemperie.",
    "Revisión de pernos, pasadores, soldaduras y placas.",
    "Sellado de hendiduras donde se acumule humedad.",
    "Evitar acumulación de polvo de cemento y depósitos.",
    "Programa de inspección cada 3-6 meses según nivel de criticidad.",
]

def generar_conclusion(activo: str, componente: str, material: str, diagnostico: dict,
                       espesor: dict, severidad: dict, riesgo: dict) -> str:
    nivel_riesgo = riesgo["nivel"]
    vr_txt = f"{espesor.get('VR', '?')} años" if espesor.get("VR") is not None else "indeterminada"
    me_txt = f"{espesor.get('ME', '?')} mm" if espesor.get("ME") is not None else "indeterminado"

    accion_urgente = ""
    if nivel_riesgo == "Crítico":
        accion_urgente = " DETENER OPERACIÓN y realizar evaluación estructural inmediata."
    elif nivel_riesgo == "Alto":
        accion_urgente = " Planificar intervención en el corto plazo (< 3 meses)."

    texto = (
        f"El activo evaluado ({activo} — {componente}) corresponde a {material} expuesto a ambiente "
        f"de severidad {severidad['nivel']} (categoría ISO {severidad['iso_categoria']}). "
        f"El mecanismo de corrosión principal diagnosticado es '{diagnostico['nombre_principal']}' "
        f"(confianza: {diagnostico.get('confianza', 'Media')}). "
        f"El margen de espesor calculado es {me_txt} y la vida remanente estimada es {vr_txt}. "
        f"La probabilidad de falla (PoF) se clasifica en nivel {riesgo['pof']} y la consecuencia de "
        f"falla (CoF) en nivel {riesgo['cof']}, resultando en un riesgo {nivel_riesgo} "
        f"(score RBI = {riesgo['riesgo']})."
        f"{accion_urgente}"
    )
    return texto