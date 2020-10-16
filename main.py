from maze import Maze
from agent import Agent
from illustrator import Illustrator


if __name__ == "__main__":
    startingPoints = [(11,2), (11,2), (0,0)]
    endingPoints = [(19,23), (21,2), (24,24)]
    solutionIllustrator = Illustrator()
    for run, (start, end) in enumerate(zip(startingPoints, endingPoints)):
        maze = Maze(start=start, end=end)
        agent = Agent()
        # BFS
        BFSResults = agent.search(maze, 'BFS')
        caption = "BFS Run {} - {}->{} - Expanded {} nodes - Cost {}".format(run+1, start, end, BFSResults['numExpanded'], BFSResults['cost'])
        solutionIllustrator.drawMaze(25,25, walls=maze.getWalls(), expandedNodes=BFSResults['closedSet'], path=BFSResults['path'], caption=caption)
        print("BFS Run {} - Path {}".format(run+1, BFSResults['path']))
        #DFS
        DFSResults = agent.search(maze, 'DFS')
        caption = "DFS Run {} - {}->{} - Expanded {} nodes - Cost {}".format(run+1, start, end, DFSResults['numExpanded'], DFSResults['cost'])
        solutionIllustrator.drawMaze(25,25, walls=maze.getWalls(), expandedNodes=DFSResults['closedSet'], path=DFSResults['path'], caption=caption)




