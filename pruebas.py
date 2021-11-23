from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()
root.title('Pruebas')

img = ImageTk.PhotoImage(Image.open('001.png'))
ttk.Label(image=img).pack()

root.mainloop()
