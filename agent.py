# Matthew Romlewski October 20 2020
from typing import Callable, Dict, Tuple, Set, Optional
from collections import deque, OrderedDict
from queue import LifoQueue
import math

from maze import Maze


class Agent:
    def search(self, maze: Maze, algorithm: str) -> Dict:
        searcher = self._getSearcher(algorithm)
        return searcher(maze)

    def _getSearcher(self, algorithm: str) -> Callable[[Maze], Dict]:
        if algorithm == 'A*':
            return self._aStar
        elif algorithm == 'BFS':
            return self._BFS
        elif algorithm == 'DFS':
            return self._DFS
        else:
            raise ValueError(algorithm)
    
    def _validateAdjacents(self, current: Tuple[int, int], maze: Maze, closedSet: dict, backTracker: Optional[OrderedDict]={}) -> Dict:
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
        closedSet = OrderedDict()
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
            closedSet[expanded] = None
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
        - ignore repeated states to avoid loops -> DFS is not an optimal algorithm anyways
        '''
        closedSet = OrderedDict()
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
            closedSet[current] = None
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

    def _heuristic(self, node: Tuple[int, int], goal: Tuple[int, int], heuristic: str) -> float:
        heuristicFn = self._getHeuristic(heuristic)
        return heuristicFn(node, goal)

    def _getHeuristic(self, heuristic: str) -> Callable:
        if heuristic == 'manhattan':
            return self._manhattan
        elif heuristic == 'euclidean':
            return self._euclidean
        else:
            raise ValueError(algorithm)
    
    def _manhattan(self, node: Tuple[int, int], goal: Tuple[int, int]) -> float:
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def _euclidean(self, node: Tuple[int, int], goal: Tuple[int, int] ) -> float:
        return math.sqrt(math.pow(node[0] - goal[0], 2) + math.pow(node[1] - goal[1], 2))

    def _aStar(self, maze: Maze) -> Dict:
        '''Assume the following
        - If a new minimum cost node is not found during child generation, then find a new 
        minimum from the frontier (go backwards potentially)
        '''
        frontier = {} # key: coordinates, val: heuristic cost
        minimumCostNode = None
        minimumCost = float('inf')
        closedSet = OrderedDict()
        backTracker = {}
        current = maze.getStart()
        heuristic = 'euclidean'
        while len(closedSet) < 625:
            minUpdated = False
            adjacentValid = self._validateAdjacents(current, maze, closedSet, backTracker={})
            row = current[0]
            col = current[1]
            if adjacentValid['left']:
                newChild = (row,col-1)
                if newChild in frontier:
                    costLeft = frontier[newChild]
                else:
                    costLeft = self._heuristic(newChild, maze.getEnd(), heuristic)
                    frontier[newChild] = costLeft
                if costLeft <= minimumCost:
                    minimumCostNode = newChild
                    minimumCost = costLeft
                    minUpdated = True
                backTracker[newChild] = current
            if adjacentValid['down']:
                newChild = (row-1,col)
                if newChild in frontier:
                    costDown = frontier[newChild]
                else:
                    costDown = self._heuristic(newChild, maze.getEnd(), heuristic)
                    frontier[newChild] = costDown
                if costDown <= minimumCost:
                    minimumCostNode = newChild
                    minimumCost = costDown
                    minUpdated = True
                backTracker[newChild] = current
            if adjacentValid['right']:
                newChild = (row,col+1)
                if newChild in frontier:
                    costRight = frontier[newChild]
                else:
                    costRight = self._heuristic(newChild, maze.getEnd(), heuristic)
                    frontier[newChild] = costRight
                if costRight <= minimumCost:
                    minimumCostNode = newChild
                    minimumCost = costRight
                    minUpdated = False
                backTracker[newChild] = current
            if adjacentValid['up']:
                newChild = (row+1,col)
                if newChild in frontier:
                    costUp = frontier[newChild]
                else:
                    costUp = self._heuristic(newChild, maze.getEnd(), heuristic)
                    frontier[newChild] = costUp
                if costUp <= minimumCost:
                    minimumCostNode = newChild
                    minimumCost = costUp
                    minUpdated = True
                backTracker[newChild] = current
            # if a minimum node wasn't found in the neighbors, find the minimum node from the full frontier
            if not minUpdated:
                minimumCost = float('inf')
                for testNode, testCost in frontier.items():
                    if testCost <= minimumCost:
                        minimumCost = testCost
                        minimumCostNode = testNode
                        
            frontier.pop(minimumCostNode)
            closedSet[minimumCostNode] = None
            current = minimumCostNode
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