import random, pygame, sys
from pygame.locals import *

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
POZADI = (153, 255, 255)
TELO = (255, 51, 153)
PODLAHA = (51, 102, 0)
BGCOLOR = BLACK

class gameController:
    def __init__(self, fps, windowwidth, windowheight):
        self.FPS = fps
        self.w = windowwidth
        self.h = windowheight

        
        
    def main(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Jumper")
        self.cam = 0

        self.hrac = player(50, 50, 50, 50, self)




        self.runGame()


    def terminate(self):
        pygame.quit()
        sys.exit()

    def tick(self):

        self.manageEvents()
        self.hrac.tick()
        self.render()
        
    def render(self):
        self.DISPLAYSURF.fill(POZADI)
        self.hrac.render()
        pygame.display.update()
        self.FPSCLOCK.tick(self.FPS)

    def manageEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT):
                    self.hrac.direction[2] = 1
                if (event.key == pygame.K_RIGHT):
                    self.hrac.direction[3] = 1
                if (event.key == pygame.K_UP):
                    self.hrac.direction[0] = 1
                if (event.key == pygame.K_DOWN):
                    self.hrac.direction[1] = 1
                if event.key == pygame.K_ESCAPE:
                    self.terminate() 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.hrac.direction[1] = 0
                if event.key == pygame.K_LEFT:
                    self.hrac.direction[2] = 0
                if event.key == pygame.K_RIGHT:
                    self.hrac.direction[3] = 0
                if event.key == pygame.K_UP:
                    self.hrac.direction[0] = 0
        

    def runGame(self):
        while True:
            self.tick()

            


class player:
    def __init__(self, x, y, w, h, parent):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = [0, 0, 0, 0]
        self.grav = 0
        self.parent = parent

    def render(self):
        bodySegmentRect = pygame.Rect(self.x-self.parent.cam, self.y, self.w, self.h)
        leftEyeSegmentRect = pygame.Rect(self.x-self.parent.cam+5, self.y+10, 15, 10)
        rightEyeSegmentRect = pygame.Rect(self.x-self.parent.cam+50-25, self.y+10, 15, 10)
        mouthSegmentRect = pygame.Rect(self.x-self.parent.cam+10, self.y+35, 30, 3)
        pygame.draw.rect(self.parent.DISPLAYSURF, TELO, bodySegmentRect)
        pygame.draw.rect(self.parent.DISPLAYSURF, BLACK, leftEyeSegmentRect)
        pygame.draw.rect(self.parent.DISPLAYSURF, BLACK, rightEyeSegmentRect)
        pygame.draw.rect(self.parent.DISPLAYSURF, BLACK, mouthSegmentRect)

    def move(self):
        if self.direction[0] == 1:
            if self.grav == 21:
                self.grav = -20
        if self.direction[1] == 1:
            self.y=self.y+10
        elif self.direction[3] == 1:
            self.x=self.x+10
        elif self.direction[2] == 1:
            self.x=self.x-10
        if self.grav!= 21:
            self.y+= self.grav
            self.grav+=1
            if self.grav == 21:
                self.grav=20
        if (self.y+50)>200:
            self.grav = 21
            self.y = 200-50
        if (self.x+50) > (self.parent.cam+self.parent.w):
            self.parent.cam+= (self.x+50) - (self.parent.cam+self.parent.w)
        elif (self.x) < (self.parent.cam):
            self.parent.cam-= self.parent.cam-self.x
        

    
    def tick(self):
        self.move()
        

class prop:
    def __init__(self, x, y, w, h, parent):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent
            

a = gameController(30, 300, 300)
a.main()
