import pygame

class Illustrator:
    def __init__(self):
        self._wallColour = (0,0,0)
        self._emptyColour = (255,255,255)
        self._openedColour = (100,100,200)
        self._pathColour = (0,255,0) 
        self._windowSize = [255,255]
        self._blockWidth = 20
        self._blockHeight = 20
        self._blockMargin = 1

    def drawMaze(self, height, width, walls, expandedNodes, path, caption="Window"):
    #def drawMaze(self):
        pygame.init()
        pygame.display.set_caption(caption)
        screen = pygame.display.set_mode([height*(self._blockHeight+self._blockMargin), width*(self._blockHeight+self._blockMargin)])
        screen.fill(self._wallColour)
        done = False  
        pathSet = set(path)
        while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            for i in range(0,height):
                for j in range(0, width):
                    
                    if (i,j) in expandedNodes and (i,j) not in pathSet:
                        colour = self._openedColour
                    elif (i,j) in walls:
                        colour = self._wallColour
                    elif (i,j) in pathSet:
                        colour = self._pathColour
                    else:
                        colour = self._emptyColour
                    pygame.draw.rect(screen,
                             colour,
                             [(self._blockMargin + self._blockWidth) * j + self._blockMargin,
                              (self._blockMargin + self._blockHeight) * (height-1-i) + self._blockMargin,
                              self._blockWidth,
                              self._blockHeight])

            pygame.display.flip()
