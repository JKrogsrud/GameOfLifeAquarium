import Cell
import random


class Aquarium():

    # instance attributes
    # row is number of rows
    # column is number of columns
    # birth is a tuple of values representing how many neighbors are required to birth a new cell
    # survive is a tuple of values representing how many neighbors are required for a live cell to survive
    # density is the reciprocal of the expected life of an initial cell during population
    def __init__(self, row=20, column=20, birth=[3], survive=[3, 4], life_density=2):
        self.row = row
        self.column = column
        self.grid = []
        self.birth = birth
        self.survive = survive
        self.life_density = life_density

        for x in range(0, self.column):
            new_row = []
            for y in range(0, self.row):
                new_row.append(Cell.Cell())
            self.grid.append(new_row)

    def populate(self):
        for x in range(0, self.column):
            for y in range(0, self.row):
                life_chance = random.getrandbits(self.life_density-1)
                if life_chance == 0:
                    self.grid[x][y].alive = True
                if self.grid[x][y].alive:
                    R = random.randrange(100, 255)
                    G = random.randrange(100, 255)
                    B = random.randrange(100, 255)
                    choice = random.randrange(3)
                    if choice == 0:
                        self.grid[x][y].color = (R, 0, 0)
                    if choice == 1:
                        self.grid[x][y].color = (0, G, 0)
                    if choice == 2:
                        self.grid[x][y].color = (0, 0, B)

    # Step function to get to the next generation of cells
    def step(self):
        # Basic Rules:
        # 1) If Cell.alive = True and number of alive neighbors < 2, cell dies
        # 2) If Cell.alive = True and has (survive) alive neighbors, cell survives
        # 3) If Cell.alive = True and has not(survive) alive neighbors, cell dies
        # 4) If Cell.alive = False and has (birth) alive neighbors, cell becomes alive

        # First for each cell we count the live neighbors

        change = False

        for x in range(0, self.column):
            for y in range(0, self.row):
                n_count, color = self.count_live_neighbors(x, y)
                if self.grid[x][y].alive:
                    if n_count not in self.survive:
                        self.grid[x][y].future_life = False
                        change = True
                else:
                    if n_count in self.birth:
                        self.grid[x][y].future_life = True
                        self.grid[x][y].future_color = color
                        change = True

        # Update the grid
        for x in range(0, self.column):
            for y in range(0, self.row):
                self.grid[x][y].step()

        return change

    def count_live_neighbors(self, x, y):
        count = 0
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        color = (0, 0, 0)
        for n in neighbors:
            try:
                neighbor = self.grid[x + n[0]][y + n[1]]
                if neighbor.alive:
                    count = count + 1
                    color = (color[0] + neighbor.color[0], color[1] + neighbor.color[1], color[1] + neighbor.color[1])
            except IndexError:
                continue
        if count > 0:
            color = (int(color[0] / count), int(color[1] / count), int(color[2] / count))
        return count, color

    def display(self):
        for y in range(0, self.row):
            row_display = ''
            for x in range(0, self.column):
                if self.grid[x][y].alive:
                    row_display += '*'
                else:
                    row_display += '_'
            print(row_display)

