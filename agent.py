
from typing import Callable, Dict, Tuple, Set
from collections import deque

from maze import Maze


class Agent:
    def search(self, maze: Maze, algorithm: str) -> Dict:
        searcher = self._getSearcher(algorithm)
        return searcher(maze)

    def _getSearcher(self, algorithm: str) -> Callable[[Maze], Dict]:
        if algorithm == 'aStar':
            return self._aStar
        elif algorithm == 'BFS':
            return self._BFS
        elif algorithm == 'DFS':
            return self._DFS
        else:
            raise ValueError(algorithm)

    def _aStar(self, maze: Maze) -> Dict:
        pass
    
    def _validateAdjacents(self, current: Tuple[int, int], maze: Maze, closedList: dict, generatedChildren: Set) -> Dict:
        row = current[0]
        col = current[1]
        bounds = maze.getSpaces()
        walls = maze.getWalls()
        checks = {}
        # check right
        checks['right'] =  (row,col+1) in bounds \
            and (row,col+1) not in closedList \
            and (row,col+1) not in walls\
            and (row,col+1) not in generatedChildren
        # check above
        checks['up'] =  (row+1,col) in bounds \
            and (row+1,col) not in closedList \
            and (row+1,col) not in walls\
            and (row+1,col) not in generatedChildren
        checks['down'] =  (row-1,col) in bounds \
            and (row-1,col) not in closedList \
            and (row-1,col) not in walls\
            and (row-1,col) not in generatedChildren
        checks['left'] =  (row,col-1) in bounds \
            and (row,col-1) not in closedList \
            and (row,col-1) not in walls\
            and (row,col-1) not in generatedChildren
        return checks
           
    def _BFS(self, maze: Maze) -> Dict:
        '''Assume the following
        - When children nodes are being generated, the order is: right, above, down, left
        - ignore repeated states in the closed list
        '''
        # dicts to remember the explored nodes
        closedList = set()
        generatedChildren = set()
        # use a dictionary to store parent-child relationships for nodes (for backtracking)
        backTracker = {}
        # use a queue to keep track of the open list of nodes
        fringe = deque()
        fringe.append(maze.getStart())
        # start algorithm
        current = None
        nodesExp = 0
        while fringe and nodesExp < 626:
            current = fringe[0]
            # generate children
            adjacentValid = self._validateAdjacents(current, maze, closedList, generatedChildren)
            row = current[0]
            col = current[1] 
            if adjacentValid['right']:
                newChild = (row,col+1)
                fringe.append(newChild)
                generatedChildren.add(newChild)
            if adjacentValid['up']:
                newChild = (row+1,col)
                fringe.append(newChild)
                generatedChildren.add(newChild)
            if adjacentValid['down']:
                newChild = (row-1,col)
                fringe.append(newChild)
                generatedChildren.add(newChild)
            if adjacentValid['left']:
                newChild = (row,col-1)
                fringe.append(newChild)
                generatedChildren.add(newChild)
            if current == maze.getEnd():
                return closedList
            expanded = fringe.popleft()
            closedList.add(expanded)
            nodesExp += 1
            print("Added node {} to closed, #{}".format(expanded, nodesExp))

    def _DFS(self, maze: Maze) -> Dict:
        pass
