from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()

# region textures
texture_grass = [load_texture('assets/textures/block_grass.png'),load_texture('assets/textures/block_grass2.png'),load_texture('assets/textures/block_grass3.png'),load_texture('assets/textures/block_grass4.png')]
texture_dirt = load_texture('assets/textures/block_dirt.png')
texture_stone = load_texture('assets/textures/block_stone.png')
texture_brick = load_texture('assets/textures/block_brick.png')
texture_none = load_texture('assets/textures/block_invisible.png')
texture_sky = load_texture('assets/textures/skybox.png')
texture_arm = load_texture('assets/textures/texture_arm.png')
# endregion
# region sound
sound_punch = Audio('assets/sounds/sound_punch', loop = False, autoplay = False)
# endregion
hotbar_selection = 1

window.fps_counter.enabled = False
window.exit_button = False

def input(key):
    if key == 'c':
        level_parent.collision = not level_parent.collision

def update():
    global hotbar_selection
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.active()
    else:
        arm.passive()

    if held_keys['1']: 
        hotbar_selection = 1
        arm_block.update_block(hotbar_selection)
    if held_keys['2']: 
        hotbar_selection = 2
        arm_block.update_block(hotbar_selection)
    if held_keys['3']: 
        hotbar_selection = 3
        arm_block.update_block(hotbar_selection)
    if held_keys['4']: 
        hotbar_selection = 4
        arm_block.update_block(hotbar_selection)

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = texture_grass[3]):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/models/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            highlight_color = color.white,
            scale = 0.5)
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                sound_punch.play()
                destroy(self)

            if key == 'right mouse down':
                sound_punch.play()
                if hotbar_selection == 1: voxel = Voxel(position = self.position + mouse.normal, texture = random.choice(texture_grass))
                if hotbar_selection == 2: voxel = Voxel(position = self.position + mouse.normal, texture = texture_dirt)
                if hotbar_selection == 3: voxel = Voxel(position = self.position + mouse.normal, texture = texture_stone)
                if hotbar_selection == 4: voxel = Voxel(position = self.position + mouse.normal, texture = texture_brick)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = texture_sky,
            scale = 1000,
            double_sided = True)

class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/models/arm',
            texture = texture_arm,
            scale = 0.2,
            rotation = Vec3(160,-10,0),
            position = Vec2(0.6,-0.6))
    def active(self):
        self.rotation =  Vec3(160,-20,0),
        self.position = Vec2(0.5,-0.5)
    def passive(self):
        self.rotation =  Vec3(160,-10,0),
        self.position = Vec2(0.6,-0.6)

class ArmBlock(Entity):
    def __init__(self, parent = camera.ui, texture = texture_grass[3]):
        super().__init__(
            parent = parent,
            model = 'assets/models/block',
            texture = texture,
            scale = 0.75,
            rotation = Vec3(180,0,0),
            position = Vec3(-0.5,-0.25,-3))
    def update_block(self, hotbar_selection):
        print(hotbar_selection)
        if hotbar_selection == 1:
            self.texture = texture_grass[3]
        if hotbar_selection == 2:
            self.texture = texture_dirt
        if hotbar_selection == 3:
            self.texture = texture_stone
        if hotbar_selection == 4:
            self.texture = texture_brick


level_parent = Entity(model=Mesh(vertices=[], uvs=[]))
hotbar = Entity(model='quad', scale=(5,1), position=(0,-1), parent = camera.ui)

for z in range(8):
    for x in range(8):
        #height = round(GeneratedNoiseMap(z, x, 20) * maxHeight)
        voxel = Voxel(position=(x, 0, z), texture = random.choice(texture_grass))
        voxel = Voxel(position=(x, -1, z), texture = texture_dirt)
        

player = FirstPersonController()
arm = Arm()
arm_block = ArmBlock(arm, texture_grass[3])
sky = Sky()
player_collision_zone = CollisionZone(parent=player, radius=2)
level_parent.collider = 'mesh' # call this only once after all vertices are set up
#print(level_parent.model.vertices)
app.run()