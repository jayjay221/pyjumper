import random, pygame, sys, time
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

        self.menu = menu(self)


        self.podlaha = podlaha(30, self)
        self.hrac = player(300, 300, 50, 50, self)

        self.objects = [self.hrac, self.podlaha, prop(5, 5, 100, 100, self)]



        #self.menu.render()
        self.runGame()


    def terminate(self):
        pygame.quit()
        sys.exit()

    def tick(self):

        self.manageEvents()
        for each in self.objects:
            if hasattr(each, 'tick'):
                each.tick()
        self.render()
        
    def render(self):
        self.DISPLAYSURF.fill(POZADI)
        for each in self.objects:
            each.render()
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
        self.stands = 0
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

    def getCoord(self, which):
        if which == 'top':
            return self.y
        elif which == 'bottom':
            return self.y+self.h
        elif which == 'left':
            return self.x
        elif which == 'right':
            return self.x+self.w
        
    def doesCollide(self, wth, vect):
        if ((self.getCoord('left')-vect[2]) < wth.getCoord('right') and
            (self.getCoord('right')+vect[3]) > wth.getCoord('left') and
            (self.getCoord('top')-vect[0]) < wth.getCoord('bottom') and
            (self.getCoord('bottom')+vect[1]) > wth.getCoord('top')):
            return 1
        else:
            return 0

    def moveCam(self):
        
        if (self.x+self.w) > (self.parent.cam+self.parent.w):
            self.parent.cam+= (self.x+self.w) - (self.parent.cam+self.parent.w)
        elif (self.x) < (self.parent.cam):
            self.parent.cam-= self.parent.cam-self.x
            
    def move(self):
        # 0 = up
        # 1 = down
        # 2 = left
        # 3 = right
    

        vect = [self.direction[0]*10, self.direction[1]*10, self.direction[2]*10, self.direction[3]*10]
        col = 0

        for each in self.parent.objects:
            if (each.__class__.__name__ != 'podlaha') and (each.__class__.__name__ != 'player'):
                if self.doesCollide(each, vect):
                    col = 1

        if col==0:
            self.x-=vect[2]
            self.x+=vect[3]
            self.y+=vect[1]
            self.y-=vect[0]
                

        
    
    def tick(self):
        self.move()
        self.moveCam();
        

class prop:
    def __init__(self, x, y, w, h, parent):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent

    def getCoord(self, which):
        if which == 'top':
            return self.y
        elif which == 'bottom':
            return self.y+self.h
        elif which == 'left':
            return self.x
        elif which == 'right':
            return self.x+self.w

    def render(self):
        floorRect = pygame.Rect(self.x-self.parent.cam, self.y, self.w, self.h)
        pygame.draw.rect(self.parent.DISPLAYSURF, PODLAHA, floorRect)


class podlaha:
    def __init__(self, y, parent):
        
        self.y = parent.h-y
        self.h = y
        self.parent = parent

    def render(self):
        floorRect = pygame.Rect(0, self.y, self.parent.w, self.h)
        pygame.draw.rect(self.parent.DISPLAYSURF, PODLAHA, floorRect)

    def getCoord(self, which):
        if which == 'top':
            return self.y
        else:
            return 0
        
class menu:
    def __init__(self, parent):
        self.font = pygame.font.SysFont("arial", 150)
        self.nadpis = self.font.render("pyJumper", 1, (0, 0, 0))
        self.parent = parent

    def render(self):
        self.parent.DISPLAYSURF.fill(POZADI)
        self.parent.DISPLAYSURF.blit(self.nadpis, (50, 200))
        pygame.display.update()
        time.sleep(5)
        
    
            

a = gameController(50, 800, 600)
a.main()
