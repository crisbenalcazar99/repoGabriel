from django.shortcuts import render, redirect
from .forms import CorrosionForm
from .casos_reales import CASO_1, CASO_2
from .engine import (
    calcular_severidad_ambiental, diagnosticar_mecanismo,
    calcular_espesor_vida, obtener_IF, calcular_pof,
    calcular_cof, calcular_riesgo, generar_conclusion, ACCIONES_BASE,
)


def index(request):
    return render(request, "corrosion/index.html")


def cargar_caso(request, numero):
    datos = CASO_1 if numero == 1 else CASO_2
    request.session["caso_precargado"] = datos
    return redirect("corrosion:evaluar")


def evaluar(request):
    caso_precargado = request.session.pop("caso_precargado", None)
    initial = caso_precargado or {}
    form = CorrosionForm(initial=initial)
    resultado = None

    if request.method == "POST":
        form = CorrosionForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            severidad = calcular_severidad_ambiental(d["factores_ambientales"])

            diagnostico = diagnosticar_mecanismo(
                d["morfologias"],
                d["ubicaciones_dano"],
                d["condiciones"],
            )

            espesor = calcular_espesor_vida(
                d["t_actual"], d["t_minimo"], d["cr"], d["datos_estimados"]
            )

            inspeccion = obtener_IF(d["calidad_inspeccion"])

            vr_val = espesor.get("VR", 0) or 0
            me_val = espesor.get("ME", 0) or 0
            pof_result = calcular_pof(
                severidad_nivel=severidad["nivel"],
                dano_visual=d["dano_visual"],
                vr=vr_val,
                me=me_val,
                mecanismo_key=diagnostico.get("principal") or "corrosion_uniforme",
                if_valor=inspeccion["IF"],
            )

            cof_result = calcular_cof(
                seg=int(d["cof_seguridad"]),
                amb=int(d["cof_ambiental"]),
                oper=int(d["cof_operativo"]),
                costo=int(d["cof_costo"]),
            )

            riesgo = calcular_riesgo(pof_result["PoF"], cof_result["CoF"])

            conclusion = generar_conclusion(
                activo=d["nombre_activo"],
                componente=d["componente_eval"],
                material=d["material"],
                diagnostico=diagnostico,
                espesor=espesor,
                severidad=severidad,
                riesgo=riesgo,
            )

            matriz = _construir_matriz(pof_result["PoF"], cof_result["CoF"])

            resultado = {
                "form_data": d,
                "caso_label": f"Caso {d['caso_numero']}",
                "severidad": severidad,
                "diagnostico": diagnostico,
                "espesor": espesor,
                "inspeccion": inspeccion,
                "pof": pof_result,
                "cof": cof_result,
                "riesgo": riesgo,
                "conclusion": conclusion,
                "acciones": ACCIONES_BASE,
                "matriz": matriz,
            }

    return render(request, "corrosion/evaluar.html", {"form": form, "resultado": resultado})


def _construir_matriz(pof_actual: int, cof_actual: int) -> list:
    def color(pof, cof):
        r = pof * cof
        if r <= 4:
            return "bg-success text-white"
        elif r <= 9:
            return "bg-warning text-dark"
        elif r <= 16:
            return "bg-orange text-white"
        else:
            return "bg-danger text-white"

    filas = []
    for pof in range(5, 0, -1):
        celdas = []
        for cof in range(1, 6):
            r = pof * cof
            es_actual = (pof == pof_actual and cof == cof_actual)
            celdas.append({"valor": r, "clase": color(pof, cof), "es_actual": es_actual})
        filas.append({"pof": pof, "celdas": celdas})
    return filas