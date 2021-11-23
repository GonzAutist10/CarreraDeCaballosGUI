import random
from PIL import Image, ImageTk


class Baraja:
    def __init__(self):
        self.baraja = sum(list(map(lambda n:
                                   [str(n)+' de oros', str(n)+' de espadas', str(n)+' de copas', str(n)+' de bastos'],
                                   ["As", 2, 3, 4, 5, 6, 7, "Sota", "Rey"])), [])
        self.imagenes = []
        self.indices = {}
        self.contador = 0
        for i in self.baraja:
            self.imagenes.append(ImageTk.PhotoImage(Image.open('images/' + i + '.jpg').resize((80, 120))))
            self.indices[i] = self.contador
            self.contador += 1
        self.barajar()

    def barajar(self):
        random.shuffle(self.baraja)

    def sacar_carta(self):
        return self.baraja.pop()
