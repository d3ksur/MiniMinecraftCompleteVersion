from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from noise import snoise2

app = Ursina()

bloque_usando = 1
textura_pasto = load_texture("complementos/Texturas/Grass_Block.png")
textura_piedra = load_texture("complementos/Texturas/Stone_Block.png")
textura_ladrillo = load_texture("complementos/Texturas/Brick_Block.png")
tierra_textura = load_texture("complementos/Texturas/Dirt_Block.png")
madera_textura = load_texture("complementos/Texturas/Wood_Block.png")
textura_cielo = load_texture("complementos/Texturas/Skybox.png")
textura_mano = load_texture("complementos/Texturas/Arm_Texture.png")
punch_sound = Audio("complementos/Sonidos/Punch_Sound.wav", loop = False, autoplay = False)

def update():
    global bloque_usando

    if held_keys["left mouse"] or held_keys["right mouse"]:
        mano.active()
    else:
        mano.passive()

    if held_keys["1"]: bloque_usando = 1
    if held_keys["2"]: bloque_usando = 2
    if held_keys["3"]: bloque_usando = 3
    if held_keys["4"]: bloque_usando = 4
    if held_keys["5"]: bloque_usando = 5



class Voxel(Button):
    def __init__(self, position = (0, 0, 0), texture = textura_pasto):
        super().__init__(
            parent = scene,
            position = position,
            model = "complementos/Modelos/Block",
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color = color.light_gray,
            scale = 0.5
        )
    
    def input(self,key):
        if self.hovered:
            if key == "left mouse down":
                punch_sound.play()
                if bloque_usando == 1: voxel = Voxel(position = self.position + mouse.normal, texture = textura_pasto)
                if bloque_usando == 2: voxel = Voxel(position = self.position + mouse.normal, texture = textura_piedra)
                if bloque_usando == 3: voxel = Voxel(position = self.position + mouse.normal, texture = textura_ladrillo)
                if bloque_usando == 4: voxel = Voxel(position = self.position + mouse.normal, texture = tierra_textura)
                if bloque_usando == 5: voxel = Voxel(position = self.position + mouse.normal, texture = madera_textura)

            
            if key == "right mouse down":
                punch_sound.play()
                destroy(self)

class Cielo(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "Sphere",
            texture = textura_cielo,
            scale = 150,
            double_sided = True
        )

class Mano(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "complementos/Modelos/Arm",
            texture = textura_mano,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

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

    # for z in range(len(terrain_heights)):
    #     for x in range(len(terrain_heights[z])):
    #         for y in range(terrain_heights[x][z]):
    #             voxel = Voxel(position=(x, y, z))

controladorDeJugador = FirstPersonController()
terrain_heights = generar_terreno_malla()
cielo = Cielo()
mano = Mano()


app.run()