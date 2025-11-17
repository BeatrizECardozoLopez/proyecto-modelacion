
#heapq hace practicamente lo mismo que hicimos en el excel de revisar las rutas y actulizar para hayar la mas corta
import heapq

# Constructor de coordenadas para hacer mejor el sistema de coordenadas de bogota y todo lo que se quiera agregar
class coordenadas:
    def __init__(self,carrera,calle): # inicializa los objetos
        self.carrera = carrera
        self.calle = calle

    def __str__(self): # genera como debe verse el string a la hora de llamarlo
        return f"Carrera {self.carrera} con Calle {self.calle}"
        
    def __eq__(self, other): # compara referencias en memoria no contenido
        return self.carrera == other.carrera and self.calle == other.calle
        
    def __hash__(self): # esto nos permite usarlo en diccionarios
        return hash((self.carrera, self.calle))
    
    def __lt__(self, other): # nos permite evaluar cuando se encuentran dos rutas con el mismo costo hacia diferentes nodos
        if self.carrera != other.carrera:
            return self.carrera < other.carrera
        return self.calle < other.calle


# Coordenadas iniciales de Javier y Andreina
JAVIER = coordenadas(14, 54)
ANDREINA = coordenadas(13, 52)


# limites iniciales
x_min, x_max = 10, 15
y_min, y_max = 50, 55

# Se definieron funciones de costo tanto para calles horizontales como para carreras verticales
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

# Como se pueden añadir mas cosas se agrego una funcion para expandir los limites de la ciudad en caso de ser necesario
def expandir_limites(carrera, calle):
    """Expande los límites si es necesario para incluir nuevas coordenadas"""
    global x_min, x_max, y_min, y_max
    x_min = min(x_min, carrera)
    x_max = max(x_max, carrera)
    y_min = min(y_min, calle)
    y_max = max(y_max, calle)

# Funcion con el algoritmo de dijkstra para determinar el camino mas corto 
def dijkstra(origin):
    """Algoritmo de Dijkstra para encontrar el camino más corto"""
    dist = {} # almacena la distancia mínima conocida desde el origen hasta cada coordenada
    pred = {} # almacena la coordenada anterior para hacer el camino más corto
    
    # Inicializar distancias en infinito
    dist = {coordenadas(x, y): float('inf')
            for x in range(x_min, x_max + 1)
            for y in range(y_min, y_max + 1)}
    
    # el primer nodo no tiene predecesor en el camino mas corto
    pred = {coordenadas: None for coordenadas in dist}

    # distancia del origen al origen = 0
    dist[origin] = 0
    # tupla de distancia y coordenada para procesar el mas cercano primero
    heap = [(0, origin)]
   
    while heap:
        # extrae el nodo con la distancia minima
        d, u = heapq.heappop(heap)

        # verifica que la distancia en el heap coincida con la actual para saber si este nodo ya fue actualizado con una dist menor
        if d != dist[u]:
            continue
       
        # generacion de vecinos
        vecinos = []
        carrera, calle = u.carrera, u.calle # coordenadas actuales
       
        # verificación de límites para movimientos
        movimientos = [
            (carrera-1, calle),  # Este --> disminuye carrera
            (carrera+1, calle),  # Oeste  --> aumentra carrera
            (carrera, calle-1),  # Sur --> disminuye calle
            (carrera, calle+1)   # Norte --> aumenta calle
        ]
       
        for nueva_carrera, nueva_calle in movimientos:
            if x_min <= nueva_carrera <= x_max and y_min <= nueva_calle <= y_max:
                vecino = coordenadas(nueva_carrera, nueva_calle)
                # calculo de costo 
                if nueva_carrera != carrera:  # Movimiento horizontal entre carreras
                    costo = costo_h(calle)
                else:  # Movimiento vertical entre calles
                    costo = costo_v(carrera)
                # se guarda la nueva distancia tentativa
                new_d = d + costo


                # al encontrar un camino mas corto se actualiza
                if new_d < dist[vecino]:
                    dist[vecino] = new_d
                    pred[vecino] = u
                    heapq.heappush(heap, (new_d, vecino))
   
    return dist, pred

def get_path(dest, pred):
    """Reconstruye el camino desde el destino hasta el origen"""
    path = []
    current = dest
    # Sigue la cadena de predecesores hasta el origen
    while current is not None:
        path.append(current)
        current = pred[current]
    path.reverse() # se invierte el camino para tenerlo desde el origen hasta el destino
    return path

def mostrar_ruta(nombre, camino, tiempo):
    """Muestra una ruta de forma más legible"""
    print(f"\n=== Trayectoria para {nombre} ===")
    if camino:
        print("Ruta optimizada:")
        for i, coord in enumerate(camino):
            if i > 0:
                print(" -> ", end="")    
            print(f"   {coord}")
        print(f"Tiempo total: {tiempo} minutos")
    else:
        print("No se encontró ruta válida")

def mostrar_coordinacion(T_j, T_a, establecimiento_nombre):
    """Muestra información clara sobre la coordinación de tiempos"""
    print(f"\nCOORDINACIÓN PARA {establecimiento_nombre.upper()}")
    print("="*50)
   
    if T_j > T_a:
        diferencia = T_j - T_a
        print(f"Andreína debe esperar {diferencia} minutos")
        print(f"Javier sale primero (tarda {diferencia} minutos más)")
    elif T_a > T_j:
        diferencia = T_a - T_j
        print(f"Javier debe esperar {diferencia} minutos")  
        print(f"Andreína sale primero (tarda {diferencia} minutos más)")
    else:
        print("Ambos deben salir al mismo tiempo")
        print(f"Tiempos iguales: {T_j} minutos cada uno")


# Establecimientos iniciales
establecimientos = {
    "The Darkness": coordenadas(14, 50),
    "La Pasión": coordenadas(11, 54),
    "Mi Rolita": coordenadas(12, 50)
}

def agregar_establecimiento():
    """Permite agregar un nuevo establecimiento"""
    print("\n" + "="*40)
    print("\nAgregar nuevo establecimiento")
    print("="*40)
    
    nombre = input("Nombre del establecimiento: ").strip()

    # validaciones clasicas
    if not nombre:
        print("Error: El nombre no puede estar vacío")
        return None
   
    # validar que no exista ya el establecimiento
    if nombre in establecimientos:
        print(f"Error: Ya existe un establecimiento llamado '{nombre}'")
        
        return None
   
    try:
        carrera = int(input("Carrera: "))
        calle = int(input("Calle: "))
       
        # validación de rangos razonables
        if not (-100 <= carrera <= 100) or not (-100 <= calle <= 100):
            print("Error: Las coordenadas deben estar entre -100 y 100")
            return None
           
        # expandir límites si es necesario
        expandir_limites(carrera, calle)
       
        nuevo_establecimiento = coordenadas(carrera, calle)
        establecimientos[nombre] = nuevo_establecimiento
       
        print(f"Establecimiento '{nombre}' agregado exitosamente!")
        print(f"Ubicación: {nuevo_establecimiento}")
        print(f"Área de búsqueda actual: Carreras {x_min}-{x_max}, Calles {y_min}-{y_max}")

        
    except ValueError:
        print("Error: Debe ingresar números válidos")
        return None


def mostrar_establecimientos():
    """Muestra la lista de establecimientos disponibles"""
    print("\n" + "="*50)
    print("ESTABLECIMIENTOS DISPONIBLES")
    print("="*50)
   
    establecimientos_lista = list(establecimientos.keys())
   
    if not establecimientos_lista:
        print("No hay establecimientos registrados.")
    else:
        for i, nombre in enumerate(establecimientos_lista, 1):
            ubicacion = establecimientos[nombre]
            print(f"{i:2d}. {nombre:25} - {ubicacion}")

    # opciones del menu
    print(f"{len(establecimientos_lista) + 1:2d}. Agregar nuevo establecimiento")
    print(f"{len(establecimientos_lista) + 2:2d}. Salir del programa")


    return establecimientos_lista

def main():
    global x_min, x_max, y_min, y_max
    
    print("PLANIFICADOR DE ENCUENTROS SECRETOS")
    print("=" * 60)
    print(f"Ubicaciones iniciales:")
    print(f"Javier: {JAVIER}")
    print(f"Andreína: {ANDREINA}")
    print(f"Área de búsqueda inicial: Carreras {x_min}-{x_max}, Calles {y_min}-{y_max}")
    
    while True:
        establecimientos_lista = mostrar_establecimientos()
        
        try:
            opcion = int(input("\nSeleccione una opción (número): "))
            
            # Agregar nuevo establecimiento
            if opcion == len(establecimientos_lista) + 1:
                agregar_establecimiento()
                continue # se muestra el menu otra vez
            
            # Salir del programa
            elif opcion == len(establecimientos_lista) + 2:
                print("\nHasta luego!")
                return
            
            # Seleccionar establecimiento existente
            elif 1 <= opcion <= len(establecimientos_lista):
                establecimiento_nombre = establecimientos_lista[opcion - 1]
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Error: Debe ingresar un número válido")

    # obtenemos las coordenadas del establecimiento seleccionado
    destino = establecimientos[establecimiento_nombre]
    
    print(f"\nCalculando rutas hacia {establecimiento_nombre}...")
    # se ejecut el algortimo desde el destino 
    dist, pred = dijkstra(destino)
    
    # obtenemos los tiempos minimos de javier y andreina
    T_j = dist[JAVIER]
    T_a = dist[ANDREINA]
    
    # caminos optimos de javier y andreina
    path_j = get_path(JAVIER, pred)
    path_a = get_path(ANDREINA, pred)
    
    # invertir caminos para mostrar desde origen hasta destino
    camino_javier = path_j[::-1] if path_j else []
    camino_andreina = path_a[::-1] if path_a else []
    
    print(f"\n{'='*60}")
    print(f"RESULTADOS PARA: {establecimiento_nombre.upper()}")
    print(f"{'='*60}")
    
    # mostrar rutas para ambos
    mostrar_ruta("Javier", camino_javier, T_j)
    mostrar_ruta("Andreína", camino_andreina, T_a)
    
    # mostrar coordinación de tiempos para saber quien sale primero y cuando se espera
    if camino_javier and camino_andreina:
        mostrar_coordinacion(T_j, T_a, establecimiento_nombre)
    else:
        print("\nNo se pueden calcular los tiempos de encuentro")

if __name__ == "__main__":
    main()