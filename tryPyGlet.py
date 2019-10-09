import pyglet
import math as mth
from player import *
from wall import *
import copy

window = pyglet.window.Window(width=1200, height=720)
pyglet.vsync = True
label = pyglet.text.Label("Hello World", font_name="Comic Sans", font_size=25,
x=window.width/2, y=window.height-25,
anchor_x="center", anchor_y="center"
)

gen = 0

amount_of_rays = 4
players = players = []
am_of_players = 70
cycles = 10

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


def reset_players(players):
    for p in players:
        p.pos = [window.width/2, window.height/2-100]
        p.rot = 0
        p.dead = False


def all_dead():
    for p in players:
        if not p.dead:
            return False
    return True

def repopulate(players):
    print("repopulate")
    calculate_fitness(players)

    new_players = []

    for p in players:
        new_players.append(pick_player(players))
        
    players = new_players
    print("done repopulating")

def pick_player(players):
    index = 0
    rand = r.random()
    while rand > 0:
        rand -= players[index].fitness
        index += 1
    index -= 1

    p = players[index]
    child = Player([window.width/2, window.height/2-100], amount_of_rays, False)
    child.net = copy.deepcopy(p.net)
    child.net.randomize_net(2)
    return child

def calculate_fitness(players):
    sum = 0
    for p in players:
        sum += p.score
    for p in players:
        p.fitness = mth.pow(p.check_piont, 2) * p.score / sum


@window.event
def on_draw():
    window.clear()
    label.draw()
    for p in players:
        # if not p.dead:
        p.sprite.draw()
    for w in walls:
        draw_line(w.start_pos, w.end_pos)
    

def update(delta_time):
    global gen
    # for i in range(cycles):
    if all_dead():
        reset_players(players)
        repopulate(players)
        gen += 1
        print(gen)

    for p in players:
        if not p.dead:
            p.cast_rays(walls)
            p.set_net_input()
            p.move(delta_time)
            p.check_for_hit()
                
        

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()