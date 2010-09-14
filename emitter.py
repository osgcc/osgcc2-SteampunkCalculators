#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
from particle import *

class Emitter(pygame.sprite.RenderPlain):
    def __init__(self,x,y,level,particle,lifetime=10, vec=Vector(0,-1), rate=10, phi=math.pi/8, xrange=30, yrange=5):
        pygame.sprite.RenderPlain.__init__(self,())
        self.pos = Vector(x,y)
        self.level = level
        self.endtime = lifetime
        self.curtime = 0
        self.dir = vec
        self.phi = phi
        self.xrange = xrange
        self.yrange=yrange
        self.particle = particle
        self.rate = rate
        self.destroyed = 0
        
    def update(self, camera_dx, camera_dy):
        self.pos.x += camera_dx
        self.pos.y += camera_dy
##        for p in self:
##            p.update(camera_dx, camera_dy)

    def kill(self):
        for p in self:
            self.remove(p)
            self.level.remove(p)
            del(p)
        self.destroyed = 1
        
    def tick(self, time):
        if(self.destroyed):
##            self.kill()
            return
        for p in self:
            if p.destroyed:
                self.remove(p)
                self.level.remove(p)     
        
        somethingExists = False
        for p in self:
            somethingExists = True
            p.particle_tick(time)
            
        if(self.endtime > 0):
            self.curtime += time
            #print(float(self.curtime) / float(self.endtime))
            if(self.curtime > self.endtime):
                self.kill()
                return
        
        if(random.random() < self.rate*time):
            #print("added particle")
            x = self.pos.x
            y = self.pos.y
            scatter = Vector(1,0).rotate(2 * math.pi * random.random())
            scatter.x *= self.xrange
            scatter.y *= self.yrange
            scatter *= random.random()
            x += scatter.x
            y += scatter.y
            vel = self.dir
            angle = random.random() * float(self.phi)
            if(random.random() < 0.5):
                angle *= float(-1)
            vel = vel.rotate(angle)
            p = Particle(x, y, self.particle.endtime, vel, self.particle.fileName)
            self.level.add(p)
            self.add(p)
        
        
        