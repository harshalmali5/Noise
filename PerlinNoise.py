#Import and Setup-------------------------------------------------------------------------------------------
import math as m
import noise
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame as p
import random as r
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0,30)
p.init()
p.display.set_caption('Pygame')

#Tweakable Variables----------------------------------------------------------------------------------------

#Functions--------------------------------------------------------------------------------------------------
def CreateColors():
    #Color scheme from https://flatuicolors.com/palette/us
    allColors = [
    (85, 239, 196),
    (129, 236, 236),
    (116, 185, 255),
    (162, 155, 254),
    (223, 230, 233),
    
    (0, 184, 148),
    (0, 206, 201),
    (9, 132, 227),
    (108, 92, 231),
    (178, 190, 195),
    
    (255, 234, 167),
    (250, 177, 160),
    (255, 118, 117),
    (253, 121, 168),
    (99, 110, 114),
    
    (253, 203, 110),
    (225, 112, 85),
    (214, 48, 49),
    (232, 67, 147),
    (45, 52, 54)
    ]
    numberOfColors = 20
    
    #Create list of random colors from allColors numberOfColors long
    colors = []
    for i in range(numberOfColors):
        index = r.randint(0, len(allColors)-1)
        colors.append(allColors[index])
        allColors.remove(allColors[index])
    return colors

def CreateMap(pnoise):
    octaves = r.randint(1,4)
    scale = r.randint(20,150)
    shape = (1920,1080)
    
    #Generate a 2d array with values from -1 to 1
    world = np.zeros((shape[1],shape[0]))
    for y in range(shape[1]):
        for x in range(shape[0]):
            if pnoise:
                world[y][x] = noise.pnoise2(y/scale, x/scale, octaves=octaves, persistence=0.5, lacunarity=2, repeatx=1024, repeaty=1024, base=0)
            else:
                world[y][x] = noise.snoise2(y/scale, x/scale, octaves=octaves, persistence=0.5, lacunarity=2, repeatx=1024, repeaty=1024, base=0)
    return world

def Draw(colors, frame, world):
    #Used to normalize height values, so if its from -0.8 to 0.8, it scales it
    coeff = 1/world.max()
    #How tall each color is
    interval = 1/len(colors)
    
    #Color all pixels
    for y in range(len(world)):
        for x in range(len(world[0])):
            #Height of pixel from 0-1
            h = (world[y][x]*coeff + 1)/2
            
            colored = False
            for i in range(len(colors)):
                if h < (i+1) * interval:
                    colored = True
                    w.set_at((x,y), colors[i])
                    break
            if not colored:
                w.set_at((x,y), colors[-1])
        p.display.update()
    #p.image.save(w, "Render/" + str(frame) + ".png")

#Variable Initialization------------------------------------------------------------------------------------
colors = CreateColors()
clock = p.time.Clock()
frame = 0
#Whether to use perlin or shader noise
pnoise = True
w = p.display.set_mode((1920,1080))
world = CreateMap(pnoise)

#Start------------------------------------------------------------------------------------------------------
Draw(colors, frame, world)

#Main Loop--------------------------------------------------------------------------------------------------
stop = False
while not stop:
    clock.tick(30)
    for event in p.event.get():
        if event.type == p.QUIT:
            stop = True
        if event.type == p.KEYDOWN:
            keys = p.key.get_pressed()
            if keys[p.K_SPACE]:
                pnoise = not pnoise
                colors = CreateColors()
                world = CreateMap(pnoise)
                Draw(colors, frame, world)
p.quit()
quit()