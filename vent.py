#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from block import *
from emitter import *

class Vent(Block):
    def __init__(self, x, y, level):
        Block.__init__(self, x, y, level)
        self.image, _ = load_image("./artSource/wall.bmp", -1)
        self.name = "Vent"
        self.MAX_HEIGHT = 350
        self.FORCE = 4
        self.particle = Particle(lifetime=10, fileName="./artSource/steam.bmp")
        x,y = level.tileToScreenCoords(x,y)
        self.emitter = Emitter(x,y,level,self.particle,lifetime=0, vec=Vector(0,-40), rate=4, phi=math.pi/12, xrange=10, yrange=5)
        
    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(camera_dx, camera_dy)
        self.emitter.update(camera_dx, camera_dy)
        
    def tick(self, player):
        self.emitter.tick(float(60)/1000)
        if((player.rect.centerx < self.rect.right) and (player.rect.centerx > self.rect.left)):
            if(player.rect.centery < self.rect.top):
                height = self.rect.top - player.rect.centery
                #print(height)
                if(height > self.MAX_HEIGHT):
                    return
                impulse = self.FORCE * ((self.MAX_HEIGHT - height) / self.MAX_HEIGHT)
                #player.dy -= impulse
                if player.dy > -15:
                    player.dy -= 5
                