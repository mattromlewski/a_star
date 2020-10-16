
from typing import Callable, Dict, Tuple, Set, Optional
from collections import deque
from queue import LifoQueue

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
    
    def _validateAdjacents(self, current: Tuple[int, int], maze: Maze, closedSet: dict, backTracker: Optional[Dict]={}) -> Dict:
        row = current[0]
        col = current[1]
        bounds = maze.getSpaces()
        walls = maze.getWalls()
        checks = {}
        checks['right'] =  (row,col+1) in bounds \
            and (row,col+1) not in closedSet \
            and (row,col+1) not in walls\
            and (row,col+1) not in backTracker
        checks['up'] =  (row+1,col) in bounds \
            and (row+1,col) not in closedSet \
            and (row+1,col) not in walls\
            and (row+1,col) not in backTracker
        checks['down'] =  (row-1,col) in bounds \
            and (row-1,col) not in closedSet \
            and (row-1,col) not in walls\
            and (row-1,col) not in backTracker
        checks['left'] =  (row,col-1) in bounds \
            and (row,col-1) not in closedSet \
            and (row,col-1) not in walls\
            and (row,col-1) not in backTracker
        return checks
           
    def _BFS(self, maze: Maze) -> Dict:
        '''Assume the following
        - When children nodes are being generated, the order is: right, above, down, left
        - ignore repeated states to avoid loops -> optimality not affected
        '''
        # dict to remember the explored nodes
        closedSet = set()
        # use a dictionary to store parent-child relationships for nodes to build final path
        # secondary utility is to track which nodes have been added to the  fringe so loops are avoided
        backTracker = {}
        # use a queue to keep track of the open list of nodes
        fringe = deque()
        fringe.append(maze.getStart())
        # start algorithm
        current = None
        while fringe:
            current = fringe[0]
            # generate children
            adjacentValid = self._validateAdjacents(current, maze, closedSet, backTracker=backTracker)
            row = current[0]
            col = current[1] 
            if adjacentValid['right']:
                newChild = (row,col+1)
                fringe.append(newChild)
                backTracker[newChild] = current
            if adjacentValid['up']:
                newChild = (row+1,col)
                fringe.append(newChild)
                backTracker[newChild] = current
            if adjacentValid['down']:
                newChild = (row-1,col)
                fringe.append(newChild)
                backTracker[newChild] = current
            if adjacentValid['left']:
                newChild = (row,col-1)
                fringe.append(newChild)
                backTracker[newChild] = current
            expanded = fringe.popleft()
            closedSet.add(expanded)
            if current == maze.getEnd():
                # build path
                key = current
                path = deque()
                while key != maze.getStart():
                    path.appendleft(key)
                    key = backTracker[key]
                path.appendleft(maze.getStart()) 
                # return path, cost, and number of nodes goal-checked
                return {'path': path, 'cost': len(path), 'numExpanded': len(closedSet), 'closedSet': closedSet}

    def _DFS(self, maze: Maze) -> Dict:
        '''Assume the following
        - When children nodes are being added to the stack, the input order is: left, down, above, right
        - ignore repeated states to avoid loops -> optimality not affected
        '''
        closedSet = set()
        backTracker = {}
        fringe = LifoQueue()
        fringe.put(maze.getStart())
        current = None
        while fringe:
            current = fringe.get()
            adjacentValid = self._validateAdjacents(current, maze, closedSet, backTracker=backTracker)
            row = current[0]
            col = current[1]
            if adjacentValid['left']:
                newChild = (row,col-1)
                fringe.put(newChild)
                backTracker[newChild] = current
            if adjacentValid['down']:
                newChild = (row-1,col)
                fringe.put(newChild)
                backTracker[newChild] = current
            if adjacentValid['up']:
                newChild = (row+1,col)
                fringe.put(newChild)
                backTracker[newChild] = current
            if adjacentValid['right']:
                newChild = (row,col+1)
                fringe.put(newChild)
                backTracker[newChild] = current
            closedSet.add(current)
            if current == maze.getEnd():
                # build path
                key = current
                path = deque()
                while key != maze.getStart():
                    path.appendleft(key)
                    key = backTracker[key]
                path.appendleft(maze.getStart()) 
                # return path, cost, and number of nodes goal-checked
                return {'path': path, 'cost': len(path), 'numExpanded': len(closedSet), 'closedSet': closedSet}
            