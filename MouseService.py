#!/usr/bin/python

from pymouse import PyMouse
import time

time.sleep(2)

m = PyMouse()

screen_width, screen_height = m.screen_size()

print(screen_width, screen_height)

top = 150
right = screen_width - 300
bottom = screen_height - 150
left = 300

current_x = left
current_y = top

# Move to top left
m.press(current_x, current_y)

delay = 0.0001
gap = 5


def drag(x, y):
    print("drag:  {},{}".format(x, y))
    m.drag(x, y)


def circle():
    global current_x, current_y, top, left, right, bottom

    # move right
    while current_x < right:
        time.sleep(delay)
        current_x = current_x + gap
        drag(current_x, current_y)

    # once the top is drawn, move down
    top += gap

    # move down
    while current_y < bottom:
        time.sleep(delay)
        current_y = current_y + gap
        drag(current_x, current_y)

    # once the right is drawn, move left
    right -= gap

    # move left
    while current_x > left:
        time.sleep(delay)
        current_x = current_x - gap
        drag(current_x, current_y)

    # once the bottom is drawn, move up
    bottom -= gap

    # move up
    while current_y > top:
        time.sleep(delay)
        current_y = current_y - gap
        drag(current_x, current_y)

    # once the left is drawn, move right
    left += gap


circle()

for _ in range(150):
    circle()
