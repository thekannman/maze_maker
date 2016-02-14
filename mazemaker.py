import numpy as np
import random
from PIL import Image
import matplotlib.pyplot as plt

class Maze:
    """"""
    start = np.zeros(2, np.int)
    end = np.zeros(2, np.int)

    def __init__(self, height, width):
        self.maze_array = np.zeros((height, width), np.int)
        self.start[0] += 1
        self.end[0] = height-2
        self.end[1] = width-1
        self.height = height
        self.width = width
        self.maze_array[tuple(self.start)] = 3

    def make_path(self):
        point = self.start
        count = 0
        self.path = []
        self.path.append(np.copy(point))
        while np.any(point != self.end):
            point,usable = self.make_move(point)
            self.path.append(np.copy(point))
            self.maze_array[tuple(point)] = 2
            count += 1
            if count == 10000000:
                break
        self.maze_array[tuple(self.end)] = 3

    def add_branches(self, num_branches):
        point = np.copy(random.choice(self.path))
        count = 0
        for i in range(num_branches):
            path = []
            while True:
                point[0] = random.randint(1, self.height-2)
                point[1] = random.randint(1,self.width-2)
                if self.maze_array[tuple(point)] > 0:
                    path.append(point)
                    break
            while np.any(point != self.end):
                point,usable = self.make_move(point, False)
                if not usable:
                    break
                path.append(np.copy(point))
                self.maze_array[tuple(point)] = 1
                count += 1
                if count == 10000000:
                    break

    def make_move(self, point, allow_backtrack = True):
        old_point = np.copy(point)
        edge_count = 0
        dead_count = 0
        while True:
            move = random.randint(0,3)
            if move == 0:
                point[0] += 1
            elif move == 1:
                point[1] += 1
            elif move == 2:
                point[0] -= 1
            else:
                point[1] -= 1
            if np.all(point == self.end):
                break
            if not self.is_in_array(point):
                point = np.copy(old_point)
                continue
            if self.is_edge(point):
                edge_count += 1
                if edge_count > 10:
                    if not allow_backtrack:
                        return point,False
                    back_points = low_heavy_random(1,len(self.path)-1)
                    point = self.backtrack(back_points)
                    break
                point = np.copy(old_point)
                continue
            if not self.is_dead_end(point):
                dead_count += 1
                if dead_count > 10:
                    if not allow_backtrack:
                        return point,False
                    back_points = low_heavy_random(1,len(self.path)-1)
                    point = self.backtrack(back_points)
                    break
                point = np.copy(old_point)
                continue
            else:
                break
        return point,True

    def is_in_array(self, point):
        if point[0] < 0:
            return False
        elif point[0] >= self.height:
            return False
        elif point[1] < 0:
            return False
        elif point[1] >= self.width:
            return False
        else:
            return True

    def is_edge(self, point):
        if point[0] == 0:
            return True
        elif point[0] == self.height-1:
            return True
        elif point[1] == 0:
            return True
        elif point[1] == self.width-1:
            return True
        else:
            return False

    def is_dead_end(self, p):
        point = np.copy(p)
        connection_count = 0
        point[0] -= 1
        connection_count += (self.maze_array[tuple(point)]>0)
        point[0] += 2
        connection_count += (self.maze_array[tuple(point)]>0)
        point[0] -= 1
        point[1] -= 1
        connection_count += (self.maze_array[tuple(point)]>0)
        point[1] += 2
        connection_count += (self.maze_array[tuple(point)]>0)
        return connection_count == 1

    def show(self):
        img = Image.fromarray((self.maze_array>0)*255.0)
        img.show()

    def show_answer(self):
        img = Image.fromarray(self.maze_array*255.0/3.0)
        img.show()

    def backtrack(self, back_points):
        for i in range(back_points):
            point = self.path.pop()
            self.maze_array[tuple(point)] = 0
        return point

def low_heavy_random(low, high):
    choices = []
    for i in range(low,high):
        choices.extend([i]*(high-i+1))
    result = random.choice(choices)
    return result

if __name__ == '__main__':
    random.seed(4)
    maze = Maze(100,100)
    maze.make_path()
    maze.add_branches(1000)
    maze.show()
    maze.show_answer()