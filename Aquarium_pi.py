#!/usr/bin/env python
import sys
import Aquarium_basic, Cell
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
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.gpio_slowdown = 2

        # Set the following options for an instance of out matrix
        matrix = RGBMatrix(options=options)

        #  Initialize the canvas
        offset_canvas = matrix.CreateFrameCanvas()

        size = width, height = 32, 32

        aquarium = Aquarium_basic.Aquarium(width, height)
        aquarium.populate()
        timer = time.time()
        changed = True

        while True:
            current_time = time.time()
            if current_time - timer > 60*3:  # It's been running 3 minutes so restart
                aquarium = Aquarium_basic.Aquarium(width, height)
                aquarium.populate()
                timer = time.time()
            if not changed:
                aquarium = Aquarium_basic.Aquarium(width, height)
                aquarium.populate()
                timer = time.time()
            im = Image.new("RGB", size)
            draw = ImageDraw.Draw(im, None)
            for x in range(0, len(aquarium.grid)):
                for y in range(0, len(aquarium.grid[0])):
                    if aquarium.grid[x][y].alive:
                        draw.point((x, y), (0, 255, 0))
                    else:
                        draw.point((x, y), (0, 0, 0))

            im = ImageOps.flip(im)
            offset_canvas.SetImage(im, 0, unsafe=False)  # Project the image to the RGB-Matrix
            offset_canvas = matrix.SwapOnVSync(offset_canvas)  # Update the matrix
            changed = aquarium.step()
            time.sleep(0.3)


# Main
if __name__ == "__main__":
    practice_board = PracticeBoard()
    if (not practice_board.process()):
        practice_board.process()

