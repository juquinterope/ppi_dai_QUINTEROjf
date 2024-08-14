# import os
# import geopandas as gpd # type: ignore
# from django.http import JsonResponse
from django.shortcuts import render
# from django.conf import settings


def planear_viaje(request):
    return render(request, 'planeacion/planear_viaje.html')
