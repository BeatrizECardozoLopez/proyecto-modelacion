import heapq

def costo_h(y):
    if y == 51:
        return 10
    else:
        return 5

def costo_v(x):
    if x in [11, 12, 13]:
        return 7
    else:
        return 5

x_min, x_max = 10, 15
y_min, y_max = 50, 55

def dijkstra(origin):
    dist = {}
    pred = {}
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
            if vx != x:
                costo = costo_h(y)
            else:
                costo = costo_v(x)
            new_d = d + costo
            if new_d < dist[v]:
                dist[v] = new_d
                pred[v] = u
                heapq.heappush(heap, (new_d, v))
    return dist, pred

def get_path(dest, pred):
    path = []
    current = dest
    while current is not None:
        path.append(current)
        current = pred[current]
    path.reverse()
    return path

javier = (14, 54)
andreina = (13, 52)

establecimientos = {
    "The Darkness": (14, 50),
    "La Pasion": (11, 54),
    "Mi Rolita": (12, 50)
}

def main():
    establecimiento_nombre = input("Ingrese el establecimiento destino (The Darkness, La Pasión, Mi Rolita): ").strip()
    if establecimiento_nombre not in establecimientos:
        print("Establecimiento no válido.")
        return
    
    destino = establecimientos[establecimiento_nombre]
    dist, pred = dijkstra(destino)
    
    T_j = dist[javier]
    T_a = dist[andreina]
    
    path_j = get_path(javier, pred)
    path_a = get_path(andreina, pred)
    
    camino_javier = path_j[::-1]  # Invertir para obtener desde Javier hasta el establecimiento
    camino_andreina = path_a[::-1]  # Invertir para obtener desde Andreína hasta el establecimiento
    
    print("\n--- Trayectoria para Javier ---")
    print("Trayectoria: ", end="")
    for i, (x, y) in enumerate(camino_javier):
        if i > 0:
            print(" -> ", end="")
        print(f"Calle {y} con Carrera {x}", end="")
    print(f"\nTiempo: {T_j} minutos")
    
    print("\n--- Trayectoria para Andreína ---")
    print("Trayectoria: ", end="")
    for i, (x, y) in enumerate(camino_andreina):
        if i > 0:
            print(" -> ", end="")
        print(f"Calle {y} con Carrera {x}", end="")
    print(f"\nTiempo: {T_a} minutos")
    
    if T_j > T_a:
        diferencia = T_j - T_a
        print(f"\nPara llegar simultáneamente, Javier debe salir {diferencia} minutos antes.")
    elif T_a > T_j:
        diferencia = T_a - T_j
        print(f"\nPara llegar simultáneamente, Andreína debe salir {diferencia} minutos antes.")
    else:
        print("\nAmbos deben salir al mismo tiempo.")

if __name__ == "__main__":
    main()