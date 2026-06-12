from django import forms
from .engine import (MORFOLOGIAS, UBICACIONES, CONDICIONES, IF_TABLA,
                     FACTOR_AMBIENTAL, DANO_VISUAL_LABELS,
                     COF_SEGURIDAD_LABELS, COF_AMBIENTAL_LABELS,
                     COF_OPERATIVO_LABELS, COF_COSTO_LABELS)

MATERIAL_CHOICES = [
    ("", "— Seleccionar —"),
    ("acero_carbono", "Acero al carbono / acero estructural"),
    ("acero_inoxidable", "Acero inoxidable (304/316)"),
    ("acero_galvanizado", "Acero galvanizado"),
    ("acero_baja_aleacion", "Acero de baja aleación (ASTM A36/A572)"),
    ("hierro_fundido", "Hierro fundido"),
    ("aluminio", "Aluminio y aleaciones"),
    ("cobre_bronce", "Cobre / Bronce"),
    ("hormigon_armado", "Hormigón armado"),
    ("rodillo", "Rodillos"),
    ("valvula", "Válvulas"),
    ("otro", "Otro / Especificar en observaciones"),
]

COMPONENTE_CHOICES = [
    ("", "— Seleccionar —"),
    ("pie_empotramiento", "Pie de empotramiento / base estructural"),
    ("estructura_inferior", "Estructura inferior / tramo de torre"),
    ("placa_base", "Placa base / placa de apoyo"),
    ("perno_pasador", "Pernos, pasadores o tornillería"),
    ("union_soldada", "Uniones soldadas / cordones"),
    ("diagonal_montante", "Diagonal / montante / arriostramiento"),
    ("tuberia", "Tubería / ducto"),
    ("recipiente_presion", "Recipiente a presión / tanque"),
    ("intercambiador", "Intercambiador de calor"),
    ("bomba_impulsor", "Bomba / impulsor"),
    ("armadura_concreto", "Armadura embebida en concreto"),
    ("rodillos_valvulas", "Rodillos y Valvulas"),
    ("otro", "Otro / Especificar"),
]

AMBIENTE_CHOICES = [
    ("", "— Seleccionar —"),
    ("atmosferico_rural", "Atmosférico rural / bajo contaminante"),
    ("atmosferico_urbano", "Atmosférico urbano"),
    ("atmosferico_industrial", "Atmosférico industrial"),
    ("atmosferico_marino", "Atmosférico marino / costero"),
    ("atmosferico_urbano_marino", "Atmosférico urbano-marino (obra en ciudad costera)"),
    ("suelo", "Suelo / enterrado"),
    ("agua_dulce", "Agua dulce / río"),
    ("agua_mar", "Agua de mar"),
    ("fluido_proceso", "Fluido de proceso / producto industrial"),
    ("alta_temperatura", "Alta temperatura / gases calientes"),
]

EXPOSICION_CHOICES = [
    ("", "— Seleccionar —"),
    ("exterior_continua", "Exterior — exposición continua a intemperie"),
    ("exterior_ciclos", "Exterior — ciclos húmedo-seco frecuentes"),
    ("bajo_techo", "Bajo techo / ambiente cerrado"),
    ("enterrado", "Enterrado o en contacto con suelo / concreto"),
    ("sumergido", "Sumergido o en zona de salpicadura"),
    ("sumergido_continuo", "Sumergido — exposición continua"),
    ("aislado", "Bajo aislamiento térmico o recubrimiento"),
    ("interior_proceso", "Interior de proceso / fluido corrosivo"),
]

def _choices(d: dict):
    return [("", "— Seleccionar —")] + [(k, v) for k, v in d.items()]

def _multi_choices(d: dict):
    return [(k, v if isinstance(v, str) else v["label"]) for k, v in d.items()]


class CorrosionForm(forms.Form):
    # --- IDENTIFICACIÓN ---
    nombre_activo    = forms.CharField(label="Nombre del activo", max_length=200,
                                       widget=forms.TextInput(attrs={"placeholder": "Ej.: Grúa Torre 1 — Obra Alborada"}))
    caso_numero      = forms.ChoiceField(label="Número de caso",
                                         choices=[("1", "Caso 1"), ("2", "Caso 2")])
    componente_eval  = forms.ChoiceField(label="Componente evaluado", choices=COMPONENTE_CHOICES)
    material         = forms.ChoiceField(label="Material principal", choices=MATERIAL_CHOICES)
    ambiente         = forms.ChoiceField(label="Ambiente predominante", choices=AMBIENTE_CHOICES)
    exposicion       = forms.ChoiceField(label="Condición de exposición", choices=EXPOSICION_CHOICES)
    ubicacion_obra   = forms.CharField(label="Ubicación / ciudad / zona", max_length=200,
                                       required=False,
                                       widget=forms.TextInput(attrs={"placeholder": "Ej.: Guayaquil, Ecuador — zona costera"}))
    edad_equipo      = forms.FloatField(label="Edad del equipo / tiempo de servicio (años)",
                                        min_value=0, required=False,
                                        widget=forms.NumberInput(attrs={"step": "0.5", "placeholder": "Ej.: 3.5"}))
    evidencia_visual = forms.CharField(label="Evidencia visual observada",
                                       required=False,
                                       widget=forms.Textarea(attrs={"rows": 3,
                                                                     "placeholder": "Describa lo que se observó visualmente: colores, texturas, zonas afectadas, extensión del daño..."}))
    mecanismo_probable = forms.CharField(label="Mecanismo probable de corrosión observado o sospechoso",
                                         required=False,
                                         widget=forms.Textarea(attrs={"rows": 3,
                                                                       "placeholder": "Ej.: Se sospecha corrosión en hendidura bajo los pernos de anclaje combinada con corrosión bajo depósitos de cemento..."}))

    # --- FACTORES AMBIENTALES ---
    factores_ambientales = forms.MultipleChoiceField(
        label="Factores ambientales presentes (seleccione todos los que apliquen)",
        choices=_multi_choices(FACTOR_AMBIENTAL),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # --- MORFOLOGÍA ---
    morfologias = forms.MultipleChoiceField(
        label="Morfología del daño observada",
        choices=_multi_choices(MORFOLOGIAS),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # --- UBICACIÓN DEL DAÑO ---
    ubicaciones_dano = forms.MultipleChoiceField(
        label="Ubicación característica del daño",
        choices=_multi_choices(UBICACIONES),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # --- CONDICIONES ACELERANTES ---
    condiciones = forms.MultipleChoiceField(
        label="Condiciones que favorecen mecanismos específicos",
        choices=_multi_choices(CONDICIONES),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # --- DAÑO VISUAL GLOBAL ---
    dano_visual = forms.ChoiceField(
        label="Estado visual del daño (evaluación global)",
        choices=[("", "— Seleccionar —")] + [(k, v) for k, v in DANO_VISUAL_LABELS.items()],
    )

    # --- ESPESOR ---
    t_actual          = forms.FloatField(label="Espesor actual medido (mm)", min_value=0.01,
                                         widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "Ej.: 8.2"}))
    t_minimo          = forms.FloatField(label="Espesor mínimo permitido (mm)", min_value=0.01,
                                         widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "Ej.: 5.0"}))
    cr                = forms.FloatField(label="Velocidad de corrosión estimada (mm/año)", min_value=0.001,
                                         widget=forms.NumberInput(attrs={"step": "0.01", "placeholder": "Ej.: 0.15"}))
    datos_estimados   = forms.BooleanField(label="Los datos de espesor son estimados (no medidos con UT)",
                                           required=False)

    # --- CALIDAD DE INSPECCIÓN ---
    calidad_inspeccion = forms.ChoiceField(
        label="Calidad / tipo de inspección realizada",
        choices=[("", "— Seleccionar —")] + [(k, v["label"]) for k, v in IF_TABLA.items()],
    )

    # --- COF ---
    cof_seguridad  = forms.ChoiceField(
        label="Consecuencia — Seguridad de personas",
        choices=[("", "— Seleccionar —")] + [(str(k), v) for k, v in COF_SEGURIDAD_LABELS.items()],
    )
    cof_ambiental  = forms.ChoiceField(
        label="Consecuencia — Impacto ambiental",
        choices=[("", "— Seleccionar —")] + [(str(k), v) for k, v in COF_AMBIENTAL_LABELS.items()],
    )
    cof_operativo  = forms.ChoiceField(
        label="Consecuencia — Impacto operativo / productivo",
        choices=[("", "— Seleccionar —")] + [(str(k), v) for k, v in COF_OPERATIVO_LABELS.items()],
    )
    cof_costo      = forms.ChoiceField(
        label="Consecuencia — Costo de reparación o reemplazo",
        choices=[("", "— Seleccionar —")] + [(str(k), v) for k, v in COF_COSTO_LABELS.items()],
    )

    # --- DATOS OPCIONALES ---
    ph_medio          = forms.FloatField(label="pH del medio", required=False,
                                          widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "0–14"}))
    temperatura_op    = forms.FloatField(label="Temperatura de operación (°C)", required=False,
                                          widget=forms.NumberInput(attrs={"step": "1", "placeholder": "Ej.: 35"}))
    cloruros_ppm      = forms.FloatField(label="Cloruros (ppm o mg/L)", required=False,
                                          widget=forms.NumberInput(attrs={"step": "1", "placeholder": "Ej.: 200"}))
    velocidad_flujo   = forms.FloatField(label="Velocidad de flujo (m/s)", required=False,
                                          widget=forms.NumberInput(attrs={"step": "0.1"}))
    ecorr             = forms.FloatField(label="Potencial Ecorr / estructura-electrolito (mV)", required=False,
                                          widget=forms.NumberInput(attrs={"step": "1"}))
    resistividad      = forms.FloatField(label="Resistividad del suelo/electrolito (Ω·cm)", required=False,
                                          widget=forms.NumberInput(attrs={"step": "1"}))

    observaciones     = forms.CharField(label="Observaciones libres", required=False,
                                         widget=forms.Textarea(attrs={"rows": 4,
                                                                       "placeholder": "Describa condiciones adicionales, hallazgos de inspección o antecedentes relevantes..."}))

    def clean(self):
        cleaned = super().clean()
        t_actual  = cleaned.get("t_actual")
        t_minimo  = cleaned.get("t_minimo")
        if t_actual and t_minimo and t_actual < t_minimo:
            self.add_error("t_actual",
                           "El espesor actual es menor que el mínimo. El componente está en estado crítico. Verifique los valores.")
        return cleaned