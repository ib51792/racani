from colorama import init, Fore
import random


class Maze:
    def __init__(self, height, width):
        self.maze = []
        self.height = height
        self.width = width
    
    def printMaze(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'u'): print(Fore.WHITE + str(self.maze[i][j]), end=" ")
                elif (self.maze[i][j] == 0): print(Fore.GREEN + str(self.maze[i][j]), end=" ")
                else: print(Fore.RED + str(self.maze[i][j]), end=" ")
            print('\n')


    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == 0): s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == 0): s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == 0): s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == 0): s_cells += 1
        return s_cells


    def generate(self):
        wall, cell, unvisited = 1, 0, 'u'
        init()

        for i in range(0, self.height):
            line = []
            for j in range(0, self.width): line.append(unvisited)
            self.maze.append(line)

        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0): starting_height += 1
        if (starting_height == self.height-1): starting_height -= 1
        if (starting_width == 0): starting_width += 1
        if (starting_width == self.width-1): starting_width -= 1

        self.maze[starting_height][starting_width] = cell
        walls = [[starting_height - 1, starting_width],
                 [starting_height, starting_width - 1],
                 [starting_height, starting_width + 1],
                 [starting_height + 1, starting_width]]
        self.maze[starting_height-1][starting_width] = 1
        self.maze[starting_height][starting_width - 1] = 1
        self.maze[starting_height][starting_width + 1] = 1
        self.maze[starting_height + 1][starting_width] = 1

        while (walls):
            rand_wall = walls[int(random.random()*len(walls))-1]
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]+1] == 0):
                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        self.maze[rand_wall[0]][rand_wall[1]] = 0
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 1
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 1
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 1
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
			
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]+1][rand_wall[1]] == 0):
                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        self.maze[rand_wall[0]][rand_wall[1]] = 0
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 1
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 1
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 1
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]-1][rand_wall[1]] == 0):
                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        self.maze[rand_wall[0]][rand_wall[1]] = 0
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 1
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 1
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 1
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == 0):
                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        self.maze[rand_wall[0]][rand_wall[1]] = 0
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 0):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 1
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 1
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 0):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 1
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)
	
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'u'): self.maze[i][j] = 1

        for i in range(0, self.width):
            if (self.maze[1][i] == 0):
                self.maze[0][i] = 0
                break

        for i in range(self.width-1, 0, -1):
            if (self.maze[self.height-2][i] == 0):
                self.maze[self.height-1][i] = 0
                break
        self.printMaze()
        return self.maze