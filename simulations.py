import math

import numpy as np
import random

CANVAS_X = 100
CANVAS_Y = 100

# choose a point from the canvas
def get_r_prime():
    return (random.randint(0, CANVAS_X), random.randint(0, CANVAS_Y))
r_prime = get_r_prime()

R_LEFT = (CANVAS_X/4, CANVAS_Y/2)
R_RIGHT = (3*CANVAS_X/4, CANVAS_Y/2)

# try toy case of wanting to pick the left target
def delta_r(ri: (float, float), rf: (float, float)):
    return (rf[0] - ri[0], rf[1] - ri[1])

def magnitude(r):
    return math.sqrt(r[0]**2 + r[1]**2)

# start with left and choose lots of random points on the canvas and measure the accuracy. using CI=0.68
NUMBER_RUNS = 1000
wins = 0
for run in NUMBER_RUNS:
    r_prime = get_r_prime()
