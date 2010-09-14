import os, sys, pygame
from pygame.locals import *
import random
from block import *
from emitter import *

class Spike(Block):
    def __init__(self, x, y, level):
        Block.__init__(self, x, y, level)
        self.image, _ = load_image("./artSource/spike.bmp", -1)
        self.name = "Spike"
