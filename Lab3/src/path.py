from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid


class Path:
    def __init__(self, maze):
        self.maze = [[ 1 ^ j  for j in i] for i in maze]
        
        
    def find(self):
        start = ((len(self.maze) - 1), self.maze[-1].index(1))
        end = (0, self.maze[0].index(1))   
        
        grid = Grid(matrix=self.maze)
        
        startPosition = grid.node(start[1], start[0])
        endPosition = grid.node(end[1], end[0])
        
        return AStarFinder().find_path(startPosition, endPosition, grid)