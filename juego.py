print("😺 Tom   vs   🐁 Jerry")
print("W,A,S,D = mover | k = salir\n")

def tablero_vacio(): # Esta función arma un tablero vacío de 9x9 para jugar
    return [['-' for _ in range(9)] for _ in range(9)] # Hace una lista de listas donde cada casillita tiene un guion "-"

def poner_obstaculos(tablero, lista_obstaculos): # Esta función agarra el tablero y le pone paredes donde le digas
    for fila, col in lista_obstaculos: # Recorre cada posición de pared que le pasaste
        tablero[fila][col] = '⬛' # Pone un cuadrado negro en esa posición

def movimiento_valido(tablero, fila_nueva, colu_nueva): # Esta función se fija si te podés mover a donde querés o no
    filas = len(tablero) # Cuenta cuántas filas tiene el tablero
    columnas = len(tablero[0]) # Cuenta cuántas columnas tiene el tablero
    if 0 <= fila_nueva < filas and 0 <= colu_nueva < columnas: # Se fija que no te salgas del tablero
        if tablero[fila_nueva][colu_nueva] != '⬛': # Se fija que no haya una pared ahí
            return True # Devuelve True si podés moverte
    return False # Devuelve False si no podés moverte

def calcular_distancia(pos1, pos2): # Esta función calcula qué tan lejos están Tom y Jerry
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) # Suma la diferencia de filas y columnas para saber la distancia

def mos_tablero(tablero): # Esta función muestra el tablero en la consola
    for col in range(len(tablero[0])): # Imprime los números de las columnas arriba
        print(col, end=" ")
    print()
    for n_fila, fila in enumerate(tablero): # Recorre cada fila del tablero
        print(n_fila, end=" ") # Imprime el número de fila al costado
        print(" ".join(fila)) # Imprime toda la fila junta

def minimax(tablero, pos_tom, pos_jerry, mov_adelante, turno_de_jerry): # Esta función hace que Jerry piense sus movimientos para alejarse de Tom
    if mov_adelante == 0: # Cuando ya no quedan mas movimientos que simular lo que hace es 
        return calcular_distancia(pos_tom, pos_jerry) # Devuelve la distancia entre Tom y Jerry
    
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lista de movimientos posibles: arriba, abajo, izquierda, derecha

    if turno_de_jerry: # Si es el turno de Jerry
        mejor = -999 # Le damos un valor inicial muy bajo para que lo vaya mejorando
        for mov in movimientos: # Prueba cada movimiento posible
            nueva_fila = pos_jerry[0] + mov[0] # Calcula la nueva fila
            nueva_col = pos_jerry[1] + mov[1] # Calcula la nueva columna
            if movimiento_valido(tablero, nueva_fila, nueva_col): # Si el movimiento es válido
                valor = minimax(tablero, pos_tom, [nueva_fila, nueva_col], mov_adelante - 1, False) # Calcula recursivamente el valor del movimiento
                if valor > mejor: # Si encontró un mejor movimiento
                    mejor = valor # Guarda ese valor
        return mejor # Devuelve el mejor valor encontrado
    else: # Si es el turno de Tom
        mejor = 999 # Le damos un valor inicial muy alto para que lo vaya bajando
        for mov in movimientos: # Prueba cada movimiento posible
            nueva_fila = pos_tom[0] + mov[0] # Calcula la nueva fila
            nueva_col = pos_tom[1] + mov[1] # Calcula la nueva columna
            if movimiento_valido(tablero, nueva_fila, nueva_col): # Si el movimiento es válido
                valor = minimax(tablero, [nueva_fila, nueva_col], pos_jerry, mov_adelante - 1, True) # Calcula recursivamente el valor del movimiento
                if valor < mejor: # Si encontró un mejor movimiento
                    mejor = valor # Guarda ese valor
        return mejor # Devuelve el mejor valor encontrado
    
def jerry_inteligente(tablero, pos_tom, pos_jerry): # Esta función mueve a Jerry automáticamente usando la lógica del minimax
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lista de movimientos posibles
    mejor_movimiento = None # Inicializa el mejor movimiento como None
    mejor_valor = -999 # Inicializa el mejor valor con un número bien bajo

    for mov in movimientos: # Prueba cada movimiento
        fila_nueva = pos_jerry[0] + mov[0] # Calcula la nueva fila
        colu_nueva = pos_jerry[1] + mov[1] # Calcula la nueva columna

        if movimiento_valido(tablero, fila_nueva, colu_nueva): # Si el movimiento es válido
            valor = minimax(tablero, pos_tom, [fila_nueva, colu_nueva], 3, False) # Evalúa el movimiento mirando 3 turnos adelante

            if valor > mejor_valor: # Si este movimiento es mejor que el anterior
                mejor_valor = valor # Guarda el nuevo mejor valor
                mejor_movimiento = [fila_nueva, colu_nueva] # Guarda el nuevo mejor movimiento

                if mejor_movimiento: # Si encontró un movimiento válido
                    tablero[pos_jerry[0]][pos_jerry[1]] = '-' # Borra a Jerry de su posición actual
                    pos_jerry[0] = mejor_movimiento[0] # Actualiza la fila de Jerry
                    pos_jerry[1] = mejor_movimiento[1] # Actualiza la columna de Jerry
                    tablero[pos_jerry[0]][pos_jerry[1]] = '🐁' # Pone a Jerry en su nueva posición
                    print(f"Jerry se movio a ({pos_jerry[0]}, {pos_jerry[1]})") # Avisa a dónde se movió Jerry

tablero=tablero_vacio() # Crea el tablero vacío

poner_obstaculos(tablero, [(2, 2), (2, 3), (2, 4), (4, 5), (5, 5), (6, 5), (3,7), (1,6), (7,2), (5,1), (6,3), (4,2), (5,7), (1,2), (7,6), (0,5)]) # Pone las paredes en el tablero

pos_tom = [0, 0] # Posición inicial de Tom en la esquina superior izquierda
pos_jerry = [8, 8] # Posición inicial de Jerry en la esquina inferior derecha

tablero[pos_tom[0]][pos_tom[1]] = '😺' # Pone a Tom en el tablero
tablero[pos_jerry[0]][pos_jerry[1]] = '🐁' # Pone a Jerry en el tablero

turnos = 0 # Contador de turnos empieza en 0
turnos_maximos = 30 # El juego dura máximo 30 turnos

while True: # Bucle infinito del juego hasta que alguien gane o salgas
    mos_tablero(tablero) # Muestra el tablero actualizado
    tecla = input("Ingresa tu movimiento: ").lower() # Pide al jugador que ingrese un movimiento y lo convierte a minúscula

    if tecla == 'k': # Si presionás K
        print("¡Has salido del juego!") # Avisa que saliste
        break # Sale del bucle y termina el juego

    if tecla == 'w': # Si presionás W
        fila_nueva = pos_tom[0] - 1 # Tom se mueve para arriba
        colu_nueva = pos_tom[1]
    elif tecla == 's': # Si presionás S
        fila_nueva = pos_tom[0] + 1 # Tom se mueve para abajo
        colu_nueva = pos_tom[1]
    elif tecla == 'a': # Si presionás A
        fila_nueva = pos_tom[0] # Tom se mueve para la izquierda
        colu_nueva = pos_tom[1] - 1
    elif tecla == 'd': # Si presionás D
        fila_nueva = pos_tom[0] # Tom se mueve para la derecha
        colu_nueva = pos_tom[1] + 1
    else: # Si presionás cualquier otra tecla
        fila_nueva = pos_tom[0] # Tom se queda donde está
        colu_nueva = pos_tom[1]

    if movimiento_valido(tablero, fila_nueva, colu_nueva): # Si el movimiento que querés hacer es válido
        tablero[pos_tom[0]][pos_tom[1]] = '-' # Borra a Tom de su posición anterior
        pos_tom[0] = fila_nueva # Actualiza la fila de Tom
        pos_tom[1] = colu_nueva # Actualiza la columna de Tom
        tablero[pos_tom[0]][pos_tom[1]] = '😺' # Pone a Tom en su nueva posición
    
        turnos += 1 # Suma un turno
        print(f"Te quedan{turnos=}/{turnos_maximos}") # Muestra cuántos turnos quedan

        if turnos >= turnos_maximos: # Si se acabaron los turnos
            print("Se acabo el tiempo, jerry gano!⏰") # Jerry gana por tiempo
            break # Termina el juego
        jerry_inteligente(tablero, pos_tom, pos_jerry) # Jerry se mueve automáticamente
        
        if pos_tom == pos_jerry: # Si Tom y Jerry están en la misma posición
            mos_tablero(tablero) # Muestra el tablero final
            print("Tom atrapo a jerry, Tom gana!🎉") # Tom gana
            break # Termina el juego

mos_tablero(tablero) # Muestra el tablero final cuando termina el juego
