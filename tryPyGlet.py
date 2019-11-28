import pyglet
import matplotlib.pyplot as plt
import math as mth
from player import *
from wall import *
from checkpiont import *
import copy
import random as r

window = pyglet.window.Window(width=1300, height=820)
pyglet.vsync = True
label = pyglet.text.Label("gen: 0, players: 100", font_name="Comic Sans", font_size=25,
x=window.width/2, y=window.height-25,
anchor_x="center", anchor_y="center"
)

# globals

gen = 0

gen_table = []
avr_fitness_table = []
avr_score_table = []
best_score_table = []
best_fitness_table = []

amount_of_rays = 4
players = []
am_of_players = 100
cycles = 1
graph_cycles = 20

checkpoints = []
walls = []

# make all the walls of the game

walls.append(Wall([1, 0], [1, window.height]))
walls.append(Wall([window.width, 0], [window.width, window.height]))
walls.append(Wall([1, window.height-1], [window.width, window.height-1]))
walls.append(Wall([1, 1], [window.width, 1]))
walls.append(Wall( [window.width/2-300, window.height/2-200], [window.width/2+300, window.height/2-200] ))
walls.append(Wall( [window.width/2-300, window.height/2-200], [window.width/2-400, window.height/2-100] ))
walls.append(Wall( [window.width/2-400, window.height/2+100], [window.width/2-400, window.height/2-100] ))
walls.append(Wall( [window.width/2-200, window.height/2], [window.width/2+300, window.height/2] ))
walls.append(Wall( [window.width/2-200, window.height/2], [window.width/2+300, window.height/2] ))
walls.append(Wall( [window.width/2-200, window.height/2], [window.width/2-200, window.height/2 + 100] ))
walls.append(Wall( [window.width/2, window.height/2 + 100], [window.width/2-200, window.height/2 + 100] ))
walls.append(Wall( [window.width/2-400, window.height/2 + 100], [window.width/2-300, window.height/2 + 220] ))
walls.append(Wall( [window.width/2-100, window.height/2 + 220], [window.width/2-300, window.height/2 + 220] ))
walls.append(Wall( [window.width/2, window.height/2 + 100], [window.width/2+100, window.height/2 + 200] ))
walls.append(Wall( [window.width/2 + 100, window.height/2 + 360], [window.width/2+100, window.height/2 + 200] ))
walls.append(Wall( [window.width/2+600, window.height/2-100], [window.width/2+300, window.height/2] ))
walls.append(Wall( [window.width/2 + 100, window.height/2 + 360], [window.width/2-500, window.height/2 + 360] ))
walls.append(Wall( [window.width/2 - 600, window.height/2 + 260], [window.width/2-500, window.height/2 + 360] ))
walls.append(Wall( [window.width/2 - 600, window.height/2 + 260], [window.width/2-600, window.height/2 - 360] ))
walls.append(Wall( [window.width/2+600, window.height/2-100], [window.width/2+600, window.height/2 - 360] ))
walls.append(Wall( [window.width/2-600, window.height/2-360], [window.width/2+600, window.height/2 - 360] ))

# make checkpoints

checkpoints.append(Checkpoint([window.width/2+300, window.height/2-200], [window.width/2+300, window.height/2], 2))
checkpoints.append(Checkpoint([window.width/2+300, window.height/2-200], [window.width/2+600, window.height/2-200], 3))
checkpoints.append(Checkpoint([window.width/2+300, window.height/2-200], [window.width/2+300, window.height/2-360], 4))
checkpoints.append(Checkpoint([window.width/2, window.height/2-200], [window.width/2, window.height/2-360], 5))
checkpoints.append(Checkpoint([window.width/2-300, window.height/2-200], [window.width/2-300, window.height/2-360], 5))


# greate first players
for i in range(am_of_players):
    players.append(Player([window.width/2, window.height/2-100], amount_of_rays, False))


def draw_line(xy1, xy2, color):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (int(xy1[0]), int(xy1[1]), int(xy2[0]), int(xy2[1]))),
        ('c4B', (color) * 2)
    )


def reset_players(players):
    for p in players:
        p.pos = [window.width/2, window.height/2-100]
        p.rot = 0
        p.dead = False


def all_dead(players):
    for p in players:
        if not p.dead:
            return False
    return True


def calc_avr_score(players):
    tot_score = 0
    for p in players:
        tot_score += p.score
    avr = tot_score/len(players)
    return avr


def calc_avr_fitness(players):
    tot_fit = 0
    for p in players:
        tot_fit += p.fitness
    avr = tot_fit/len(players)
    return avr

def find_best_score(players):
    best_score = 0
    for p in players:
        if p.score > best_score:
            best_score = p.score
    return best_score

def find_best_fitt(players):
    best_fit = 0
    best_fit_player = None
    for p in players:
        if p.fitness > best_fit:
            best_fit = p.fitness
            best_fit_player = p
    return best_fit, best_fit_player


def repopulate(players):
    calculate_fitness(players)

    avr_fit = calc_avr_fitness(players)
    avr_score = calc_avr_score(players)
    best_fit, best_player = find_best_fitt(players)
    best_score = find_best_score(players)

    best_score_table.append(best_score)
    best_fitness_table.append(best_fit)
    avr_fitness_table.append(avr_fit)
    avr_score_table.append(avr_score)

    new_players = []

    bP = Player([window.width/2, window.height/2-100], amount_of_rays, False)
    bP.net = copy.deepcopy(best_player.net)

    new_players.append(bP)

    for i in range(int((len(players) - 1)/3)):
        p = pick_player(players)
        p.net.randomize_net(1)
        p.dead = False
        new_players.append(p)
    for i in range(int(mth.ceil((len(players) - 1)/3))):
        p1 = pick_player(players)
        p2 = pick_player(players)
        p3 = cross_players(p1, p2)
        p3.dead = False
        new_players.append(p3)
    for i in range(int((len(players) - 1)/3)):
        new_players.append(Player([window.width/2, window.height/2-100], amount_of_rays, False))
        
    players = []
    players = new_players
    return players
    

def pick_player(players):
    index = 0
    rand = r.random() * am_of_players
    while rand > 0:
        rand -= players[index].fitness
        index += 1
    index -= 1
    child = Player([window.width/2, window.height/2-100], amount_of_rays, False)
    child.net = copy.deepcopy(players[index].net)
    return child


def cross_players(p1, p2):
    # make child with net of first parrent
    child = Player([window.width/2, window.height/2-100], amount_of_rays, False)
    child.net = copy.deepcopy(p1.net)
    for i in range(len(child.net.nodes)):
        if not i == 0:
            for n in range(len(child.net.nodes[i])):
                node = child.net.nodes[i][n]
                for w in range(len(node.weights)):
                    if r.randint(0,1):
                        weight = p2.net.nodes[i][n].weights[w]
    return child



def calculate_fitness(players):
    sum = 0
    for p in players:
        sum += p.score
    for p in players:
        p.fitness = (mth.pow(p.check_piont, 2) * p.score / sum) * am_of_players
        # p.fitness = (mth.pow(p.check_piont, 2) * p.score)
        # p.fitness = p.score / sum


@window.event
def on_draw():
    # if gen % 10 == 0:
    window.clear()
    label.draw()
    for p in players:
        if not p.dead:
            # p.sprite.draw()
            for line in p.boundries:
                    draw_line([ line[0], line[1] ], [ line[2], line[3] ], (255,0,0,255))
    for w in walls:
        draw_line(w.start_pos, w.end_pos, w.color)
    for ch in checkpoints:
        draw_line(ch.start_pos, ch.end_pos, ch.color)
    

def update(delta_time):
    global gen
    global players
    for i in range(cycles):
        if all_dead(players):
            
            players = repopulate(players)
            gen += 1
            
            gen_table.append(gen-1)
            label.text = (str("gen: " + str(gen) + " players: " + str(len(players))))

            # plot of fitness and score
            fig, axs = plt.subplots(2, 1)
            axs[0].plot(gen_table, avr_fitness_table, gen_table, best_fitness_table)
            axs[0].set_xlim(0, len(gen_table)-1)
            axs[0].set_xlabel('gen.')
            axs[0].set_ylabel('avr. fitness, best fitness')
            axs[0].grid(True)

            axs[1].plot(gen_table, avr_score_table, gen_table, best_score_table)
            axs[1].set_xlim(0, len(gen_table)-1)
            axs[1].set_xlabel('gen.')
            axs[1].set_ylabel('avr. score, best score')
            axs[1].grid(True)
                            
            if gen % graph_cycles == 0:
                fig.tight_layout()
                fig.savefig("graph.png")

            


        for p in players:
            if not p.dead:
                p.cast_rays(walls)
                p.set_net_input()
                p.move(delta_time)
                p.check_for_hit(walls, checkpoints)
                p.out_off_bounds(window.width, window.height)
                
    
                
        

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()