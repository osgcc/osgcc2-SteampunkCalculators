#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
from block import *
from vent import *
from spike import *
from player import *

X_DIM = levelWidth/GRID_WIDTH
Y_DIM = levelHeight/GRID_WIDTH

class Level(pygame.sprite.RenderPlain):
    def __init__(self, levelName ):
        self.origin = None
        self.collision_group = None
        self.deadly_collision_grp = None
        self.goal = None
        self.thing = None
        #self.collision_group = pygame.sprite.RenderPlain()
        #self.deadly_collision_grp = pygame.sprite.RenderPlain()
        #self.initMatrix()
        pygame.sprite.RenderPlain.__init__(self,())
        #self.makeBorderTiles()
        #self.origin = self.matrix[0][0]
        self.load(levelName)
       
    def clear(self):
        self.remove(self)
        if(self.collision_group != None):
            self.collision_group.remove(self.collision_group)
        if(self.deadly_collision_grp != None):
            self.deadly_collision_grp.remove(self.deadly_collision_grp)
        del(self.collision_group)
        del(self.deadly_collision_grp)
        del(self.goal)
        del(self.thing)
        self.goal = None
        self.thing = None
        self.collision_group = pygame.sprite.RenderPlain()
        self.deadly_collision_grp = pygame.sprite.RenderPlain()
        
    def initMatrix(self):
        self.matrix = {}
        for x in (range(0,X_DIM)):
            self.matrix[x] = {}
            
    def makeBorderTiles(self):
        for x in (range(0,X_DIM)):
            self.insertTile(1,x,0)
            self.insertTile(1,x,Y_DIM-1)
            
        for y in (range(0,Y_DIM)):
            self.insertTile(1,0,y)
            self.insertTile(1,X_DIM-1,y)
            
        self.fixBlockImages()
        
    def fixBlockImages(self):
        for x in (range(0,X_DIM)):
            for y in (range(0,Y_DIM)):
                if(not self.matrix[x].has_key(y)):
                    continue
                obj = self.matrix[x][y]
                up,left,down,right = False,False,False,False
                if((x!=0) and (self.matrix[x-1].has_key(y))):
                    left=True
                if((x!=X_DIM-1) and (self.matrix[x+1].has_key(y))):
                    right=True
                if((y!=0) and (self.matrix[x].has_key(y-1))):
                    up=True
                if((y!=Y_DIM-1) and (self.matrix[x].has_key(y+1))):
                    down=True
                    
                if(not left and not right):
                    obj.image,_ = load_image("./artSource/wall.bmp", -1)
                elif(not up and not down):
                    obj.image,_ = load_image("./artSource/floor.bmp", -1)
                elif(up or down or left or right):
                    if(left and up):
                        obj.image,_ = load_image("./artSource/lr_corner.bmp", -1)
                    elif(left and down):
                        obj.image,_ = load_image("./artSource/ur_corner.bmp", -1)
                    elif(right and up):
                        obj.image,_ = load_image("./artSource/ll_corner.bmp", -1)
                    elif(right and down):
                        obj.image,_ = load_image("./artSource/ul_corner.bmp", -1)
        
    def makeTile(self,mx,my,type):
        x,y = self.screenToTileCoords(mx,my)
        self.insertTile(type,x,y)
        
    def deleteTile(self,mx,my):
        x,y = self.screenToTileCoords(mx,my)
        if(not self.matrix[x].has_key(y)):
            return
        
        self.remove(self.matrix[x][y])
        self.collision_group.remove(self.matrix[x][y])
        del(self.matrix[x][y])
        
    def tick(self, player):
        for obj in self:
            obj.tick(player)
        
    def insertTile(self,type,x,y):
        if(x < 0 or x >= X_DIM):
            return
        if(y < 0 or y >= Y_DIM):
            return
        if(self.matrix[x].has_key(y)):
            return
        
        obj = None
        if(type==BLOCK_TYPE):
            obj = Block(x,y,self)
        elif(type==VENT_TYPE):
            obj = Vent(x,y,self)
        elif(type==THING_TYPE):
            self.thing.rect.centerx, self.thing.rect.centery = self.tileToScreenCoords(x,y)
            return
        elif type == SPIKE_TYPE:
            obj = Spike(x, y, self)
        elif(type==GOAL_TYPE):
            self.goal.rect.centerx, self.goal.rect.centery = self.tileToScreenCoords(x,y)
            return

        if(obj == None):
            print("Bad tile type!")
            return
        
        self.matrix[x][y] = obj
        self.add(obj)
        if type == SPIKE_TYPE:
            self.deadly_collision_grp.add(obj)
        else:
            self.collision_group.add(obj)
            
    def save(self, fileName):
        f = open(fileName, 'w')
        for x in (range(0,X_DIM)):
            for y in (range(0,Y_DIM)):
                if(not self.matrix[x].has_key(y)):
                    continue
                obj = self.matrix[x][y]
                obj.writeToFile(f)
        x,y = self.screenToTileCoords(self.goal.rect.centerx, self.goal.rect.centery)
        f.write("Goal " + str(x) + " " + str(y) + "\n")
        x,y = self.screenToTileCoords(self.thing.rect.centerx, self.thing.rect.centery)
        f.write("Thing " + str(x) + " " + str(y) + "\n")
        
    def load(self, fileName):
        self.origin = None
        self.clear()
        self.initMatrix()
        gx,gy = 200,200
        gdefined = False
        tx,ty = 600,200
        tdefined = False
        f = open(fileName, 'r')
        for line in f:
            args = line.split(" ")
            if(args[0] == "Goal"):
                gx,gy = int(args[1]),int(args[2]);
                gdefined = True
            elif(args[0] == "Thing"):
                tx,ty = int(args[1]),int(args[2]);
                tdefined = True
            else:
                type = 1
                if(args[0] == "Block"):
                    type = 1
                elif(args[0] == "Vent"):
                    type = 2
                elif args[0] == "Spike":
                    type = SPIKE_TYPE
                self.insertTile(type,int(args[1]),int(args[2]))
        self.origin = self.matrix[0][0]
        if(gdefined):
            x,y = self.tileToScreenCoords(gx,gy)
            self.goal = Goal(x,y)
        if(tdefined):
            x,y = self.tileToScreenCoords(tx,ty)
            self.thing = Thing(x,y)
        if(self.goal == None):
            self.goal = Goal(600,200)
        if(self.thing == None):
            self.thing = Thing(200,200)
        
    def screenToTileCoords(self,mx,my):
        if(not self.origin):
            print("pygame.origin must be defined to call this!")
            return 0,0
        mx -= self.origin.rect.left
        my -= self.origin.rect.top
        x = mx / GRID_WIDTH
        y = my / GRID_WIDTH
        return x,y

    def tileToScreenCoords(self,mx,my):
        mx *= GRID_WIDTH
        my *= GRID_WIDTH
        #NOTE:  this is tricky, it is necessary for the setup to work right
        if(not self.origin):
            return mx,my
        mx += self.origin.rect.left
        my += self.origin.rect.top
        return mx,my 
    
    def count_parts(self):
        pass
