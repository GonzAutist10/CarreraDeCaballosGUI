import Baraja


def clear():
    for i in range(50):
        print()


def pedir_jugadores():
    for i in range(4):
        print("Nombres de los jugadores que han apostado a " + palos[i] + ":")
        while True:
            jugador = input()
            if jugador == '':
                break
            jugadores[i].append(jugador)


def final():
    if palo in ["oros", "bastos"]:
        print("\n\033[1m\033[4mHan ganado los " + palo + "!\033[0m\n")
    else:
        print("\n\033[1m\033[4mHan ganado las " + palo + "!\033[0m\n")

    print("Jugadores que mandan beber el doble de tragos que apostaron:")
    for jugador in jugadores[num]:
        print(jugador)


def retroceso(x):
    print("\n\033[1mTodos los caballos han alcanzado la posición " + str(x) + "\033[0m")
    carta = cartas_retroceso.pop()
    print("Carta de retroceso: " + carta)
    palo = carta.split()[2]
    num = palos.index(palo)
    posicion_nueva = caballos[num] - 1
    caballos[num] = posicion_nueva
    print("Jugadores que beben 1 trago:\n")
    for jugador in jugadores[num]:
        print(jugador)


baraja = Baraja.Baraja()
palos = ["oros", "espadas", "copas", "bastos"]
caballos = [0 for i in range(4)]
jugadores = [[] for i in range(4)]

posiciones = int(input("Con cuántas posiciones quieres jugar?\n"))
cartas_retroceso = [baraja.sacar_carta() for i in range(posiciones)]
retrocesos = 0
pedir_jugadores()

turnos = 1
print("\033[1m\033[4mComienza la carrera de caballos!\033[0m")

while input("\nPresione la tecla enter para sacar la siguiente carta") == '':
    clear()
    print("\033[4mTurno " + str(turnos) + "\033[0m\n")
    carta = baraja.sacar_carta()
    print("Carta: " + carta + "\n")
    palo = carta.split()[2]
    num = palos.index(palo)
    posicion_nueva = caballos[num] + 1
    caballos[num] = posicion_nueva
    if posicion_nueva == posiciones:
        final()
        break

    print("Jugadores que mandan beber " + str(posicion_nueva) + ":")
    for jugador in jugadores[num]:
        print(jugador)

    if all(posicion > retrocesos for posicion in caballos):
        retrocesos = retrocesos + 1
        retroceso(retrocesos)

    print("\nPosiciones actuales: " + str(caballos))

    turnos = turnos + 1
