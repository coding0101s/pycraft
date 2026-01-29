from ursina import *

app = Ursina()

hit_distance = 4

# create player
from ursina.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController(y=6, height=1.7, jump_height=1.5, gravity=0.5, collider='box')
player.cursor.enabled = False

class Block(Entity):
    def __init__(self, pos=(0, 0, 0)):
        super().__init__(
            parent=scene,
            color=color.white,
            model='cube',
            collider='box',
            position=pos,
            scale=(1, 1)
        )

        if pos[1] != 4:
            self.texture = 'image/stone.png'
        elif pos[1] == 4:
            self.texture = 'image/grass.png'

def input(key):
    if key == 'escape':
        application.quit()

    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=hit_distance, ignore=(player,))

        if hit_info.hit:
            destroy(hit_info.entity)
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=hit_distance, ignore=(player,))

        if hit_info.hit:
            target_pos = hit_info.entity.position + hit_info.normal
            if target_pos != player.position:
                Block(target_pos)

white = Entity(
        parent=scene,
        model='cube',
        color=color.white,
        scale=1.0001
)
white.alpha = 0.5
white.enabled = False
prev_entity = [None]

def update():
    hit_info = raycast(camera.world_position, camera.forward, distance=hit_distance, ignore=(player,))
    if hit_info.hit:
        if prev_entity[0] == hit_info.entity:
            return 
        
        if prev_entity[0] != None:
            white.enabled = False

        prev_entity[0] = hit_info.entity
        white.position = hit_info.entity.position
        white.enabled = True
    else:
        white.enabled = False

# turn off scene debug ui
from ursina.prefabs.editor_camera import EditorCamera
window.editor_ui.enabled = False

# turn off exit button and fps counter
window.exit_button.visible = False
window.fps_counter = False

# main
window.title = 'Pycraft'
window.borderless = False
window.fullscreen = True
# window.size = (800, 600)
window.color = color.azure

for y in range(5):
    for x in range(10):
        for z in range(10):
            Block((x, y, z))

app.run()