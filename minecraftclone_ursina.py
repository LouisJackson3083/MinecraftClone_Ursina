from ursina import *

class Test_cube(Entity):
    def __init__(self):
        super().__init__(
            model = 'cube',
            color = color.white,
            texture = 'white_cube',
            rotation = Vec3(45,45,45)
        )
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                print('Button Pressed')

class Test_button(Button):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'cube',
            texture = 'brick',
            color = color.blue,
            highlight_color = color.red,
            pressed_color = color.green
        )

def update():
    if held_keys['a']:
        test_square.x -= 5 * time.dt
        test_square.y -= 5 * time.dt

app = Ursina()

test_square = Entity(model = 'quad', color = color.red, scale = (1,4), position = (5,4))

# tamarin_texture = load_texture('assets/tamarin.jpg')
# tamarin = Entity(model = 'quad', texture = tamarin_texture, scale = (5,5))

test_cube = Test_button()

app.run()