#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, lifetime=10, vel=Vector(0,-40), fileName="./artSource/steam.bmp"):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_alpha_image(fileName, -1)
        self.fileName = fileName
        self.x = float(x)
        self.y = float(y)
        self.image, self.rect = load_image(fileName, -1)
        self.rect.centerx = x
        self.rect.centery = y
        self.name = "Particle"
        self.velocity = vel
        self.endtime = lifetime
        self.curtime = 0
        self.destroyed=0
        
    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(camera_dx, camera_dy)
        self.x += float(camera_dx)
        self.y += float(camera_dy)
        
    def tick(self, player):
        pass
        
    def particle_tick(self, time):
        delta = self.velocity*float(time)
        self.x += float(delta.x)
        self.y += float(delta.y)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.curtime += time
        if(self.curtime > self.endtime):
            self.destroyed = 1
            return
        self.image.set_alpha(int(255*(1-float(self.curtime)/self.endtime)))
        #print(self.image.get_alpha())
        