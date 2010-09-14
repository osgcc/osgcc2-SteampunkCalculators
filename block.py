#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("./artSource/floor.bmp", -1)
        self.rect.topleft = level.tileToScreenCoords(x,y)
        self.level = level
        self.name = "Block"

    def update(self, camera_dx, camera_dy):
        self.rect = self.rect.move(camera_dx, camera_dy)
        
    def tick(self, player):
        pass
        
    def onCollision(self, obj):
        if(self.rect.collidepoint(obj.rect.topleft)):
            obj.ulHit = self.rect
        if(self.rect.collidepoint(obj.rect.bottomleft)):
            obj.llHit = self.rect
        if(self.rect.collidepoint(obj.rect.topright)):
            obj.urHit = self.rect
        if(self.rect.collidepoint(obj.rect.bottomright)):
            obj.lrHit = self.rect

            
    def writeToFile(self, f):
        f.write(self.name + " ")
        x, y = self.level.screenToTileCoords(self.rect.left, self.rect.top)
        f.write(str(x) + " " + str(y))
        f.write("\n");