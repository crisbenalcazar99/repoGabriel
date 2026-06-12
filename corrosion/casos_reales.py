"""
Datos preconfigurados para los dos casos reales de grúas torre en Guayaquil.
Se usan para pre-llenar el formulario con un solo clic.
"""

CASO_1 = {
    "nombre_activo": "Grúa Torre 1 — Obra Alborada, Guayaquil",
    "caso_numero": "1",
    "componente_eval": "pie_empotramiento",
    "material": "acero_carbono",
    "ambiente": "atmosferico_urbano_marino",
    "exposicion": "exterior_ciclos",
    "ubicacion_obra": "Guayaquil, Ecuador — zona urbana costera",
    "factores_ambientales": [
        "humedad_alta", "ambiente_marino", "cloruros",
        "polvo_cemento", "ciclos_humedo_seco", "recubrimiento_danado",
        "depositos", "zonas_ocluidas", "contacto_suelo",
    ],
    "morfologias": [
        "adelgazamiento_general", "hendidura", "bajo_depositos",
    ],
    "ubicaciones_dano": [
        "sup_horizontales", "soldaduras_zac", "tornillos_bridas", "interfase_suelo",
    ],
    "condiciones": [
        "cloruros_presentes", "diferencial_aireacion", "recubrimiento_poros",
        "bacteria_sulfatos",
    ],
    "dano_visual": "oxido_avanzado",
    "t_actual": 8.5,
    "t_minimo": 5.0,
    "cr": 0.18,
    "datos_estimados": True,
    "calidad_inspeccion": "visual_fotos",
    "cof_seguridad": "4",
    "cof_ambiental": "2",
    "cof_operativo": "4",
    "cof_costo": "3",
    "ph_medio": 7.2,
    "temperatura_op": 32.0,
    "cloruros_ppm": 180.0,
    "observaciones": (
        "La corrosión es visible principalmente en los primeros 15 m de altura. "
        "Por encima de esa cota casi no hay daño. Se atribuye a mayor exposición a polvo "
        "de cemento, humedad de la obra y contacto con concreto en la zona inferior. "
        "Pintura con pérdida de adherencia, ampollas y desprendimientos."
    ),
}

CASO_2 = {
    "nombre_activo": "Grúa Torre 4 — Obra Alborada, Guayaquil",
    "caso_numero": "2",
    "componente_eval": "pie_empotramiento",
    "material": "acero_carbono",
    "ambiente": "atmosferico_urbano_marino",
    "exposicion": "exterior_ciclos",
    "ubicacion_obra": "Guayaquil, Ecuador — zona urbana costera",
    "factores_ambientales": [
        "humedad_alta", "ambiente_marino", "cloruros",
        "polvo_cemento", "ciclos_humedo_seco", "recubrimiento_danado",
        "depositos", "zonas_ocluidas", "contacto_suelo", "contaminantes_so2",
    ],
    "morfologias": [
        "adelgazamiento_general", "picaduras", "hendidura",
        "bajo_depositos", "galvanica_contacto",
    ],
    "ubicaciones_dano": [
        "sup_horizontales", "soldaduras_zac", "tornillos_bridas",
        "interfase_suelo", "bajo_aislamiento",
    ],
    "condiciones": [
        "cloruros_presentes", "diferencial_aireacion", "recubrimiento_poros",
        "metales_disimiles", "anodo_pequeno", "bacteria_sulfatos",
    ],
    "dano_visual": "oxido_avanzado",
    "t_actual": 7.8,
    "t_minimo": 5.0,
    "cr": 0.22,
    "datos_estimados": True,
    "calidad_inspeccion": "visual_fotos",
    "cof_seguridad": "4",
    "cof_ambiental": "2",
    "cof_operativo": "4",
    "cof_costo": "3",
    "ph_medio": 6.9,
    "temperatura_op": 33.0,
    "cloruros_ppm": 230.0,
    "observaciones": (
        "Pintura amarilla deteriorada con pérdida de recubrimiento en bordes, uniones y zonas "
        "de contacto. Óxido rojizo/marrón avanzado en pernos, pasadores, placas laterales y "
        "perfiles estructurales. Se detectan indicios de picadura incipiente en placas. "
        "Posible corrosión galvánica en pernos/pasadores. Componente estructural crítico de grúa."
    ),
}