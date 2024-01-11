#!/usr/bin/env python
import sys
import Aquarium_modified, Cell
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from samplebase import SampleBase
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

class PracticeBoard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(PracticeBoard, self).__init__(*args, **kwargs)

    def run(self):

        # Object for control over the LED Matrix
        options = RGBMatrixOptions()

        # The following are all options for control over the LED Matrix, most of these are left as their defaults
        options.hardware_mapping = 'adafruit-hat'
        options.rows = 32
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 50
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.gpio_slowdown = 4

        # Set the following options for an instance of out matrix
        matrix = RGBMatrix(options=options)

        #  Initialize the canvas
        offset_canvas = matrix.CreateFrameCanvas()

        row = 32
        column = 32
        size = (row,column)
        birth=[2,3,6]
        survive = [6, 7, 8]
        life_density = 2
        n_dist_min = 1
        n_dist_max = 2

        aquarium = Aquarium_modified.Aquarium(row, column, birth, survive, life_density, n_dist_min, n_dist_max)
        aquarium.populate()
        timer = time.time()
        changed = True

        while True:
            current_time = time.time()
            if current_time - timer > 60*3:  # It's been running 3 minutes so restart
                aquarium = Aquarium_modified.Aquarium(row, column, birth, survive, life_density, n_dist_min, n_dist_max)
                aquarium.populate()
                timer = time.time()
            if not changed:
                aquarium = Aquarium_modified.Aquarium(row, column, birth, survive, life_density, n_dist_min, n_dist_max)
                aquarium.populate()
                timer = time.time()
            im = Image.new("RGB", size)
            draw = ImageDraw.Draw(im, None)
            for x in range(0, len(aquarium.grid)):
                for y in range(0, len(aquarium.grid[0])):
                    if aquarium.grid[x][y].alive:
                        draw.point((x, y), aquarium.grid[x][y].color)
                    else:
                        draw.point((x, y), (0, 0, 0))

            im = ImageOps.flip(im)
            offset_canvas.SetImage(im, 0, unsafe=False)  # Project the image to the RGB-Matrix
            offset_canvas = matrix.SwapOnVSync(offset_canvas)  # Update the matrix
            changed = aquarium.step()
            time.sleep(0.2)


# Main
if __name__ == "__main__":
    practice_board = PracticeBoard()
    if (not practice_board.process()):
        practice_board.process()

