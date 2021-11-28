from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()

# region textures
texture_grass = load_texture('assets/textures/block_grass.png')
texture_dirt = load_texture('assets/textures/block_dirt.png')
texture_stone = load_texture('assets/textures/block_stone.png')
texture_brick = load_texture('assets/textures/block_brick.png')
sky_texture = load_texture('assets/textures/skybox.png')
texture_arm = load_texture('assets/textures/texture_arm.png')
# endregion
# region sound
sound_punch = Audio('assets/sounds/sound_punch', loop = False, autoplay = False)
# endregion
hotbar_selection = 1

window.fps_counter.enabled = False
window.exit_button = False

def update():
    global hotbar_selection
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.active()
    else:
        arm.passive()

    if held_keys['1']: hotbar_selection = 1
    if held_keys['2']: hotbar_selection = 2
    if held_keys['3']: hotbar_selection = 3
    if held_keys['4']: hotbar_selection = 4

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = texture_grass):
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
                if hotbar_selection == 1: voxel = Voxel(position = self.position + mouse.normal, texture = texture_grass)
                if hotbar_selection == 2: voxel = Voxel(position = self.position + mouse.normal, texture = texture_dirt)
                if hotbar_selection == 3: voxel = Voxel(position = self.position + mouse.normal, texture = texture_stone)
                if hotbar_selection == 4: voxel = Voxel(position = self.position + mouse.normal, texture = texture_brick)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
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

level_parent = Entity(model=Mesh(vertices=[], uvs=[]))

for z in range(8):
    for x in range(8):
        # height = round(GeneratedNoiseMap(z, x, 20) * maxHeight)
        voxel = Voxel(position=(x, 0, z))
        level_parent.model.vertices.extend(voxel.model.vertices)
        

player = FirstPersonController()
arm = Arm()
sky = Sky()
player_collision_zone = CollisionZone(parent=player, radius=2)
level_parent.collider = 'mesh' # call this only once after all vertices are set up
print(level_parent.model.vertices)


app.run()