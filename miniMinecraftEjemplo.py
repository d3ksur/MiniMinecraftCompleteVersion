from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import tkinter as tk
from noise import snoise2
import random

ventana = None  # Declarar ventana como variable global

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = 'grass',
            color = color.rgb(255, 255, 255),
            highlight_color = color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                voxel = Voxel(position= self.position + mouse.normal)

            if key == "right mouse down":
                destroy(self)

def generar_terreno_malla():
    ChunkSize = 16
    terrain_heights = [[0 for _ in range(ChunkSize)] for _ in range(ChunkSize)]

    for z in range(ChunkSize):
        for x in range(ChunkSize):
            height = int(snoise2(x / 10, z / 10) * 6 + 2)  # Generar altura usando snoise2
            terrain_heights[x][z] = height

            for y in range(height):
                voxel = Voxel(position=(x, y, z))

    # Generar terreno plano debajo del terreno generado
    for z in range(ChunkSize):
        for x in range(ChunkSize):
            for y in range(1, -1, -1):
                voxel = Voxel(position=(x, -y, z))

    return terrain_heights

def iniciar_juego():
    app = Ursina()

    terrain_heights = generar_terreno_malla()

    for z in range(len(terrain_heights)):
        for x in range(len(terrain_heights[z])):
            for y in range(terrain_heights[x][z]):
                voxel = Voxel(position=(x, y, z))

    player = FirstPersonController()

    app.run()

def mostrar_menu():
    global ventana  # Declarar ventana como variable global

    ventana = tk.Tk()

    # Obtener el tamaño de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Configurar el tamaño del menú de inicio
    menu_width = 400
    menu_height = 300

    # Calcular la posición x e y para centrar el menú de inicio
    x = (screen_width - menu_width) // 2
    y = (screen_height - menu_height) // 2

    # Configurar la posición y dimensiones del menú de inicio
    ventana.geometry(f"{menu_width}x{menu_height}+{x}+{y}")

    etiqueta = tk.Label(ventana, text="¡Bienvenido al juego!")
    etiqueta.pack(pady=20)

    boton = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
    boton.pack(pady=10)

    ventana.mainloop()

mostrar_menu()
