from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader 
from random import randint
from numpy import abs, floor

app = Ursina()

#####################
### Variables
#####################

heldBlock = 1 # Block tenu par le joueur par défaut

mapWidth  = 25 # Taille de la carte

waterLevel= 0 # Niveau de la mer

heightMap = [[0]] # Initialisation de la height map
negAmp    = -1    # Amplitude négative de la gen de height map
posAmp    = 1     # Amplitude positive de la gen de height map
minHeight = -1 # Altitude minimum de la map


treeSpawnRate = 80 # Les arbres on une chance sur --treeSpawnRate-- de spawn
treeList = []

#####################
### Load textures
#####################

grassTex  = load_texture('assets/grass_block')
stoneTex  = load_texture('assets/stone_block')
woodTex  = load_texture('assets/wood_block')
dirtTex   = load_texture('assets/dirt_block')
leafTex   = load_texture('assets/leaf_block')

waterTex  = load_texture('assets/water_block')
skyboxTex = load_texture('assets/skybox')

playerArmTex = load_texture('assets/arm_texture')
blockSfx  = Audio('assets/punch_sound.wav', loop = False, autoplay = False)
gameMusic = Audio('assets/Minecraft.mp3',   loop = True,  autoplay = False)

#####################
### Player config
#####################

playerCamera    = FirstPersonController()

playerCamera.speed = 4.5
playerCamera.height = 1.8
playerCamera.gravity = 0.65
playerCamera.jump_height = 1.8	
playerCamera.jump_up_duration = .35	
playerCamera.fall_after = .2
playerCamera.jumping = False	
playerCamera.air_time = 0
playerCamera.cursor.color = color.white
playerCamera.cursor.rotation_z = 0
playerCamera.cursor.scale = .004

#####################
### Game config
#####################

gameMusic.play()
gameMusic.volume=.5

pivot = Entity()
AmbientLight(parent=pivot)

window.fullscreen = False
window.fps_counter.enabled = False
window.exit_button.visible = False

#####################
### Functions
#####################

# Gestion des inputs généraux du jeu
def input(key):
    global heldBlock

    if key == 'escape': quit()
    if key == '1': heldBlock = 1
    if key == '2': heldBlock = 2
    if key == '3': heldBlock = 3
    if key == '4': heldBlock = 4
    

# Actions en jeu, est appelé à chaque frame
def update():
    global heldBlock, mapWidth

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.actif()
    else :
        hand.passif()

    # Si le joueur tombe, il revient au centre de la map
    if playerCamera.y < -20 :
        playerCamera.x = mapWidth/2
        playerCamera.z = mapWidth/2
        playerCamera.y = 30

# Génération d'une height map aléatoire
def genHeightMap():
    global heightMap, mapWidth

    for i in range(1,mapWidth):
        heightMap[0].append((heightMap[0][i-1]+randint(negAmp, posAmp)))
        heightMap.append([(heightMap[i-1][0]+randint(negAmp, posAmp))])

    for i in range(1,mapWidth):
        for j in range(1,mapWidth):
            if heightMap[i][j-1] >= heightMap[i-1][j]:
                heightMap[i].append(randint(heightMap[i-1][j],heightMap[i][j-1]))
            else:
                heightMap[i].append(randint(heightMap[i][j-1],heightMap[i-1][j]))

# On génère la map
def mapCreate():
    global mapWidth, heightMap, minHeight, treeSpawnRate, treeList

    genHeightMap()
    for z in range(mapWidth): 
        for x in range(mapWidth):
            if heightMap[z][x] < 0: Block(position = (x,-1,z), texture = stoneTex)
            else: Block(position = (x,heightMap[z][x],z))

            # On rajoute les blocs entre la position y du bloc et le y minimum de la map
            if heightMap[z][x] != minHeight:
                for i in range(minHeight,heightMap[z][x]):
                    if heightMap[z][x] < 0: Block(position = (x,i,z), texture = stoneTex)
                    else: Block(position = (x,i,z), texture = dirtTex)

            # On rajoute des arbres
            if      heightMap[z][x] >= 0 \
                and randint(0,treeSpawnRate) == 1:
                addTree(x,heightMap[z][x],z)
                treeList.append([z,x])
    addWater()

# On rajoute l'eau à partir du niveau --waterLevel--
def addWater():
    global mapWidth, heightMap, waterLevel
    for z in range(mapWidth):
        for x in range(mapWidth):
            if heightMap[z][x] < waterLevel:
                Block(position =(x,waterLevel,z), texture = waterTex)

# Spawn d'un arbre à la position passée en argument
def addTree(_x,_y,_z):
    height = randint(5,9)
    for i in range(height): # Tronc
        Block(position = (_x,_y+i,_z), texture = woodTex)
    for i in range(1,3):    # Rangées 1 & 2 de feuilles
        for j in range(-2,3):
            for k in range(-2,3):
                if      (j,k) != (_x,_z) \
                    and (j,k) != (-2,-2) \
                    and (j,k) != (-2,2) \
                    and (j,k) != (2,-2) \
                    and (j,k) != (2,2) :
                    Block(position = (_x+j,_y+height-i,_z+k), texture = leafTex, double_sided=True, scale=.49)
    for j in range(-1,2): # Rangées 3 de feuilles
        for k in range(-1,2):
            if (j,k) != (_x,_z):
                Block(position = (_x+j,_y+height,_z+k), texture = leafTex, double_sided=True, scale=.49)
    for j in range(-1,2): # Rangées 4 de feuilles
        for k in range(-1,2):
            if      (j,k) != (-1,-1) \
                and (j,k) != (-1,1) \
                and (j,k) != (1,-1) \
                and (j,k) != (1,1) :
                Block(position = (_x+j,_y+height+1,_z+k), texture = leafTex, double_sided=True, scale=.49)

#####################
### Classes
#####################

# Main visible du joueur
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent    = camera.ui,
            model     = load_model('assets/arm.obj'),
            texture   = playerArmTex,
            scale     = 0.2,
            rotation  = Vec3(150,-10,50),
            position  = Vec2(0.4,-0.6)
        )

    # Animation au clic
    def actif(self):
        self.position = Vec2(0.3,-0.5)
    def passif(self):
        self.position = Vec2(0.4,-0.6)

# Création d'un block
class Block(Button):
    def __init__(self, position = (0,0,0), texture = grassTex, double_sided=False, scale=.5): # Caractéristriques d'un block
        super().__init__(
            parent   = scene,
            position = position,
            model    = load_model('assets/block.obj'),
            origin_y = 0.5,
            texture  = texture,
            color    = color.color(0,0,random.uniform(0.9,1)),
            highlight_color = color.rgb(215,215,215),
            scale    = scale,
            shader   = basic_lighting_shader,
            double_sided= double_sided
        )
    
    def input(self,key): # Inputs add/delete block
        if self.hovered:
            if key == 'left mouse down': 
                blockSfx.play()
                if heldBlock == 1: block = Block(position = self.position + mouse.normal, texture = grassTex)
                if heldBlock == 2: block = Block(position = self.position + mouse.normal, texture = stoneTex)
                if heldBlock == 3: block = Block(position = self.position + mouse.normal, texture = woodTex)
                if heldBlock == 4: block = Block(position = self.position + mouse.normal, texture = leafTex, double_sided = True, scale=0.49)
            if key == 'right mouse down': 
                if self.texture != waterTex:
                    blockSfx.play()
                    destroy(self)

#####################
### Main code
#####################

mapCreate()

# On place le joueur
playerCamera.position = (floor(mapWidth/2), 20, floor(mapWidth/2))

#####################
### Game launch
#####################

sky  = Sky()
hand = Hand()

app.run()