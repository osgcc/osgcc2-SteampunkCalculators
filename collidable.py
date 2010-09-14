#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
from math import *

class Collidable():
    def __init__(self):
        pass
        
    def beginCollision(self):
        self.ulHit = None
        self.urHit = None
        self.llHit = None
        self.lrHit = None
        
    def endCollision(self):
        contacts = 0
        if(self.ulHit):
            contacts += 1
        if(self.llHit):
            contacts += 1
        if(self.urHit):
            contacts += 1
        if(self.lrHit):
            contacts += 1
            
        negateX, negateY = False, False
        if(contacts == 1):
            if(self.ulHit):
                xDist = fabs(self.ulHit.right - self.rect.left)
                yDist = fabs(self.ulHit.bottom - self.rect.top)
                if(xDist > yDist):
                    self.rect.top = self.ulHit.bottom
                    negateY = True
                else:
                    self.rect.left = self.ulHit.right
                    negateX = True
            if(self.urHit):
                xDist = fabs(self.urHit.left - self.rect.right)
                yDist = fabs(self.urHit.bottom - self.rect.top)
                if(xDist > yDist):
                    self.rect.top = self.urHit.bottom
                    negateY = True
                else:
                    self.rect.right = self.urHit.left
                    negateX = True
            if(self.llHit):
                xDist = fabs(self.llHit.right - self.rect.left)
                yDist = fabs(self.llHit.top - self.rect.bottom)
                if(xDist > yDist):
                    self.rect.bottom = self.llHit.top
                    negateY = True
                else:
                    self.rect.left = self.llHit.right
                    negateX = True
            if(self.lrHit):
                xDist = fabs(self.lrHit.left - self.rect.right)
                yDist = fabs(self.lrHit.top - self.rect.bottom)
                if(xDist > yDist):
                    self.rect.bottom = self.lrHit.top
                    negateY = True
                else:
                    self.rect.right = self.lrHit.left
                    negateX = True
        elif(contacts == 2):
            if(self.ulHit and self.urHit):
                self.rect.top = self.ulHit.bottom
                negateY = True
            elif(self.llHit and self.lrHit):
                self.rect.bottom = self.llHit.top
                negateY = True
            elif(self.llHit and self.ulHit):
                self.rect.left = self.llHit.right
                negateX = True
            elif(self.lrHit and self.urHit):
                self.rect.right = self.lrHit.left
                negateX = True
        elif(contacts == 3):
            negateY = True
            negateX = True
            if(self.ulHit and self.llHit and self.lrHit):
                self.rect.bottomleft = self.llHit.topright
            elif(self.urHit and self.ulHit and self.llHit):
                self.rect.topleft = self.ulHit.bottomright
            elif(self.lrHit and self.urHit and self.ulHit):
                self.rect.topright = self.urHit.bottomleft
            elif(self.llHit and self.lrHit and self.urHit):
                self.rect.bottomright = self.lrHit.topleft
        else:
            print("You're screwed")
            
        origVec = Vector(self.dx,self.dy)
        if(negateX):
            self.dx = -1 * self.elasticity * self.dx
        if(negateY):
            self.dy = -1 * self.elasticity * self.dy
        newVec = Vector(self.dx,self.dy)
        newVec = (origVec + newVec) / float(2)
        self.doImpact(newVec)
        
        