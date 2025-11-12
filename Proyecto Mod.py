
#CON LIMITE DE CALLES Y CARRERAS
# import heapq

# def costo_h(y):
#     if y == 51:
#         return 10
#     else:
#         return 5

# def costo_v(x):
#     if x in [11, 12, 13]:
#         return 7
#     else:
#         return 5

# x_min, x_max = 10, 15
# y_min, y_max = 50, 55

# def dijkstra(origin):
#     dist = {}
#     pred = {}
#     for x in range(x_min, x_max + 1):
#         for y in range(y_min, y_max + 1):
#             dist[(x, y)] = float('inf')
#             pred[(x, y)] = None
#     dist[origin] = 0
#     heap = [(0, origin)]
#     while heap:
#         d, u = heapq.heappop(heap)
#         if d != dist[u]:
#             continue
#         x, y = u
#         vecinos = []
#         if x > x_min:
#             vecinos.append((x - 1, y))  # este
#         if x < x_max:
#             vecinos.append((x + 1, y))  # oeste
#         if y > y_min:
#             vecinos.append((x, y - 1))  # sur
#         if y < y_max:
#             vecinos.append((x, y + 1))  # norte
#         for v in vecinos:
#             vx, vy = v
#             if vx != x:
#                 costo = costo_h(y)
#             else:
#                 costo = costo_v(x)
#             new_d = d + costo
#             if new_d < dist[v]:
#                 dist[v] = new_d
#                 pred[v] = u
#                 heapq.heappush(heap, (new_d, v))
#     return dist, pred

# def get_path(dest, pred):
#     path = []
#     current = dest
#     while current is not None:
#         path.append(current)
#         current = pred[current]
#     path.reverse()
#     return path

# javier = (14, 54)
# andreina = (13, 52)

# establecimientos = {
#     "The Darkness": (14, 50),
#     "La Pasión": (11, 54),
#     "Mi Rolita": (12, 50)
# }

# def agregar_establecimiento():
#     print("\n--- Agregar nuevo establecimiento ---")
#     nombre = input("Nombre del establecimiento: ").strip()
    
#     try:
#         carrera = int(input("Carrera (10-15): "))
#         calle = int(input("Calle (50-55): "))
        
#         if carrera < 10 or carrera > 15 or calle < 50 or calle > 55:
#             print("Error: La carrera debe estar entre 10-15 y la calle entre 50-55")
#             return None
#         else:
#             establecimientos[nombre] = (carrera, calle)
#             print(f"Establecimiento '{nombre}' agregado exitosamente!")
#             return nombre
#     except ValueError:
#         print("Error: Debe ingresar números válidos")
#         return None

# def mostrar_establecimientos():
#     print("\n--- Establecimientos disponibles ---")
#     establecimientos_lista = list(establecimientos.keys())
#     for i, nombre in enumerate(establecimientos_lista, 1):
#         carrera, calle = establecimientos[nombre]
#         print(f"{i}. {nombre} - Carrera {carrera} con Calle {calle}")
#     print(f"{len(establecimientos_lista) + 1}. Agregar nuevo establecimiento")
#     return establecimientos_lista

# def main():
#     while True:
#         establecimientos_lista = mostrar_establecimientos()
        
#         try:
#             opcion = int(input("\nSeleccione el establecimiento destino (número): "))
            
#             if opcion == len(establecimientos_lista) + 1:
#                 agregar_establecimiento()
#                 continue
#             elif 1 <= opcion <= len(establecimientos_lista):
#                 establecimiento_nombre = establecimientos_lista[opcion - 1]
#                 break
#             else:
#                 print("Opción no válida. Intente nuevamente.")
#         except ValueError:
#             print("Error: Debe ingresar un número válido")
    
#     destino = establecimientos[establecimiento_nombre]
#     dist, pred = dijkstra(destino)
    
#     T_j = dist[javier]
#     T_a = dist[andreina]
    
#     path_j = get_path(javier, pred)
#     path_a = get_path(andreina, pred)
    
#     camino_javier = path_j[::-1]
#     camino_andreina = path_a[::-1]
    
#     print(f"\n--- Trayectoria para Javier hacia {establecimiento_nombre} ---")
#     print("Trayectoria: ", end="")
#     for i, (x, y) in enumerate(camino_javier):
#         if i > 0:
#             print(" -> ", end="")
#         print(f"Calle {y} con Carrera {x}", end="")
#     print(f"\nTiempo: {T_j} minutos")
    
#     print(f"\n--- Trayectoria para Andreína hacia {establecimiento_nombre} ---")
#     print("Trayectoria: ", end="")
#     for i, (x, y) in enumerate(camino_andreina):
#         if i > 0:
#             print(" -> ", end="")
#         print(f"Calle {y} con Carrera {x}", end="")
#     print(f"\nTiempo: {T_a} minutos")
    
#     if T_j > T_a:
#         diferencia = T_j - T_a
#         print(f"\nPara llegar simultáneamente, Andreína debe esperar {diferencia} minutos (Javier sale primero).")
#     elif T_a > T_j:
#         diferencia = T_a - T_j
#         print(f"\nPara llegar simultáneamente, Javier debe esperar {diferencia} minutos (Andreína sale primero).")
#     else:
#         print("\nAmbos deben salir al mismo tiempo.")

# if __name__ == "__main__":
#     main()



#MAS FLEXIBLE Y FUERA DE LA ZONA DELIMITADA:


import heapq

# Coordenadas iniciales de Javier y Andreína
JAVIER = (14, 54)
ANDREINA = (13, 52)

# Límites originales del problema, pero ahora expandibles
x_min, x_max = 10, 15
y_min, y_max = 50, 55

def costo_h(y):
    """Costo horizontal (calles)"""
    if y == 51:
        return 10  
    else:
        return 5  

def costo_v(x):
    """Costo vertical (carreras)"""
    if x in [11, 12, 13]:
        return 7  
    else:
        return 5 

def expandir_limites(carrera, calle):
    """Expande los límites si es necesario para incluir nuevas coordenadas"""
    global x_min, x_max, y_min, y_max
    x_min = min(x_min, carrera)
    x_max = max(x_max, carrera)
    y_min = min(y_min, calle)
    y_max = max(y_max, calle)

def dijkstra(origin):
    """Algoritmo de Dijkstra para encontrar el camino más corto"""
    dist = {}
    pred = {}
    
    # Inicializar distancias
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            dist[(x, y)] = float('inf')
            pred[(x, y)] = None
    
    dist[origin] = 0
    heap = [(0, origin)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        
        x, y = u
        vecinos = []
        
        # Movimientos posibles: norte, sur, este, oeste
        if x > x_min:
            vecinos.append((x - 1, y))  # este
        if x < x_max:
            vecinos.append((x + 1, y))  # oeste
        if y > y_min:
            vecinos.append((x, y - 1))  # sur
        if y < y_max:
            vecinos.append((x, y + 1))  # norte
        
        for v in vecinos:
            vx, vy = v
            # Determinar si es movimiento horizontal o vertical
            if vx != x:  # Movimiento horizontal (cambio de carrera)
                costo = costo_h(y)
            else:  # Movimiento vertical (cambio de calle)
                costo = costo_v(x)
            
            new_d = d + costo
            if new_d < dist[v]:
                dist[v] = new_d
                pred[v] = u
                heapq.heappush(heap, (new_d, v))
    
    return dist, pred

def get_path(dest, pred):
    """Reconstruye el camino desde el destino hasta el origen"""
    path = []
    current = dest
    while current is not None:
        path.append(current)
        current = pred[current]
    path.reverse()
    return path

# Establecimientos iniciales
establecimientos = {
    "The Darkness": (14, 50),
    "La Pasión": (11, 54),
    "Mi Rolita": (12, 50)
}

def agregar_establecimiento():
    """Permite al usuario agregar un nuevo establecimiento"""
    print("\n--- Agregar nuevo establecimiento ---")
    nombre = input("Nombre del establecimiento: ").strip()
    
    try:
        carrera = int(input("Carrera: "))
        calle = int(input("Calle: "))
        
        # Expandir límites si es necesario
        expandir_limites(carrera, calle)
        
        establecimientos[nombre] = (carrera, calle)
        print(f"Establecimiento '{nombre}' agregado exitosamente en Carrera {carrera} con Calle {calle}!")
        print(f"Área de búsqueda expandida: Carreras {x_min}-{x_max}, Calles {y_min}-{y_max}")
        return nombre
        
    except ValueError:
        print("Error: Debe ingresar números válidos")
        return None

def mostrar_establecimientos():
    """Muestra la lista de establecimientos disponibles"""
    print("\n--- Establecimientos disponibles ---")
    establecimientos_lista = list(establecimientos.keys())
    for i, nombre in enumerate(establecimientos_lista, 1):
        carrera, calle = establecimientos[nombre]
        print(f"{i}. {nombre} - Carrera {carrera} con Calle {calle}")
    print(f"{len(establecimientos_lista) + 1}. Agregar nuevo establecimiento")
    return establecimientos_lista

def main():
    global x_min, x_max, y_min, y_max
    
    print("=== PLANIFICADOR DE ENCUENTROS SECRETOS ===")
    print(f"Ubicaciones iniciales:")
    print(f"  - Javier: Carrera {JAVIER[0]} con Calle {JAVIER[1]}")
    print(f"  - Andreína: Carrera {ANDREINA[0]} con Calle {ANDREINA[1]}")
    print(f"Área de búsqueda inicial: Carreras {x_min}-{x_max}, Calles {y_min}-{y_max}")
    
    while True:
        establecimientos_lista = mostrar_establecimientos()
        
        try:
            opcion = int(input("\nSeleccione el establecimiento destino (número): "))
            
            if opcion == len(establecimientos_lista) + 1:
                agregar_establecimiento()
                continue
            elif 1 <= opcion <= len(establecimientos_lista):
                establecimiento_nombre = establecimientos_lista[opcion - 1]
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Error: Debe ingresar un número válido")
    
    destino = establecimientos[establecimiento_nombre]
    
    print(f"\nCalculando rutas hacia {establecimiento_nombre}...")
    dist, pred = dijkstra(destino)
    
    T_j = dist[JAVIER]
    T_a = dist[ANDREINA]
    
    path_j = get_path(JAVIER, pred)
    path_a = get_path(ANDREINA, pred)
    
    # Invertir caminos para mostrar desde origen hasta destino
    camino_javier = path_j[::-1] if path_j else []
    camino_andreina = path_a[::-1] if path_a else []
    
    print(f"\n=== RESULTADOS PARA {establecimiento_nombre.upper()} ===")
    
    print(f"\n--- Trayectoria para Javier ---")
    if camino_javier:
        print("Ruta: ", end="")
        for i, (x, y) in enumerate(camino_javier):
            if i > 0:
                print(" -> ", end="")
            print(f"Carrera {x} con Calle {y}", end="")
        print(f"\nTiempo total: {T_j} minutos")
    else:
        print("No se encontró ruta válida")
    
    print(f"\n--- Trayectoria para Andreína ---")
    if camino_andreina:
        print("Ruta: ", end="")
        for i, (x, y) in enumerate(camino_andreina):
            if i > 0:
                print(" -> ", end="")
            print(f"Carrera {x} con Calle {y}", end="")
        print(f"\nTiempo total: {T_a} minutos")
    else:
        print("No se encontró ruta válida")
    
    # Coordenadas de destino para verificación
    print(f"\nDestino: Carrera {destino[0]} con Calle {destino[1]}")
    
    if camino_javier and camino_andreina:
        if T_j > T_a:
            diferencia = T_j - T_a
            print(f"\n💡 Para llegar simultáneamente:")
            print(f"   Andreína debe esperar {diferencia} minutos")
            print(f"   (Javier sale primero y tarda {diferencia} minutos más)")
        elif T_a > T_j:
            diferencia = T_a - T_j
            print(f"\n💡 Para llegar simultáneamente:")
            print(f"   Javier debe esperar {diferencia} minutos")
            print(f"   (Andreína sale primero y tarda {diferencia} minutos más)")
        else:
            print(f"\n💡 Ambos deben salir al mismo tiempo")
            print(f"   (Tiempos iguales: {T_j} minutos cada uno)")
    else:
        print("\n❌ No se pueden calcular los tiempos de encuentro")

if __name__ == "__main__":
    main()