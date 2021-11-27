from ursina import *

class Test_cube(Entity):
    def __init__(self):
        super().__init__(
            model = 'cube',
            color = color.white,
            texture = 'white_cube'
            )

def update():
    if held_keys['a']:
        test_square.x -= 5 * time.dt
        test_square.y -= 5 * time.dt

app = Ursina()

test_square = Entity(model = 'quad', color = color.red, scale = (1,4), position = (5,4))

tamarin_texture = load_texture('assets/tamarin.jpg')
tamarin = Entity(model = 'quad', texture = tamarin_texture, scale = (5,5))

test_cube = Test_cube()

app.run()