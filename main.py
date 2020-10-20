# Matthew Romlewski October 20 2020
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
        for algorithm in ['A*']:
            results = agent.search(maze, '{}'.format(algorithm))
            caption = "{} Run {} - {}->{} - Expanded {} nodes - Cost {}"\
                .format(algorithm, run+1, start, end, results['numExpanded'], results['cost'])
            solutionIllustrator.drawMaze(
                25,
                25, 
                walls=maze.getWalls(), 
                expandedNodes=results['closedSet'], 
                path=results['path'], caption=caption
            )
            print("{} Run {} - Path {}".format(algorithm, run+1, results['path']))
            print(caption)
