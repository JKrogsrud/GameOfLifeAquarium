import sys, pygame
import Aquarium_basic, Cell
import time
pygame.init()

size = width, height = 500, 500

screen = pygame.display.set_mode(size)
aquarium = Aquarium_basic.Aquarium(50, 50)
aquarium.populate()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # pxarray = pygame.PixelArray(screen)
    for x in range(0,len(aquarium.grid)):
        for y in range(0,len(aquarium.grid[0])):
            if aquarium.grid[x][y].alive:
                # pxarray[x,y] = (255, 0, 0)
                pygame.draw.rect(screen,(0,255,0),[x*10,y*10,10,10])
            else:
                # pxarray[x, y] = (0, 0, 0)
                pygame.draw.rect(screen, (0, 0, 0), [x * 10, y * 10, 10, 10])
    pygame.display.flip()
    aquarium.step()
    time.sleep(0.1)