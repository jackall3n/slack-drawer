import linedraw
from pymouse import PyMouse
import time
import argparse
import json
import sys

hatch_size = 8
contour_simplify = 1
draw_contours = True
draw_hatch = True
input_path = ''
delay = 3
speed = 0.001

def get_cache_name():
    return 'cache/{}-{}-{}-{}-{}.json'.format(input_path, linedraw.contour_simplify, linedraw.draw_hatch,
                                              linedraw.draw_contours, linedraw.hatch_size)


def draw():
    linedraw.draw_contours = draw_contours
    linedraw.draw_hatch = draw_hatch
    linedraw.hatch_size = hatch_size
    linedraw.contour_simplify = contour_simplify

    cache_name = get_cache_name()

    print(cache_name, input_path)

    try:
        file = open(cache_name, 'r')
        fc = file.read()
        lines = json.loads(fc)
        file.close()
    except FileNotFoundError:
        print("Unexpected error:", sys.exc_info()[0])
        file = open(cache_name, 'w')
        lines = linedraw.sketch(input_path)
        file.write(json.dumps(lines))
        file.close()

    mouse = PyMouse()

    mouse_x, mouse_y = mouse.position()

    time.sleep(delay)

    scale = 1

    def get_x(_x):
        return (_x * scale) + mouse_x

    def get_y(_y):
        return (_y * scale) + mouse_y

    def drag(_x, _y):
        # print("drag: {},{}".format(_x, _y))
        mouse.drag(_x, _y)

    for line in lines:

        start_x, start_y = line[0]

        mouse.press(get_x(start_x), get_y(start_y), 1)

        for (x, y) in line:
            time.sleep(speed)
            drag(get_x(x), get_y(y))

        end_x, end_y = line[len(line) - 1]

        mouse.release(get_x(end_x), get_y(end_y), 1)

    mouse.move(mouse_x, mouse_y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert image to vectorized line drawing for plotters.')
    parser.add_argument('-i', '--input', dest='input_path',
                        default='tfw.jpg', action='store', nargs='?', type=str,
                        help='Input path')

    parser.add_argument('-nc', '--no_contour', dest='no_contour',
                        const=draw_contours, default=not draw_contours, action='store_const',
                        help="Don't draw contours.")

    parser.add_argument('-nh', '--no_hatch', dest='no_hatch',
                        const=draw_hatch, default=not draw_hatch, action='store_const',
                        help='Disable hatching.')

    parser.add_argument('--hatch_size', dest='hatch_size',
                        default=hatch_size, action='store', nargs='?', type=int,
                        help='Patch size of hatches. eg. 8, 16, 32')

    parser.add_argument('-s', '--speed', dest='speed',
                        default=speed, action='store', nargs='?', type=float,
                        help='Speed that drawing occurs')

    parser.add_argument('-d', '--delay', dest='delay',
                        default=delay, action='store', nargs='?', type=int,
                        help='Seconds before drawing begins')

    parser.add_argument('-cs', '--contour_simplify', dest='contour_simplify',
                        default=contour_simplify, action='store', nargs='?', type=int,
                        help='Level of contour simplification. eg. 1, 2, 3')

    args = parser.parse_args()

    draw_hatch = not args.no_hatch
    draw_contours = not args.no_contour
    hatch_size = args.hatch_size
    contour_simplify = args.contour_simplify
    input_path = args.input_path
    delay = args.delay
    speed = args.speed

    draw()
