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
            pressed_color = color.green)
    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                print("AAAAAAAAAAAAAAAAA")
def update():
    if held_keys['a']:
        print("Pressed A")

app = Ursina()

test_cube = Test_button()

app.run()