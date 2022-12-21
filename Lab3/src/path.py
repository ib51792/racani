from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Path:
    def __init__(self, maze):
        self.maze = maze
        
        
    def find(self):
        i, j = (0, 0)
        
        for j, v in enumerate(self.maze[0]):
                if v == 0: break
        
        end = [i, j]
        
        i = len(self.maze) - 1
        
        for j, v in enumerate(self.maze[-1]):
                if v == 0: break
                
        start = [i, j]
        
        for i, v in enumerate(self.maze):
            for j, v2 in enumerate(v):
                if v2 == 1:
                    self.maze[i][j] = 0
                else:
                    self.maze[i][j] = 1
        
        
        grid = Grid(matrix=self.maze)
        
        startPosition = grid.node(start[1], start[0])
        endPosition = grid.node(end[1], end[0])
        
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, _ = finder.find_path(startPosition, endPosition, grid)
        
        return path