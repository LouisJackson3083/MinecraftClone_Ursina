from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
sky = Sky()
sky.color = window.color
player = FirstPersonController()
player.gravity = 0.0
player.height = 1.8
player.camera_pivot.y = player.height
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
        player.speed = 16
    else:
        playerGamemode='survival'
        player.speed = 8

def input(key):
    if key == 'c':
        switch_render_mode()
    if key == 'x':
        switch_playerGamemode()
# endregion

pX = player.x
pZ = player.z

def update():
    global pX, pZ

    print(pX,pZ)
    # Generate terrain at current swirl position
    terrain.generateTerrain()

    blockFound=False
    step = 2
    height = 1.86

    if abs(player.x - pX)>16 or abs(player.z - pZ)>16:
        pX=player.x
        pZ=player.z
        terrain.swirlEngine.reset(pX,pZ)

    if playerGamemode == 'creative':
        if held_keys['space']:
            player.y += 20*time.dt
        if held_keys['shift']:
            player.y -= 20*time.dt

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


app.run()