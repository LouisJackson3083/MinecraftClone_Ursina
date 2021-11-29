from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()

# region textures
texture_grass = [load_texture('assets/textures/block_grass.png'),load_texture('assets/textures/block_grass2.png'),load_texture('assets/textures/block_grass3.png'),load_texture('assets/textures/block_grass4.png')]
texture_dirt = load_texture('assets/textures/block_dirt.png')
texture_stone = load_texture('assets/textures/block_stone.png')
texture_brick = load_texture('assets/textures/block_brick.png')
texture_log = load_texture('assets/textures/block_log.png')
texture_leaves = load_texture('assets/textures/block_leaves.png')
texture_none = load_texture('assets/textures/block_invisible.png')
texture_sky = load_texture('assets/textures/skybox.png')
texture_arm = load_texture('assets/textures/texture_arm.png')
# endregion
# region sound
sound_punch = Audio('assets/sounds/sound_punch', loop = False, autoplay = False)
# endregion

hotbar_selection = 1
render_mode = 0

window.fps_counter.enabled = False
window.exit_button = False

def switch_render_mode():
    global render_mode
    render_mode+=1
    if render_mode>=4: render_mode=0
    window.render_mode = window.render_modes[render_mode]

def player_setup():
    player.height = 1.6
    player.camera_pivot.y = player.height
    player.jump_height = 1.6
    #player.collider = BoxCollider(player, center=Vec3(0,0.9,0), size=Vec3(0.8,1.9,0.8))

def input(key):
    if key == 'c':
        switch_render_mode()

def update():
    global hotbar_selection
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.active()
    else:
        arm.passive()

    if held_keys['1']: 
        hotbar_selection = 1
        arm_block.update_block(texture_grass[3])
    if held_keys['2']: 
        hotbar_selection = 2
        arm_block.update_block(texture_dirt)
    if held_keys['3']: 
        hotbar_selection = 3
        arm_block.update_block(texture_stone)
    if held_keys['4']: 
        hotbar_selection = 4
        arm_block.update_block(texture_brick)
    if held_keys['5']: 
        hotbar_selection = 5
        arm_block.update_block(texture_log)
    if held_keys['6']: 
        hotbar_selection = 6
        arm_block.update_block(texture_leaves)

def create_tree(position = (0,0,0), height = 9, size = 7):
    tree = []
    for i in range(size):
        for j in range(height-4,height+1):
            for k in range(size):
                if (((i==0 or i==size-1) or (k==0 or k==size-1)) and (j==height-size+1 or j==height)) or ((i==0 or i==size-1) and (k==0 or k==size-1) or (j < height-1 and i == size//2 and k == size//2)):
                    continue
                else:
                    voxel = Voxel(position=position+(i-size//2, j, k-size//2), texture = texture_leaves)
    for i in range(height-1):
        voxel = Voxel(position=position+(0, i, 0), texture = texture_log)

def create_chunk(xChunk,zChunk):
    for z in range(16):
        for x in range(16):
            #height = round(GeneratedNoiseMap(z, x, 20) * maxHeight)
            voxel = Voxel(position=(x + xChunk*16, 0, z + zChunk*16), texture = random.choice(texture_grass))
            voxel = Voxel(position=(x + xChunk*16, -1, z + zChunk*16), texture = texture_dirt)                

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
                #e = Entity(model='cube', parent=scene, origin_y = 0.25, collider = 'box', texture = texture_brick, position=self.position+mouse.normal)
                
                if hotbar_selection == 1: voxel = Voxel(position = self.position + mouse.normal, texture = random.choice(texture_grass))
                if hotbar_selection == 2: voxel = Voxel(position = self.position + mouse.normal, texture = texture_dirt)
                if hotbar_selection == 3: voxel = Voxel(position = self.position + mouse.normal, texture = texture_stone)
                if hotbar_selection == 4: voxel = Voxel(position = self.position + mouse.normal, texture = texture_brick)
                if hotbar_selection == 5: voxel = Voxel(position = self.position + mouse.normal, texture = texture_log)
                if hotbar_selection == 6: voxel = Voxel(position = self.position + mouse.normal, texture = texture_leaves)

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
    def update_block(self, texture = texture_grass[3]):
        self.texture = texture


level_colliders = Entity(model=Mesh(vertices=[], uvs=[]))
# hotbar = Entity(model='quad', scale=(5,1), position=(0,-1), parent = camera.ui)

create_chunk(0,0)
create_chunk(0,1)
create_chunk(1,0)
create_chunk(1,1)

create_tree(position = (10,0,10))

player = FirstPersonController()
arm = Arm()
arm_block = ArmBlock(arm, texture_grass[3])
sky = Sky()
player_setup()
player_collision_zone = CollisionZone(parent=player, radius=2)
level_colliders.collider = 'mesh' # call this only once after all vertices are set up
#print(level_parent.model.vertices)

app.run()