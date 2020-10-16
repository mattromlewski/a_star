from maze import Maze
from agent import Agent


if __name__ == "__main__":
    startingPoints = [(11,2), (11,2), (0,0)]
    endingPoints = [(19,23), (21,2), (23,23)]
    for run, (start, end) in enumerate(zip(startingPoints, endingPoints)):
        print("Run {} - Start {} - End {}".format(run+1, start, end))
        maze = Maze(start=start, end=end)
        agent = Agent()
        BFSResults = agent.search(maze, 'BFS')
        print(BFSResults)



