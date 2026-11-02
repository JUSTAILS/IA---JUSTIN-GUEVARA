from collections import deque
import time

estadoInicial = (3, 3, 1)  # [misioneros, canibales, barco a la izq]
estadoObjetivo = (0, 0, 0)  # [misioneros, canibales, barco a la der]

acciones = [
    (1, 0), # Mover 1 misionero
    (2, 0), # Mover 2 misioneros
    (0, 1), # Mover 1 canibal
    (0, 2), # Mover 2 canibales
    (1, 1)  # Mover 1 misionero y 1 canibal
]

def estado_valido(estado: tuple):

    misioneros_izq, canibales_izq, bote = estado
    # Validar límites
    if not (0 <= misioneros_izq <= 3 and 0 <= canibales_izq <= 3):
        return False
    # Validar posición del bote
    if bote not in (0, 1):
        return False
    # Cantidades en la derecha
    misioneros_der = 3 - misioneros_izq
    canibales_der = 3 - canibales_izq
    # Seguridad de la izquierda
    if misioneros_izq > 0 and misioneros_izq < canibales_izq:
        return False
    # Seguridad de la derecha
    if misioneros_der > 0 and misioneros_der < canibales_der:
        return False
    return True

def obtener_sucesores(estado):
    sucesores = []
    for accion in acciones:
        misionero, canibal = accion
        if estado[2] == 1:  # Bote a la izquierda
            # Comprobar disponibilidad
            if misionero > estado[0] or canibal > estado[1]:
                continue
            nuevo_estado = (
                estado[0] - misionero,
                estado[1] - canibal,
                0
            )
        else:  # Bote a la derecha
            # Comprobar disponibilidad
            if misionero > (3 - estado[0]) or canibal > (3 - estado[1]):
                continue
            nuevo_estado = (
                estado[0] + misionero,
                estado[1] + canibal,
                1
            )
        if estado_valido(nuevo_estado):
            sucesores.append(nuevo_estado)
    return sucesores
