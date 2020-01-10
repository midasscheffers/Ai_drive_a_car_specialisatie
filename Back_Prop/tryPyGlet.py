import pyglet
import math as mth
from player import *
from wall import *
from checkpiont import *
import copy
import random as r


# globals
WIDTH = 1300
HEIGHT = 820

gen = 0


amount_of_rays = 90
players = []
am_of_players = 1
cycles = 1

walls = []


window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
pyglet.vsync = True
label = pyglet.text.Label("gen: 0, players: 100", font_name="Comic Sans", font_size=25,
x=WIDTH/2, y=HEIGHT-25,
anchor_x="center", anchor_y="center"
)



# make all the walls of the game
walls.append(Wall([1, 0], [1, HEIGHT]))
walls.append(Wall([WIDTH, 0], [WIDTH, HEIGHT]))
walls.append(Wall([1, HEIGHT-1], [WIDTH, HEIGHT-1]))
walls.append(Wall([1, 1], [WIDTH, 1]))
walls.append(Wall( [WIDTH/2-300, HEIGHT/2-200], [WIDTH/2+300, HEIGHT/2-200] ))
walls.append(Wall( [WIDTH/2-300, HEIGHT/2-200], [WIDTH/2-400, HEIGHT/2-100] ))
walls.append(Wall( [WIDTH/2-400, HEIGHT/2+100], [WIDTH/2-400, HEIGHT/2-100] ))
walls.append(Wall( [WIDTH/2-200, HEIGHT/2], [WIDTH/2+300, HEIGHT/2] ))
walls.append(Wall( [WIDTH/2-200, HEIGHT/2], [WIDTH/2+300, HEIGHT/2] ))
walls.append(Wall( [WIDTH/2-200, HEIGHT/2], [WIDTH/2-200, HEIGHT/2 + 100] ))
walls.append(Wall( [WIDTH/2, HEIGHT/2 + 100], [WIDTH/2-200, HEIGHT/2 + 100] ))
walls.append(Wall( [WIDTH/2-400, HEIGHT/2 + 100], [WIDTH/2-300, HEIGHT/2 + 220] ))
walls.append(Wall( [WIDTH/2-100, HEIGHT/2 + 220], [WIDTH/2-300, HEIGHT/2 + 220] ))
walls.append(Wall( [WIDTH/2, HEIGHT/2 + 100], [WIDTH/2+100, HEIGHT/2 + 200] ))
walls.append(Wall( [WIDTH/2 + 100, HEIGHT/2 + 360], [WIDTH/2+100, HEIGHT/2 + 200] ))
walls.append(Wall( [WIDTH/2+600, HEIGHT/2-100], [WIDTH/2+300, HEIGHT/2] ))
walls.append(Wall( [WIDTH/2 + 100, HEIGHT/2 + 360], [WIDTH/2-500, HEIGHT/2 + 360] ))
walls.append(Wall( [WIDTH/2 - 600, HEIGHT/2 + 260], [WIDTH/2-500, HEIGHT/2 + 360] ))
walls.append(Wall( [WIDTH/2 - 600, HEIGHT/2 + 260], [WIDTH/2-600, HEIGHT/2 - 360] ))
walls.append(Wall( [WIDTH/2+600, HEIGHT/2-100], [WIDTH/2+600, HEIGHT/2 - 360] ))
walls.append(Wall( [WIDTH/2-600, HEIGHT/2-360], [WIDTH/2+600, HEIGHT/2 - 360] ))


# greate first players
for i in range(am_of_players):
    players.append(Player([WIDTH/2, HEIGHT/2-100], amount_of_rays, 90, False))


def draw_line(xy1, xy2, color):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (int(xy1[0]), int(xy1[1]), int(xy2[0]), int(xy2[1]))),
        ('c4B', (color) * 2)
    )


def reset_players(players):
    for p in players:
        p.pos = [WIDTH/2, HEIGHT/2-100]
        p.rot = 0
        p.reset_rays()
        p.dead = False


def all_dead(players):
    for p in players:
        if not p.dead:
            return False
    return True


@window.event
def on_draw():
    # if gen % 10 == 0:
    window.clear()
    label.draw()
    for p in players:
        if not p.dead:
            # p.sprite.draw()
            for line in p.boundries:
                    draw_line([ line[0], line[1] ], [ line[2], line[3] ], p.color)
            for rp in p.ray_pts:
                draw_line([p.pos[0], p.pos[1]], [rp[0], rp[1]], (p.rays[p.ray_pts.index(rp)]).color)
                (p.rays[p.ray_pts.index(rp)]).color = (255, 0, 255, 255)
    for w in walls:
        draw_line(w.start_pos, w.end_pos, w.color)
    # else:
    #     window.clear()
    #     label.draw()
    

def update(delta_time):
    global gen
    global players
    for i in range(cycles):
        if all_dead(players):

            for p in players:
                p.net.change_net_weights()

            reset_players(players)
            
            # players = repopulate(players)
            gen += 1
            
            label.text = (str("gen: " + str(gen) + " players: " + str(len(players))))

            

        for p in players:
            if not p.dead:
                p.cast_rays(walls)
                p.set_net_input()
                p.move(.02)
                p.net.calc_cost(p.find_dis_out())
                p.check_for_hit(walls)
                p.out_off_bounds(WIDTH, HEIGHT)
                

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()