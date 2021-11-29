from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
sky = Sky()
sky.color = window.color
player = FirstPersonController()
player.gravity = 0.0
player.cursor.visible = False
playerGamemode = 'survival'

terrain = MeshTerrain()

# region stuff i added
render_mode = 0
def switch_render_mode():
    global render_mode
    render_mode+=1
    if render_mode>=4: render_mode=0
    window.render_mode = window.render_modes[render_mode]
def switch_playerGamemode():
    global playerGamemode
    if playerGamemode == 'survival':
        playerGamemode='creative'
    else:
        playerGamemode='survival'

def input(key):
    if key == 'c':
        switch_render_mode()
    if key == 'x':
        switch_playerGamemode()

    if playerGamemode == 'creative':
        if key == 'f':
            player.y += 5*time.dt
        if key == 'g':
            player.y -= 5*time.dt
# endregion

def update():
    blockFound=False
    step = 2
    height = 1.86

    if playerGamemode == 'survival':
        x = str(floor(player.x+0.5))
        y = floor(player.y+0.5)
        z = str(floor(player.z+0.5))
        for i in range(-step,step):
            if terrain.td.get("x"+x+"y"+str(y+i)+"z"+z)=="t":
                target = y+i+height
                blockFound=True
                break

        if blockFound==True:
            player.y = lerp(player.y, target, 6 * time.dt) # Lerp the player to the target position
        else:
            player.y -= 9.8 * time.dt # Apply gravity
    # updateTerrain()
    pass

terrain.generateTerrain()

app.run()