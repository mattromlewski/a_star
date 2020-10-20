# Matthew Romlewski October 20 2020
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
        # Draws the maze, then the explored nodes, and then the path
        pygame.init()
        pygame.display.set_caption(caption)
        screen = pygame.display.set_mode([height*(self._blockHeight+self._blockMargin), width*(self._blockHeight+self._blockMargin)])
        screen.fill(self._wallColour)
        done = False  
        pathSet = set(path)
        for i in range(0,height):
            for j in range(0, width):
                if (i,j) in walls:
                    colour = self._wallColour
                else:
                    colour = self._emptyColour
                pygame.draw.rect(screen,
                            colour,
                            [(self._blockMargin + self._blockWidth) * j + self._blockMargin,
                            (self._blockMargin + self._blockHeight) * (height-1-i) + self._blockMargin,
                            self._blockWidth,
                            self._blockHeight])
        colour = self._openedColour
        for explored in expandedNodes.keys():
            i = explored[0]
            j = explored[1]
            pygame.draw.rect(screen,
                            colour,
                            [(self._blockMargin + self._blockWidth) * j + self._blockMargin,
                            (self._blockMargin + self._blockHeight) * (height-1-i) + self._blockMargin,
                            self._blockWidth,
                            self._blockHeight])
            pygame.time.wait(5)

            pygame.display.flip()
        colour = self._pathColour
        for pathStep in path:
            i = pathStep[0]
            j = pathStep[1]
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            pygame.draw.rect(screen,
                            colour,
                            [(self._blockMargin + self._blockWidth) * j + self._blockMargin,
                            (self._blockMargin + self._blockHeight) * (height-1-i) + self._blockMargin,
                            self._blockWidth,
                            self._blockHeight])
            pygame.time.wait(10)
            pygame.display.flip()
        while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            