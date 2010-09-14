#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
from math import *
from collidable import *
from emitter import *
from player import *
import level

class Enemy(Bullet):
    def __init__(self, guy):
        Bullet.__init__(self, guy, Vector(1,0).rotate(2 * math.pi * random.random()))
        self.speed = 5
        self.image, self.rect = load_image("calculator.bmp", -1)
        self.rect.center = guy.level.tileToScreenCoords(random.randint(0,level.X_DIM-1),random.randint(0,level.Y_DIM-1))
        self.particle = Particle(lifetime=2, fileName="./artSource/steam.bmp")
        
    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(self.dx + camera_dx, self.dy + camera_dy)
        if(random.random() < 0.01):
            self.setVec(Vector(1,0).rotate(2 * math.pi * random.random()))
        else:
            self.setVec(self.vec.rotate(((random.random() * math.pi / 16)) - (math.pi / 32)))
        
    def doImpact(self, newVec):
        newVec = Vector(self.dx,self.dy)
        self.setVec(newVec)
        
    def explode(self):
        #print("EXPLODE")
        return Emitter(self.rect.centerx,self.rect.centery,self.guy.level,self.particle,lifetime=4, vec=Vector(1,0), rate=80, phi=math.pi, xrange=40, yrange=40)
        
