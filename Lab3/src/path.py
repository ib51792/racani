from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Path:
    def __init__(self, maze):
        self.maze = [[ 1 ^ j  for j in i] for i in maze]
        
        
    def find(self):
        end = (0, self.maze[0].index(1))
        start = ((len(self.maze) - 1), self.maze[-1].index(1))   
        
        grid = Grid(matrix=self.maze)
        
        startPosition = grid.node(start[1], start[0])
        endPosition = grid.node(end[1], end[0])
        
        finder = AStarFinder()
        path, _ = finder.find_path(startPosition, endPosition, grid)
        
        return path