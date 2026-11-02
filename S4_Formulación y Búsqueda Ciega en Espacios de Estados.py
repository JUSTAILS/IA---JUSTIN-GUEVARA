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

def bfs(inicial, objetivo):

    cola = deque([inicial]) # Cola para BFS
    visitados = set([inicial]) # Conjunto para estados visitados
    padre = {inicial: None} # Diccionario para rastrear el camino
    nodos_expandidos = 0    
    while cola: # Mientras haya estados en la cola
        estado = cola.popleft() 
        if estado == objetivo:
            break
        nodos_expandidos += 1
        for sucesor in obtener_sucesores(estado): # Obtener sucesores del estado actual
            if sucesor not in visitados: # Si el sucesor no ha sido visitado
                visitados.add(sucesor)
                cola.append(sucesor)
                padre[sucesor] = estado
    existe_ruta = objetivo in padre # Verificar si se encontró una ruta al objetivo
    ruta = []
    if existe_ruta:
        actual = objetivo
        while actual is not None: # Reconstruir la ruta desde el objetivo hasta el inicio
            ruta.append(actual)
            actual = padre[actual]
        ruta.reverse()
    return existe_ruta, ruta, nodos_expandidos, len(visitados) # Retornar si existe ruta, la ruta encontrada, nodos expandidos y estados descubiertos

def dfs(inicio, objetivo):
    pila = [inicio] # Pila para DFS
    visitados = {inicio} # Conjunto para estados visitados
    padre = {inicio: None} # Diccionario para rastrear el camino
    nodos_expandidos = 0
    while pila: # Mientras haya estados en la pila
        estado = pila.pop()
        if estado == objetivo:
            break
        nodos_expandidos += 1
        for sucesor in obtener_sucesores(estado): # Obtener sucesores del estado actual
            if sucesor not in visitados: # Si el sucesor no ha sido visitado
                visitados.add(sucesor)
                pila.append(sucesor)
                padre[sucesor] = estado
    existe_ruta = objetivo in padre # Verificar si se encontró una ruta al objetivo
    ruta = []
    if existe_ruta:
        actual = objetivo
        while actual is not None: # Reconstruir la ruta desde el objetivo hasta el inicio
            ruta.append(actual)
            actual = padre[actual]
        ruta.reverse()
    return existe_ruta, ruta, nodos_expandidos, len(visitados) # Retornar si existe ruta, la ruta encontrada, nodos expandidos y estados descubiertos

def calcular_factor_ramificacion(nodos_descubiertos, profundidad):
    if nodos_descubiertos < 1 or profundidad < 0:
        return None
    if profundidad == 0:
        return None
    # Una ruta de profundidad d contiene al menos d+1 estados.
    if nodos_descubiertos < profundidad + 1:
        return None
    if nodos_descubiertos == profundidad + 1:
        return 1.0
    def suma_nodos(b):
        return sum(b ** nivel for nivel in range(profundidad + 1))
    # Límites iniciales de la búsqueda binaria.
    inferior = 1.0
    superior = 2.0
    # Ampliar el límite superior hasta encontrar el intervalo.
    while suma_nodos(superior) < nodos_descubiertos:
        superior *= 2
    # Aproximación del factor mediante búsqueda binaria.
    for _ in range(100):
        medio = (inferior + superior) / 2
        if suma_nodos(medio) < nodos_descubiertos:
            inferior = medio
        else:
            superior = medio
    return (inferior + superior) / 2

# Medición de tiempo y ejecución de BFS y DFS
inicio_bfs = time.perf_counter()
resultado_bfs = bfs(estadoInicial, estadoObjetivo)
fin_bfs = time.perf_counter()
tiempo_bfs = fin_bfs - inicio_bfs
factor_bfs = calcular_factor_ramificacion(
    resultado_bfs[3],
    len(resultado_bfs[1]) - 1
)

inicio_dfs = time.perf_counter()
resultado_dfs = dfs(estadoInicial, estadoObjetivo)
fin_dfs = time.perf_counter()
tiempo_dfs = fin_dfs - inicio_dfs
factor_dfs = calcular_factor_ramificacion(
    resultado_dfs[3],
    len(resultado_dfs[1]) - 1
)

# Resultados
print()
print("RESULTADOS BFS")
print("Tiempo:", tiempo_bfs, "segundos")
print("Longitud:", len(resultado_bfs[1]) - 1)
print("¿Existe ruta?:", resultado_bfs[0])
print("Ruta:", resultado_bfs[1])
print("Nodos expandidos:", resultado_bfs[2])
print("Estados descubiertos:", resultado_bfs[3])
print("Factor de ramificación efectivo:", 
      f"{factor_bfs:.6f}" if factor_bfs is not None else "No calculable")
print()
print("==============================================")
print()
print("\nRESULTADOS DFS")
print("Tiempo:", tiempo_dfs, "segundos")
print("Longitud:", len(resultado_dfs[1]) - 1)
print("¿Existe ruta?:", resultado_dfs[0])
print("Ruta:", resultado_dfs[1])
print("Nodos expandidos:", resultado_dfs[2])
print("Estados descubiertos:", resultado_dfs[3])
print("Factor de ramificación efectivo:", 
      f"{factor_dfs:.6f}" if factor_dfs is not None else "No calculable")