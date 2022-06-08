class Cell:
    def __init__(self, alive=False, color=(0,0,0)):
        self.alive = alive
        self.color = color
        self.future_life = alive
        self.future_color = color

    def step(self):
        self.alive = self.future_life
        self.color = self.future_color
