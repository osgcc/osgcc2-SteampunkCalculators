#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from vector import *

screenHeight = 600
screenWidth = 800
levelHeight = 1200
levelWidth = 1600

GRID_WIDTH = 32
LEVEL_FILE = "./levels/level1.txt"

BLOCK_TYPE, VENT_TYPE, THING_TYPE, PARTICLE_TYPE, SPIKE_TYPE, GOAL_TYPE = range(1,7)

def load_image(name, colorkey=None):
    path, this_file = os.path.split(sys.argv[0])
    fullname = os.path.join(path, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_alpha_image(name, colorkey=None):
    path, this_file = os.path.split(sys.argv[0])
    fullname = os.path.join(path, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    return image, image.get_rect()


