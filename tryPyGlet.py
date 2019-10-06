import pyglet
import math as mth
from player import *
from wall import *
import copy

window = pyglet.window.Window(width=1920, height=1080)
pyglet.vsync = True
label = pyglet.text.Label("Hello World", font_name="Comic Sans", font_size=25,
x=window.width/2, y=window.height-25,
anchor_x="center", anchor_y="center"
)

gen = 0

amount_of_rays = 4
players = players = []
am_of_players = 10

walls = []

walls.append(Wall([1, 0], [1, window.height]))
walls.append(Wall([window.width, 0], [window.width, window.height]))
walls.append(Wall([1, window.height-1], [window.width, window.height-1]))
walls.append(Wall([1, 1], [window.width, 1]))
walls.append(Wall( [window.width/2-300, window.height/2-200], [window.width/2+300, window.height/2-200] ))
walls.append(Wall( [window.width/2-300, window.height/2-200], [window.width/2-400, window.height/2-100] ))
walls.append(Wall( [window.width/2-400, window.height/2+100], [window.width/2-400, window.height/2-100] ))
walls.append(Wall( [window.width/2-300, window.height/2], [window.width/2+300, window.height/2] ))


for i in range(am_of_players):
    players.append(Player([window.width/2, window.height/2-100], amount_of_rays, False))


def draw_line(xy1, xy2):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (int(xy1[0]), int(xy1[1]), int(xy2[0]), int(xy2[1])))
    )


def repopulate():
    global players
    copys = []
    for p in players:
        new_p = Player([window.width/2, window.height/2-100], amount_of_rays, False)
        new_p.net = copy.deepcopy(p.net)
        copys.append(new_p)
    for p in copys:
        p.net.randomize_net(100)
    players = players + copys



@window.event
def on_draw():
    window.clear()
    label.draw()
    for p in players:
        if not p.dead:
            p.sprite.draw()
    for w in walls:
        draw_line(w.start_pos, w.end_pos)
    

def update(delta_time):
    global gen
    
    for p in players:
        p.cast_rays(walls)
        p.set_net_input()
        p.move(delta_time)
        p.check_for_hit()
        if p.dead:
            if len(players) > am_of_players/2:
                players.remove(p)
            else:
                print(gen)
                gen += 1
                repopulate()
                for pl in players:
                    pl.pos = [window.width/2, window.height/2-100]
                    pl.rot = 0
        

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()