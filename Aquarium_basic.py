import numpy as np
import Cell
import random


class Aquarium():

    # instance attributes
    # row is number of rows
    # column is number of columns
    def __init__(self, row=20, column=20):
        self.row = row
        self.column = column
        self.grid = []

        for x in range(0, self.column):
            new_row = []
            for y in range(0, self.row):
                new_row.append(Cell.Cell())
            self.grid.append(new_row)

    def populate(self):
        for x in range(0, self.column):
            for y in range(0, self.row):
                self.grid[x][y].alive = bool(random.getrandbits(1))
                if self.grid[x][y].alive:
                    R = random.getrandbits(255)
                    G = random.getrandbits(255)
                    B = random.getrandbits(255)
                    self.grid[x][y].color = (R, G, B)

    # Step function to get to the next generation of cells
    def step(self):
        # Basic Rules:
        # 1) If Cell.alive = True and number of alive neighbors < 2, cell dies
        # 2) If Cell.alive = True and has 2 or 3 alive neighbors, cell lives
        # 3) If Cell.alive = True and has > 3 alive neighbors, cell dies
        # 4) If Cell.alive = False and has 3 alive neighbors, cell becomes alive

        # First for each cell we count the live neighbors

        change = False

        for x in range(0, self.column):
            for y in range(0, self.row):
                n_count = self.count_live_neighbors(x, y)
                if self.grid[x][y].alive:
                    # Rule 1 check
                    if n_count < 2:
                        self.grid[x][y].future_life = False
                        change = True
                    if n_count > 3:
                        self.grid[x][y].future_life = False
                        change = True
                else:
                    if n_count == 3:
                        self.grid[x][y].future_life = True
                        change = True

        # Update the grid
        for x in range(0, self.column):
            for y in range(0, self.row):
                self.grid[x][y].step()

        return change

    def count_live_neighbors(self, x, y):
        count = 0
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for n in neighbors:
            try:
                if self.grid[x+n[0]][y+n[1]].alive:
                    count = count + 1
            except IndexError:
                continue
        return count

    def display(self):
        for y in range(0, self.row):
            row_display = ''
            for x in range(0, self.column):
                if self.grid[x][y].alive:
                    row_display += '*'
                else:
                    row_display += '_'
            print(row_display)

