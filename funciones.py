# funciones.py
import pandas as pd

def segmento_trl(nivel):
    if 1 <= nivel <= 3:
        return "TRL 1-3"
    elif 4 <= nivel <= 7:
        return "TRL 4-7"
    elif 8 <= nivel <= 9:
        return "TRL 8-9"
    return "Desconocido"

def calcular_puntajes_por_segmento(fila, diccionario):
    puntajes = {"TRL 1-3": 0, "TRL 4-7": 0, "TRL 8-9": 0}
    for pregunta, respuestas_map in diccionario.items():
        for columna, respuesta_usuario in fila.items():
            if respuesta_usuario in respuestas_map:
                datos = respuestas_map[respuesta_usuario]
                puntajes[datos["segmento"]] += datos["puntaje"]
    return puntajes
