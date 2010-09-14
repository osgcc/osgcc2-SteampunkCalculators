#!/usr/bin/env python

import os, sys, pygame
from pygame.locals import *
import random
from util import *
import player
import level
from particle import *
import vector
from enemy import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

path, this_file = os.path.split(sys.argv[0])

HEIGHT = screenHeight
WIDTH = screenWidth

camera_x = 0
camera_y = 0

levelNum = 1

UP, RIGHT, DOWN, LEFT = range(0,4)
FACES = ["up", "right", "down", "left"]

class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("artSource/crosshair.png", -1)
    
    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

def gravity(sprite):
    #pass
    if sprite.dy < 10:
        sprite.dy += 1

def main(levelName):
    pygame.init()
    pygame.font.init()
    #pygame.mixer.pre_init(44100, -16, 2, 4048)
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Steam Calc')
    pygame.mouse.set_visible(False)
    #pygame.key.set_repeat(10, 100)
    
    font = pygame.font.SysFont("Times", 40)
    score_text = '0'
    score_size = font.size(score_text)

    pygame.mixer.music.load("oggs/03 Ghosts I.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    #score = font.render(score_text, 1, (250, 0, 0))

    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill((250, 250, 250))
    
    (background, _) = load_image("bg.bmp", -1)

    screen.blit(background, (0, 0))
    #screen.blit(score, (10, 10))
    pygame.display.flip()
    
    clock = pygame.time.Clock()

    the_level = level.Level(levelName)

    the_guy = player.Guy(the_level)
    camera_x = screenWidth / 2
    camera_y = screenHeight / 2

    guy_group = pygame.sprite.RenderPlain((the_guy,))

    bullets = pygame.sprite.RenderPlain()
    
    particles = pygame.sprite.RenderPlain()
    emitters = []

    things = pygame.sprite.RenderPlain(the_level.thing)
    goals = pygame.sprite.RenderPlain(the_level.goal)
    
    enemies = pygame.sprite.RenderPlain(Enemy(the_guy))
    for i in (range(0,30)):
        enemies.add(Enemy(the_guy))

    (mx, my) = pygame.mouse.get_pos()
    cursor = pygame.sprite.RenderPlain(Cursor(mx, my))

    reload_time = 5
    mType = 1

    while 1:
        clock.tick(60)
        for p in particles:
            p.particle_tick(float(60)/1000)
        for e in emitters:
            e.tick(float(60)/1000)
            
        if(random.random() < 0.01):
            #print("Makin a dude")
            enemies.add(Enemy(the_guy))
        
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] or pressed[K_a]:
            the_guy.move(LEFT)
        elif pressed[K_RIGHT] or pressed[K_d]:
            the_guy.move(RIGHT)
        
        if pressed[K_UP] or pressed[K_w]:
            the_guy.move(UP)

        #if pressed[K_SPACE]:
        #    reload_time -= 1
        #    if reload_time <= 0:
        #        mx, my = pygame.mouse.get_pos()
        #        mv = vector.Vector(mx - the_guy.rect.centerx, my - the_guy.rect.centery)
        #        the_guy.shoot(bullets, mv)
        #        reload_time = 5
        #else:
        #    reload_time = 10
            
        mb1,mb2,mb3 = pygame.mouse.get_pressed()

        if mb1:
            mx, my = pygame.mouse.get_pos()
            mv = vector.Vector(mx - the_guy.rect.centerx, my - the_guy.rect.centery)
            the_guy.shoot(bullets, mv)
        else:
            the_guy.reload()

        if(mb3):
            mX, mY = pygame.mouse.get_pos()
            if(mType==PARTICLE_TYPE):
                p = Particle(x=mX,y=mY)
                particles.add(p)
            else:
                the_level.makeTile(mX,mY,mType)
        if(mb2):
            mX, mY = pygame.mouse.get_pos()
            the_level.deleteTile(mX,mY)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                #pressed = pygame.key.get_pressed()
                if event.key == K_ESCAPE:
                    sys.exit(0)
                    
                elif event.key == pygame.K_1:
                    mType = BLOCK_TYPE
                elif event.key == pygame.K_2:
                    mType = VENT_TYPE
                elif event.key == pygame.K_3:
                    mType = THING_TYPE
                elif event.key == pygame.K_4:
                    mType = PARTICLE_TYPE
                elif event.key == pygame.K_5:
                    mType = SPIKE_TYPE
                elif event.key == pygame.K_6:
                    mType = GOAL_TYPE
                elif event.key == pygame.K_0:
                    the_guy.jp_fuel += 10000

                elif event.key == pygame.K_c:
                    the_level.save(LEVEL_FILE)
                elif event.key == pygame.K_l:
                    the_level.load(LEVEL_FILE)
                elif event.key == pygame.K_g:
                    the_guy.gun_type = ((1 + the_guy.gun_type) % 2)

            elif event.type == KEYUP:
                if event.key == K_UP:
                    the_guy.move(DOWN) # Reuse down for "Not going up"
            
        for bullet in bullets:
            if bullet.destroy == 1:
                bullets.remove(bullet)
                
        for p in particles:
            if p.destroyed == 1:
                particles.remove(p)
                
        for e in emitters:
            if e.destroyed == 1:
                emitters.remove(e)
                e.kill()
                del(e)

        #If person isn't on a floor
        gravity(the_guy)
        the_level.tick(the_guy)

        guy_group.update()

        
        for bad_things in (the_level.deadly_collision_grp, enemies):
            if pygame.sprite.groupcollide(guy_group, bad_things, 0, 0):
                guy_group.remove(the_guy)

                #the_guy = player.Guy(the_level, lives=(the_guy.lives - 1))
                return (screen, False)
        
        #pygame.sprite.groupcollide(bullets, the_level, 0, 0)
        for collection in (bullets, enemies):
            colliding_bullets = pygame.sprite.groupcollide(collection, the_level.collision_group, 0, 0)
            if colliding_bullets:
                for b in colliding_bullets:
                    b.beginCollision()
                for b in colliding_bullets:
                    for wall in colliding_bullets[b]:
                        wall.onCollision(b)
                    b.endCollision()
            
        hit_walls = pygame.sprite.groupcollide(the_level.collision_group, guy_group, 0, 0)
        if hit_walls:
            the_guy.beginCollision()
            for wall in hit_walls:
                wall.onCollision(the_guy)
            the_guy.endCollision()

        touched_things = pygame.sprite.groupcollide(things, guy_group, 0, 0)
        for thing in touched_things:
            the_guy.carry(thing)
            
        end_goal = pygame.sprite.groupcollide(goals, guy_group, 0, 0)
        for goal in end_goal:
            return screen, True
            
        cList = pygame.sprite.groupcollide(enemies, bullets, 0, 0)
        for e in cList:
            emitters.append(e.explode())
        cList = pygame.sprite.groupcollide(enemies, bullets, 1, 1)

        camera_dx = camera_x - the_guy.rect.centerx
        camera_dy = camera_y - the_guy.rect.centery

        camera_x = screenWidth / 2
        camera_y = screenHeight / 2
        
        #print camera_dx, camera_dy, camera_x, camera_y
        bullets.update(camera_dx, camera_dy)
        things.update(camera_dx, camera_dy)
        goals.update(camera_dx, camera_dy)
        the_level.update(camera_dx, camera_dy)
        particles.update(camera_dx, camera_dy)
        for e in emitters:
            e.update(camera_dx, camera_dy)
        enemies.update(camera_dx, camera_dy)
        
        (mx, my) = pygame.mouse.get_pos()
        cursor.update(mx, my)

        screen.blit(background, (0, 0))
	
        the_level.draw(screen)
        bullets.draw(screen)
        things.draw(screen)
        goals.draw(screen)
        particles.draw(screen)
        enemies.draw(screen)

        the_guy.setCenterPos(screenWidth / 2,screenHeight / 2)

        guy_group.draw(screen)

        cursor.draw(screen)
        
        #score = font.render(str(zombie_count), 1, (250, 0, 0))
        #screen.blit(score, (10, 5))

        pygame.display.flip()
        
def game_over(screen, success):
    global levelNum
    font = pygame.font.SysFont("Times", 80)
    text = 'Game Over'
    if(success):
        if(levelNum==4):
            text = 'You Beat The GAMWE!'
        else:
            text = 'You Beat The Level!'
        levelNum += 1
    size = font.size(text)
    
    ren = font.render(text, 1, (250, 0, 0))
    
    screen.blit(ren, (170, 200))
    pygame.display.flip()
    pygame.event.clear()
    
    event = pygame.event.wait()
    if event.type == KEYDOWN and event.key == K_RETURN:
        if(levelNum==5):
            sys.exit(0)
        return
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        sys.exit(0)
    elif event.type == QUIT:
        sys.exit(0)
    
if __name__ == '__main__': 
    while(1):
        (screen, b) = main("./levels/level"+str(levelNum)+".txt")
        game_over(screen, b)
    
