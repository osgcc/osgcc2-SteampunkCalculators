#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
from math import *
from collidable import *
from emitter import *
from vector import *

UP, RIGHT, DOWN, LEFT = range(0,4)
PISTOL, SHOTGUN = range(0, 2)

class Guy(pygame.sprite.Sprite, Collidable):
    def __init__(self, level, lives=3):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("dot.right.bmp", -1)
        self.img_left, self.rect_left = load_image("dot.left.bmp", -1)
        self.img_right, self.rect_right = load_image("dot.right.bmp", -1)
        self.img_jpon_r, self.rect_jpon_r = load_image("dot.right.on.bmp", -1)
        self.img_jpon_l, self.rect_jpon_l = load_image("dot.left.on.bmp", -1)

        self.dx = 0
        self.dy = 0
        self.elasticity = 0
        self.level = level
        
        self.direction = RIGHT

        self.carrying = None # A Sprite to hold over head (can't shoot)

        self.rect = self.rect.move(60, 0)

        self.gun_sound = pygame.mixer.Sound("gun.wav")
        self.sound_playing = False
        self.shotgun_sound = pygame.mixer.Sound("shotgun.wav")

        self.lives = lives
        self.jp_fuel = 10

        self.gun_type = PISTOL
        self.reload_time = 10

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)
        
        if self.carrying:
            self.carrying.rect = self.carrying.rect.move(self.dx, self.dy)

        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
                    

        if self.dx > 0:
            self.dx -= 1
        elif self.dx < 0:
            self.dx += 1
        
        if self.dy < 0:
            self.dy += 1

    def move(self, new_direction):
        
        if new_direction == LEFT:
            self.image = self.img_left
            self.direction = LEFT

            if self.dx > -10:
                self.dx -= 2

        elif new_direction == RIGHT:
            self.image = self.img_right
            self.direction = RIGHT
            if self.dx < 10:
                self.dx += 2

        if new_direction == UP and self.jp_fuel > 0:
            if self.dy > -15:
                self.dy -= 5
            if self.direction == RIGHT:
                self.image = self.img_jpon_r
            else:
                self.image = self.img_jpon_l
            self.jp_fuel -= 1

        elif new_direction == DOWN:
            if self.direction == RIGHT:
                self.image = self.img_right
            else:
                self.image = self.img_left

    def shoot(self, bullets, mv):
        if not self.carrying:
            self.reload_time -= 1
            if self.reload_time <= 0:
                if self.gun_type == PISTOL:
                    bullets.add(Bullet(self, mv))
                    if True:#not self.sound_playing:
                        self.gun_sound.play()
                    self.reload_time = 5
                else:
                    bullets.add((Bullet(self, mv + 
                                        Vector(0,
                                               -20)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               -15)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               -10)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               -5)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               +5)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               +10)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               +15)),
                                 Bullet(self, mv + 
                                        Vector(0,
                                               +20))))
                    if True: #not self.sound_playing:
                        self.shotgun_sound.play()

                    self.reload_time = 20

    def reload(self):
        self.reload_time = 10

    def carry(self, thing):
        self.carrying = thing
        thing.rect.bottom = self.rect.top
        thing.rect.left = self.rect.left
        
    def setCenterPos(self,x,y):
        self.rect.centerx = x
        self.rect.centery = y
        if(self.carrying):
            self.carrying.rect.centerx = x
            self.carrying.rect.centery = y
            
    def doImpact(self, vec):
        if vec.y > 0.9:
            self.jp_fuel = 10
            
            
class Bullet(pygame.sprite.Sprite, Collidable):
    def __init__(self, guy, mv):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet.bmp", -1)
        self.rect.center = guy.rect.center
        self.destroy = 0
        
        self.elasticity = 1
        self.speed = 15
        self.guy = guy
        self.particle = Particle(lifetime=1, fileName="./artSource/steam.bmp")
        
        self.setVec(mv)
            
        self.emitter = None
        
    def setVec(self, vec):
        self.vec = vec
        self.dx = int(cos(vec.angle()) * self.speed)
        self.dy = int(sin(vec.angle()) * self.speed)
        
        if vec.y < 0:
            self.dy *= -1
        

    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(self.dx + camera_dx, self.dy + camera_dy)

        if (self.rect.centerx > levelWidth or
            self.rect.centery > levelHeight or
            self.rect.centerx < 0 or
            self.rect.centery < 0):

            self.destroy = 1
            if(self.emitter != None):
                self.emitter.kill()
                del(self.emitter)
                self.emitter = None
            
        if(self.emitter != None):
            self.emitter.tick(float(60)/1000)
            self.emitter.update(camera_dx, camera_dy)
            
    def doImpact(self, newVec):
        if(self.emitter != None):
            self.emitter.kill()
            del(self.emitter)
        self.emitter = Emitter(self.rect.centerx,self.rect.centery,self.guy.level,self.particle,lifetime=2, vec=newVec.unit()*40, rate=40, phi=math.pi/4, xrange=5, yrange=5)

class Thing(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image("thing.bmp", (0xFF, 0x00, 0xBB))
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(camera_dx, camera_dy)
        
class Goal(Thing):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image("goal.bmp", (0xFF, 0x00, 0xBB))
        self.rect.centerx = x
        self.rect.centery = y
