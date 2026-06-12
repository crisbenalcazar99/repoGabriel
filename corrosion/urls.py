from django.urls import path
from . import views

app_name = "corrosion"

urlpatterns = [
    path("", views.index, name="index"),
    path("evaluar/", views.evaluar, name="evaluar"),
    path("caso/<int:numero>/", views.cargar_caso, name="cargar_caso"),
]