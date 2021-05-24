import sys, pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA
from itertools import product
from numpy import multiply, subtract, dot
from math import sqrt
from colorsys import hls_to_rgb, hsv_to_rgb

X_SIZE = 400
Y_SIZE = 400
screen_size = (X_SIZE, Y_SIZE)

CENTER_POINT = [X_SIZE/2, Y_SIZE/2, X_SIZE/2]
RADIUS = 100
LIGHT_SOURCE_POSITION = [150, 250, 0]
OBSERVER_POSITION = [200, 200, 0]

BALL_COLOR = 0.1
COLOR_SATURATION = 0.5

X = 0
Y = 1 
Z = 2

STEP = 50 

Ia = 1      # natężenie światła w otoczeniu obiektu
Ip = 1      # natężenie światła punktowego
Ka = 0.2    # współczynnik odbicia światła otoczenia

Ks = 0.1     # współczynnik odbicia światła kierunkowego 
Kd = 0.4    # współczynnik odbicia światła rozproszonego 
n = 10      # współczynnik gładkości powierzchni

move_keys = { K_UP: lambda: move(STEP, Y), K_DOWN: lambda: move(-STEP, Y), K_RIGHT: lambda: move(STEP, X), 
            K_LEFT: lambda: move(-STEP, X), K_PERIOD: lambda: move(STEP, Z), K_COMMA: lambda: move(-STEP, Z)}


def find_z_coordinate(x, y):
    b = -2 * CENTER_POINT[2]
    c = CENTER_POINT[2]**2 + (x - CENTER_POINT[0])**2 + (y - CENTER_POINT[1])**2 - RADIUS**2
    delta = b**2 - 4*c

    if delta == 0:
        return -b/2
    elif delta > 0:
        return min((sqrt(delta) - b)/2, (-sqrt(delta) - b)/2)

def calculate_light_source_distance(point):
    x_diff = LIGHT_SOURCE_POSITION[X] - point[X]
    y_diff = LIGHT_SOURCE_POSITION[Y] - point[Y]
    z_diff = LIGHT_SOURCE_POSITION[Z] - point[Z]

    return sqrt((x_diff)**2 + (y_diff)**2 + (z_diff)**2)

def f_att(r):    # współczynnik tłumienia źródła z odległością
    C1 = 0.1
    C2 = 0.2
    C3 = 0.25

    return min(1/(C1 + C2*r +C3*r**2), 1)

def calculate_light_intensity(point):
    N = normal_vector(point)
    L = versor(vector(point, LIGHT_SOURCE_POSITION))
    V = versor(vector(point, OBSERVER_POSITION))
    R = versor(subtract(multiply(multiply(N, 2), multiply(N, L)), L))

    r = calculate_light_source_distance(point) / 100
    f = f_att(r)

    I = phong_model_function(Ia, Ip, Ka, Kd, Ks, f, N, L, R, V, n)

    return min(I, 1)

def normal_vector(point):
    return versor(vector(CENTER_POINT, point))

def phong_model_function(Ia, Ip, Ka, Kd, Ks, f, N, L, R, V, n):

    ambient_light = Ia * Ka
    diffuse_reflection = Ip * f * Kd * max(dot(N,L), 0)
    directional_reflection = Ip * f * Ks * max(dot(R,V),0)**n

    return ambient_light + diffuse_reflection + directional_reflection

def vector(start_point, end_point):
    return [end_point[0] - start_point[0], end_point[1] - start_point[1], end_point[2] - start_point[2]]

def versor(vector):
    n = sqrt(sum(e**2 for e in vector))
    return [e / n for e in vector]

def draw():
    x_range = range(X_SIZE)
    y_range = range(Y_SIZE)

    for x, y in product(x_range, y_range):
        z = find_z_coordinate(x, y)

        if z:
            ilumination = calculate_light_intensity([x, y, z])
            #r, g, b = hsv_to_rgb(BALL_COLOR, 0.8, ilumination)
            r, g, b = hls_to_rgb(BALL_COLOR, ilumination, COLOR_SATURATION)
            color = (255*r,255*g,255*b)

            screen.set_at((x, Y_SIZE - y), color)


def move(step, coord):
    LIGHT_SOURCE_POSITION[coord] += step
    print(f'Pozycja źródła światła: {LIGHT_SOURCE_POSITION}')

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