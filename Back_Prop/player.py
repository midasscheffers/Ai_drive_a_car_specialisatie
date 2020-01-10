from ray import *
from network import *
import math as mth
import random as r
import pyglet

class Player:

    def __init__(self, pos, amount_of_rays, ray_degrees, selected):
        # variables for player
            # network
        self.net = Network([amount_of_rays, 2, 3])
        self.net_input = []
        self.amount_of_rays = amount_of_rays
        self.rays = []
        self.detections = []
        self.ray_pts = []
        self.ray_degrees = ray_degrees
        self.fitness = 1
        self.check_piont = 1
        self.score = 0
        self.times_finished = 0
            # game
        self.pos = pos
        self.vel = [1, 0]
        self.accel = [0, 0]
        self.rot = 0
        self.dead = False
        self.size = 20
        self.speed = 120
        self.rot_speed = 125
        self.boundries = []
        self.touching_finish = False
            # draw
        self.color = (255,0,0,255)
        self.selected = selected
        self.img = pyglet.resource.image("car.png")
        self.img.width = self.size * 2
        self.img.height = self.size
        self.img.anchor_x = self.img.width/2
        self.img.anchor_y = self.img.height/2
        self.sprite = pyglet.sprite.Sprite(self.img)
        # add img boundries to list
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], self.img.width/2, self.img.height/2, -self.img.width/2, -self.img.height/2])
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], -self.img.width/2, self.img.height/2, self.img.width/2, -self.img.height/2])
        #create rays
        for i in range(0, amount_of_rays):
            self.rays.append(Ray(self.pos, mth.radians((ray_degrees/self.amount_of_rays)*i - ray_degrees/2))) #+mth.radians()
            self.detections.append(0)
            self.ray_pts.append([0,0])
    

    def move(self, delta_time):
        temp_rot = self.rot
        temp_pos = self.pos
        net_out = self.net.run(True)
        if net_out[1] == 0:
            self.rot += net_out[0] * self.rot_speed * delta_time
        elif net_out[1] == 1:
            pass
        elif net_out[1] == 2:
            self.rot -= net_out[0] * self.rot_speed * delta_time
        self.sprite.rotation = -self.rot
        self.accel[0] = mth.cos(mth.radians(self.rot))
        self.accel[1] = mth.sin(mth.radians(self.rot))
        self.vel[0] = self.accel[0]
        self.vel[1] = self.accel[1]
        self.pos[0] += self.speed * delta_time * self.vel[0]
        self.pos[1] += self.speed * delta_time * self.vel[1]
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
        self.move_boundries(temp_rot, temp_pos)
        for r in self.rays:
            r.pos = self.pos
            if net_out[1] == 0:
                r.rotate_ray(mth.radians(net_out[0] * self.rot_speed * delta_time))
            elif net_out[0] == 1:
                pass
            elif net_out[1] == 2:
                r.rotate_ray(mth.radians(net_out[0] * self.rot_speed * delta_time) * -1)
        self.score += 1


    def move_boundries(self, rot, old_pos):
        amount_of_rot = self.rot
        for line in self.boundries:
            line[0] = self.pos[0] + (line[4] * mth.cos(mth.radians(amount_of_rot))) - (line[5] * mth.sin(mth.radians(amount_of_rot)))
            line[1] = self.pos[1] + (line[4] * mth.sin(mth.radians(amount_of_rot))) + (line[5] * mth.cos(mth.radians(amount_of_rot)))
            line[2] = self.pos[0] + (line[6] * mth.cos(mth.radians(amount_of_rot))) - (line[7] * mth.sin(mth.radians(amount_of_rot)))
            line[3] = self.pos[1] + (line[6] * mth.sin(mth.radians(amount_of_rot))) + (line[7] * mth.cos(mth.radians(amount_of_rot)))

    def reset_rays(self):
        for i in range(0, len(self.rays)):
            r = self.rays[i]
            r.dir = 0
            r.rotate_ray(mth.radians((self.ray_degrees/self.amount_of_rays)*i - self.ray_degrees/2))


    def find_dis_out(self):
        best_detect = [0, 0]
        for i in range(len(self.detections)):
            if best_detect[1] < self.detections[i]:
                best_detect = [i, self.detections[i]]
        
        
        best_r = self.rays[best_detect[0]]
        best_r.color = (0, 255, 255, 255)

        our_rot = self.rot % 360
        ray_rot = mth.degrees(best_r.dir) % 360

        if ray_rot-our_rot < 180 and ray_rot-our_rot > 0:
            print(0)
            return 0
        else:
            print(2)
            return 2

        print(1)
        return 2


    def check_for_hit(self, walls):
        for line in self.boundries:
            for wall in walls:
                x1 = wall.start_pos[0]
                y1 = wall.start_pos[1]
                x2 = wall.end_pos[0]
                y2 = wall.end_pos[1]

                x3 = line[0]
                y3 = line[1]
                x4 = line[2]
                y4 = line[3]
                if self.lineline_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                    self.dead = True

            
                

                

    
    def lineline_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True
        return False


    def out_off_bounds(self, xmax, ymax):
        if self.pos[0] < 0 or self.pos[0] > xmax or self.pos[1] < 0 or self.pos[1] > ymax:
            self.dead = True



    def set_net_input(self):
        self.net_input = []
        for i in self.detections:
            self.net_input.append(i)
        self.net.set_input(self.net_input)
        

    def cast_rays(self, walls):
        for i in range(len(self.rays)):
            r = self.rays[i]
            closest = False
            record = 99999999999
            for w in walls:
                pt = r.cast(w)
                if not pt == False:
                    dist = mth.sqrt(mth.pow(self.pos[0]-pt[0], 2) + mth.pow(self.pos[1]-pt[1], 2))
                    if dist < record:
                        record = dist
                        closest = pt

            if not closest == False:
                self.detections[i] = record
                self.ray_pts[i] = closest
            else:
                self.detections[i] = 99999999999