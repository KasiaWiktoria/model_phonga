import sys, pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA
from itertools import product
from numpy import multiply, subtract, dot
from math import sqrt
import colorsys

X_SIZE = 500
Y_SIZE = 500
screen_size = (X_SIZE, Y_SIZE)

CENTER_POINT = [X_SIZE/2, Y_SIZE/2, X_SIZE/2]
RADIUS = 100
LIGHT_SOURCE_POSITION = [400, 400, 0]
OBSERVER_POSITION = [200, 200, 0]

X = 0
Y = 1 
Z = 2

STEP = 100 

move_keys = {
    K_UP: lambda: move(STEP, Y),
    K_DOWN: lambda: move(-STEP, Y),
    K_RIGHT: lambda: move(STEP, X),
    K_LEFT: lambda: move(-STEP, X),
    K_PERIOD: lambda: move(STEP, Z),
    K_COMMA: lambda: move(-STEP, Z),
}

def find_z_coordinate(x, y):
    b = -2 * CENTER_POINT[2]
    c = CENTER_POINT[2]**2 + (x - CENTER_POINT[0])**2 + (y - CENTER_POINT[1])**2 - RADIUS**2
    delta = b**2 - 4*c

    if delta == 0:
        return -b/2
    elif delta > 0:
        return min((sqrt(delta) - b) / 2, (-sqrt(delta) - b) / 2)

def f_att(r):    # współczynnik tłumienia źródła z odległością
    C = 0.25

    return min(1/(C+r), 1)

def phong_model_function(point):
    Ia = 2      # natężenie światła w otoczeniu obiektu
    Ip = 1      # natężenie światła punktowego
    Ka = 0.05   # współczynnik odbicia światła otoczenia

    Ks = 0      # współczynnik odbicia światła kierunkowego 
    Kd = 0.5    # współczynnik odbicia światła rozproszonego 
    n = 1       # współczynnik gładkości powierzchni

    #F = f_att()

    N = versor(vector(CENTER_POINT, point))
    L = versor(vector(point, LIGHT_SOURCE_POSITION))
    V = versor(vector(point, OBSERVER_POSITION))
    R = versor(subtract(multiply(multiply(N, 2), multiply(N, L)), L))

    return Ia*Ka + Ip * (Kd*max(dot(N,L), 0) + Ks*max(dot(R,V),0)**n)


def vector(start_point, end_point):
    return [end_point[0] - start_point[0], end_point[1] - start_point[1], end_point[2] - start_point[2]]


def versor(vector):
    n = sqrt(sum(e**2 for e in vector))
    return [e / n for e in vector]


def draw():
    for x, y in product(range(X_SIZE), range(Y_SIZE)):
        coords = (x, Y_SIZE - y)
        z = find_z_coordinate(x, y)
        if z:
            ilumination = phong_model_function([x, y, z])
            intensity = min(int(ilumination * 255), 255)
            screen.set_at(coords, colorsys.hsv_to_rgb(0.2, 1, intensity))


def move(step, coord):
    LIGHT_SOURCE_POSITION[coord] += step


pygame.init()
screen = pygame.display.set_mode(screen_size)

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            move_keys[event.key]()
    draw()

    pygame.display.flip()