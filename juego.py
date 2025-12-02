print("=== Juego: Tom y Jerry ===\n")
print("😺 Tom   vs   🐁 Jerry")

print("Controles:")
print("W,A,S,D = mover | k = salir\n")
# Aca hice una funcion que crea un tablero vacio de 9x9
def tablero_vacio():
    #Cada casilla se representa por un guion 
    return [['-' for _ in range(9)] for _ in range(9)]

# Aca hice una funcion que coloca obstaculos en el tablero que simulan paredes
def poner_obstaculos(tablero, lista_obstaculos):
    for fila, col in lista_obstaculos:
        tablero[fila][col] = '⬛'

# Aca hice una funcion que verifica si el movimiento es valido
def movimiento_valido(tablero, fila_nueva, colu_nueva):
    #usamos len para obtener el numero de filas y columnas del tablero
    filas = len(tablero)
    columnas = len(tablero[0])
    #aca verificamos si la nueva posicion esta dentro de los limites del tablero y no es un obstaculo
    if 0 <= fila_nueva < filas and 0 <= colu_nueva < columnas:
        #en esta parte verificamos que la casilla no sea un obstaculo
        if tablero[fila_nueva][colu_nueva] != '⬛':
            #este return indica que el movimiento es valido
            return True
        #y este return indica que el movimiento no es valido
    return False

#esta funcion calcula la distancia de "manhattan" entre dos posiciones
def calcular_distancia(pos1, pos2):

    #estos son las coordenadas de las dos posiciones que se pasan como argumentos
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#En esta parte hice una funcion que muestra el tablero en la consola
def mos_tablero(tablero): 
    
# Imprimi los numeros de las columnas
    print("  ",end="")

    #este for recorre las columnas del tablero
    for col in range(len(tablero[0])):
        print(col, end=" ")
    print()

# Este for recorre las filas del tablero y las enumera
    for n_fila, fila in enumerate(tablero):
        print(n_fila, end=" ")
        print(" ".join(fila))

def minimax(tablero, pos_tom, pos_jerry, mov_adelante, turno_de_jerry):
    if mov_adelante == 0:
        return calcular_distancia(pos_tom, pos_jerry)
    
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der

    if turno_de_jerry: 
        #a jerry le damos un valor inicial muy bajo para que luego pueda ir subiendolo
        mejor = -999
        for mov in movimientos:
            nueva_fila = pos_jerry[0] + mov[0]
            nueva_col = pos_jerry[1] + mov[1]
            if movimiento_valido(tablero, nueva_fila, nueva_col):
                valor = minimax(tablero, pos_tom, [nueva_fila, nueva_col], mov_adelante - 1, False)
                if valor > mejor:
                    mejor = valor
        return mejor
    else:
        #a tom le damos un valor muy alto para que luego pueda ir bajandolo
        mejor = 999
        for mov in movimientos:
            nueva_fila = pos_tom[0] + mov[0]
            nueva_col = pos_tom[1] + mov[1]
            if movimiento_valido(tablero, nueva_fila, nueva_col):
                valor = minimax(tablero, [nueva_fila, nueva_col], pos_jerry, mov_adelante - 1, True)
                if valor < mejor:
                    mejor = valor
        return mejor
    
def jerry_inteligente(tablero, pos_tom, pos_jerry):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    mejor_movimiento = None
    mejor_valor = -999

    for mov in movimientos: 
        fila_nueva = pos_jerry[0] + mov[0]
        colu_nueva = pos_jerry[1] + mov[1]

        if movimiento_valido(tablero, fila_nueva, colu_nueva):
            valor = minimax(tablero, pos_tom, [fila_nueva, colu_nueva], 3, False)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = [fila_nueva, colu_nueva]

                if mejor_movimiento:
                    tablero[pos_jerry[0]][pos_jerry[1]] = '-'
                    pos_jerry[0] = mejor_movimiento[0]
                    pos_jerry[1] = mejor_movimiento[1]
                    tablero[pos_jerry[0]][pos_jerry[1]] = '🐁' 
                    print(f"Jerry se movio a ({pos_jerry[0]}, {pos_jerry[1]})")


# Crear el tablero
tablero=tablero_vacio()

# Coloque algunos obstaculos en el tablero
poner_obstaculos(tablero, [(2, 2), (2, 3), (2, 4), (4, 5), (5, 5), (6, 5), (3,7), (1,6), (7,2), (5,1), (6,3), (4,2), (5,7), (1,2), (7,6), (0,5)])

pos_tom = [0, 0]  # Posición inicial de Tom
pos_jerry = [8, 8]  # Posición inicial de Jerry

tablero[pos_tom[0]][pos_tom[1]] = '😺'  # Posición de Tom
tablero[pos_jerry[0]][pos_jerry[1]] = '🐁'  # Posición de Jerry

#aca puse un contardor de turnos para que no sea largo el juego
turnos = 0
turnos_maximos = 30

# Bucle principal del juego
while True: 
    mos_tablero(tablero)
    tecla = input("Ingresa tu movimiento: ").lower()

#esto es si el jugador quiere salir del juego
    if tecla == 'k':    
        print("¡Has salido del juego!")
        break

#Tom se mueve segun la tecla ingresada 
    if tecla == 'w':
        fila_nueva = pos_tom[0] - 1
        colu_nueva = pos_tom[1]  
    elif tecla == 's':
        fila_nueva = pos_tom[0] + 1
        colu_nueva = pos_tom[1]
    elif tecla == 'a':
        fila_nueva = pos_tom[0]
        colu_nueva = pos_tom[1] - 1
    elif tecla == 'd':
        fila_nueva = pos_tom[0] 
        colu_nueva = pos_tom[1] + 1
    else:
        fila_nueva = pos_tom[0]
        colu_nueva = pos_tom[1]  

        #si la tecla no es valida, no se mueve
    if movimiento_valido(tablero, fila_nueva, colu_nueva):
        tablero[pos_tom[0]][pos_tom[1]] = '-'  # Limpiar la posición anterior
        pos_tom[0] = fila_nueva
        pos_tom[1] = colu_nueva
        tablero[pos_tom[0]][pos_tom[1]] = '😺'  # Actualizar la posición de Tom
    
        #aca suma un turno
        turnos += 1
        #aca muestra los turnos que tenes usando debugging f-string
        print(f"Te quedan{turnos=}/{turnos_maximos}")

        #aca se verifica si se acaban los turnos 
        if turnos >= turnos_maximos:
            print("Se acabo el tiempo, jerry gano!⏰")
            break
        jerry_inteligente(tablero, pos_tom, pos_jerry)
        
        #aca verifica si tom atrapo a jerry
        if pos_tom == pos_jerry:
            mos_tablero(tablero)
            print("Tom atrapo a jerry, Tom gana!🎉")
            break

        # Verificar de nuevo si Tom atrapó a Jerry después del movimiento de Jerry


# Mostre el tablero en la consola
mos_tablero(tablero)
