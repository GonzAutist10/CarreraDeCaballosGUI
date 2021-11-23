from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from Baraja import *


def formulario():
    global formulario
    global num_posiciones
    global jugadores_oros, jugadores_espadas, jugadores_copas, jugadores_bastos
    global botones

    # Formulario
    formulario = Frame(raiz)
    formulario.pack()
    formulario.config(bg='gray')

    ttk.Label(formulario, text='Numero de casillas:', background='gray', foreground='white')\
        .grid(row=0, column=0, sticky='w', padx=10, pady=10)
    num_posiciones = IntVar()
    ttk.Entry(formulario, textvariable=num_posiciones).grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(formulario, text='Jugadores que apuestan a oros: ', background='gray', foreground='white')\
        .grid(row=1, column=0, sticky='w', padx=10, pady=10)
    jugadores_oros = Text(formulario, height=1, width=15)
    jugadores_oros.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(formulario, text='Jugadores que apuestan a espadas: ', background='gray', foreground='white')\
        .grid(row=2, column=0, sticky='w', padx=10, pady=10)
    jugadores_espadas = Text(formulario, height=1, width=15)
    jugadores_espadas.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(formulario, text='Jugadores que apuestan a copas: ', background='gray', foreground='white')\
        .grid(row=3, column=0, sticky='w', padx=10, pady=10)
    jugadores_copas = Text(formulario, height=1, width=15)
    jugadores_copas.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(formulario, text='Jugadores que apuestan a bastos: ', background='gray', foreground='white')\
        .grid(row=4, column=0, sticky='w', padx=10, pady=10)
    jugadores_bastos = Text(formulario, height=1, width=15)
    jugadores_bastos.grid(row=4, column=1, padx=10, pady=10)

    # Botones
    botones = Frame(raiz)
    botones.pack(side='bottom', fill='x')
    botones.config(bg='gray')
    ttk.Button(botones, text='Comenzar', command=lambda: comenzar()).pack(side=RIGHT, pady=10, padx=10)
    ttk.Button(botones, text='Salir', command=lambda: salir()).pack(side=LEFT, pady=10, padx=10)


def comenzar():
    global posiciones
    global jugadores
    global cartas_retroceso

    posiciones = num_posiciones.get()
    jugadores[0] = jugadores_oros.get('1.0', END).split('\n')[:-1]
    jugadores[1] = jugadores_espadas.get('1.0', END).split('\n')[:-1]
    jugadores[2] = jugadores_copas.get('1.0', END).split('\n')[:-1]
    jugadores[3] = jugadores_bastos.get('1.0', END).split('\n')[:-1]
    cartas_retroceso = [baraja.sacar_carta() for i in range(posiciones)]
    formulario.destroy()
    botones.destroy()
    construir_tablero()


def construir_tablero():
    global texto
    global botones
    global casillas

    # Tablero
    raiz.attributes('-fullscreen', True)
    tablero = Frame(raiz)
    tablero.pack(pady=50)
    tablero.config(bg='white')

    # Casillas
    img = ImageTk.PhotoImage(Image.open('images/casilla.jpg').resize((80, 120)))
    casillas = [[ttk.Label(tablero, image=img) for j in range(5)] for i in range(posiciones+1)]
    for i in range(posiciones+1):
        for j in range(4):
            casilla = casillas[i][j]
            casilla.photo = img
            casilla.grid(row=i, column=j, padx=10, pady=10)

    # Caballos
    for i in range(4):
        casillas[0][i].configure(image=caballos_img[i])
        casillas[0][i].photo = caballos_img[i]

    # Cartas de retroceso
    img = ImageTk.PhotoImage(Image.open('images/carta.jpg').resize((80, 120)))
    for i in range(1, posiciones+1):
        casillas[i][4].configure(image=img)
        casillas[i][4].photo = img
        casillas[i][4].grid(row=i, column=4, padx=10, pady=10)

    # Texto
    texto = StringVar()
    Entry(raiz, textvariable=texto, state=DISABLED, justify='center', bg='gray', fg='white', font='Helvetica 15 bold', width=47).pack()
    texto.set('¡Comienza la carrera de caballos!')

    # Botones
    botones = Frame(raiz)
    botones.pack()
    botones.config(bg='gray')
    ttk.Button(botones, text='Siguiente', command=lambda: sig_turno()).pack(side=RIGHT, pady=10, padx=150)
    ttk.Button(botones, text='Salir', command=lambda: salir()).pack(side=LEFT, pady=10, padx=150)


def sig_turno():
    global retrocesos

    if all(posicion > retrocesos for posicion in caballos):
        retrocesos += 1
        retroceder()

    else:
        avanzar()


def avanzar():
    mostrar_carta = Toplevel()
    mostrar_carta.title('Carta sacada')
    mostrar_carta.iconbitmap('caballo.ico')
    mostrar_carta.config(bg='gray')

    w = 300
    h = 400
    ws = raiz.winfo_screenwidth()
    hs = raiz.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    mostrar_carta.geometry('%dx%d+%d+%d' % (w, h, x, y))

    carta = baraja.sacar_carta()
    indice = baraja.indices[carta]
    img = baraja.imagenes[indice]
    carta_img = ttk.Label(mostrar_carta, image=img)
    carta_img.photo = img
    carta_img.pack(pady=30, padx=10)

    palo = carta.split()[2]
    num = palos.index(palo)
    posicion_nueva = caballos[num] + 1

    if posicion_nueva == posiciones + 1:
        final(palo)

    img = ImageTk.PhotoImage(Image.open('images/casilla.jpg').resize((80, 120)))
    casillas[caballos[num]][num].configure(image=img)
    casillas[caballos[num]][num].photo = img
    caballos[num] = posicion_nueva
    img = caballos_img[num]
    casillas[caballos[num]][num].configure(image=img)
    casillas[caballos[num]][num].photo = img

    ttk.Label(mostrar_carta, text='Mandan beber ' + str(posicion_nueva) + ' tragos:', background='gray',
              foreground='white', font='Helvetica 10 bold').pack(padx=10, pady=10)
    for jugador in jugadores[num]:
        ttk.Label(mostrar_carta, text=jugador, background='gray', foreground='white', font='Helvetica 10 bold')\
            .pack(padx=10)

    texto.set('¡El caballo de ' + palo + ' avanza!')

    ttk.Button(mostrar_carta, text='OK', command=lambda: mostrar_carta.destroy()).pack(side='bottom', pady=10, padx=10)
    mostrar_carta.mainloop()


def retroceder():
    carta = cartas_retroceso[retrocesos-1]

    palo = carta.split()[2]
    num = palos.index(palo)
    posicion_nueva = caballos[num] - 1

    img = ImageTk.PhotoImage(Image.open('images/casilla.jpg').resize((80, 120)))
    casillas[caballos[num]][num].configure(image=img)
    casillas[caballos[num]][num].photo = img
    caballos[num] = posicion_nueva
    img = caballos_img[num]
    casillas[caballos[num]][num].configure(image=img)
    casillas[caballos[num]][num].photo = img

    indice = baraja.indices[carta]
    img = baraja.imagenes[indice]
    casillas[retrocesos][4].configure(image=img)
    casillas[retrocesos][4].photo = img

    retroceso = Toplevel()
    retroceso.title('Retroceso')
    retroceso.iconbitmap('caballo.ico')
    retroceso.config(bg='gray')

    w = 500
    h = 300
    ws = raiz.winfo_screenwidth()
    hs = raiz.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    retroceso.geometry('%dx%d+%d+%d' % (w, h, x, y))

    ttk.Label(retroceso, text='¡Todos los caballos han alcanzado la posición ' + str(retrocesos) + '!',
              background='gray', foreground='white', font='Helvetica 12 bold').pack(padx=10, pady=10)
    ttk.Label(retroceso, text='Beben 1 trago:', background='gray', foreground='white', font='Helvetica 10 bold')\
        .pack(padx=10, pady=10)

    for jugador in jugadores[num]:
        ttk.Label(retroceso, text=jugador, background='gray', foreground='white', font='Helvetica 10 bold')\
            .pack(padx=10)

    texto.set('¡El caballo de ' + palo + ' retrocede!')
    ttk.Button(retroceso, text='OK', command=lambda: retroceso.destroy()).pack(side='bottom', pady=10, padx=10)
    retroceso.mainloop()


def final(palo):
    num = palos.index(palo)
    victoria = Toplevel()
    victoria.title('Final')
    victoria.iconbitmap('caballo.ico')
    victoria.config(bg='gray')
    victoria.attributes('-fullscreen', True)

    ttk.Label(victoria, text='¡El caballo de ' + str(palo) + ' se alza con la victoria!', background='gray',
              foreground='yellow', font='Helvetica 20 bold').pack(padx=10, pady=50)

    img = caballos_img_final[num]
    caballo = ttk.Label(victoria, image=img)
    caballo.photo = img
    caballo.pack(padx=10, pady=30)

    ttk.Label(victoria, text='Mandan beber el doble de tragos que apostaron:', background='gray',
              foreground='white', font='Helvetica 13 bold').pack(padx=10, pady=10)
    for jugador in jugadores[num]:
        ttk.Label(victoria, text=jugador, background='gray', foreground='white', font='Helvetica 12 bold') \
            .pack(padx=10)

    ttk.Button(victoria, text='Terminar', command=lambda: raiz.destroy()).pack(side='bottom', pady=50, padx=10)
    victoria.mainloop()


def salir():
    resultado = messagebox.askquestion("Salir", "¿Está seguro que desea salir?")

    if resultado == "yes":
        raiz.destroy()


posiciones = 0
palos = ['oros', 'espadas', 'copas', 'bastos']
jugadores = [[] for i in range(4)]
caballos = [0 for i in range(4)]
cartas_retroceso = []
retrocesos = 0

# Root
raiz = Tk()
raiz.title('Carrera de Caballos')
raiz.iconbitmap('caballo.ico')
raiz.config(bg='gray')

w = 400
h = 250
ws = raiz.winfo_screenwidth()
hs = raiz.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
raiz.geometry('%dx%d+%d+%d' % (w, h, x, y))

baraja = Baraja()
caballos_img = [ImageTk.PhotoImage(Image.open('images/caballo_oros.jpg').resize((80, 120))),
                ImageTk.PhotoImage(Image.open('images/caballo_espadas.jpg').resize((80, 120))),
                ImageTk.PhotoImage(Image.open('images/caballo_copas.jpg').resize((80, 120))),
                ImageTk.PhotoImage(Image.open('images/caballo_bastos.jpg').resize((80, 120)))]

caballos_img_final = [ImageTk.PhotoImage(Image.open('images/caballo_oros.jpg').resize((300, 450))),
                      ImageTk.PhotoImage(Image.open('images/caballo_espadas.jpg').resize((300, 450))),
                      ImageTk.PhotoImage(Image.open('images/caballo_copas.jpg').resize((300, 450))),
                      ImageTk.PhotoImage(Image.open('images/caballo_bastos.jpg').resize((300, 450)))]

formulario()

raiz.mainloop()
