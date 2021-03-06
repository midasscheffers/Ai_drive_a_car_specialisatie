from ray import *
from network import *
import math as mth
import random as r
import pyglet

class Player:

    def __init__(self, pos, amount_of_rays, selected):
        self.net = Network([amount_of_rays + 1, 16, 16, 2])
        self.net_input = []
        self.fitnes = 0
        self.pos = pos
        self.vel = [1, 0]
        self.accel = [0, 0]
        self.rot = 0
        self.dead = False
        self.size = 20
        self.selected = selected
        self.img = pyglet.resource.image("car.png")
        self.img.width = self.size * 2
        self.img.height = self.size
        self.img.anchor_x = self.img.width/2
        self.img.anchor_y = self.img.height/2
        self.sprite = pyglet.sprite.Sprite(self.img)
        self.speed = 100
        self.rot_speed = 100
        self.amount_of_rays = amount_of_rays
        self.rays = []
        self.detections = []
        self.ray_pts = []
        for i in range(0, amount_of_rays):
            self.rays.append(Ray(self.pos, mth.radians((360/self.amount_of_rays)*i)))
            self.detections.append(0)
            self.ray_pts.append([0,0])
    

    def move(self, delta_time):
        net_out = self.net.run(True)
        if net_out[1] == 0:
            self.rot += net_out[0] * self.rot_speed * delta_time
        else:
            self.rot -= net_out[0] * self.rot_speed * delta_time
        # self.rot +=r.random() * self.rot_speed * delta_time
        # self.rot += self.rot_speed
        self.sprite.rotation = -self.rot
        self.accel[0] = mth.cos(mth.radians(self.rot))
        self.accel[1] = mth.sin(mth.radians(self.rot))
        self.vel[0] = self.accel[0]
        self.vel[1] = self.accel[1]
        # self.vel[0] = max(-1, min(self.vel[0], 1))
        # self.vel[1] = max(-1, min(self.vel[1], 1))
        self.pos[0] += self.vel[0] * self.speed * delta_time
        self.pos[1] += self.vel[1] * self.speed * delta_time
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
        for r in self.rays:
            r.pos = self.pos


    def check_for_hit(self):
        for i in range(len(self.detections)):
            if self.detections[i] < self.size:
                self.dead = True
                break



    def set_net_input(self):
        self.net_input = []
        self.net_input.append(self.rot)
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
                    dist = mth.pow(self.pos[0]-pt[0], 2) + mth.pow(self.pos[1]-pt[1], 2)
                    if dist < record:
                        record = dist
                        closest = pt

            if not closest == False:
                if self.selected:
                    pass
                    # pygame.draw.line(
                    #     gameDisplay,
                    #     green,
                    #     [int(self.pos[0]), int(self.pos[1])],
                    #     [int(closest[0]), int(closest[1])]
                    # )
                self.detections[i] = record
                self.ray_pts[i] = closest
            else:
                self.detections[i] = 99999999999

    def map_to_range(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)