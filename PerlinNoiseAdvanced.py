from collections import namedtuple
import random
import math
import numpy as np
from matplotlib import pyplot as plt

scale = 100
width = 500
height = 500
octaves = 10
persistence = 0.5
lacunarity = 1.6

noise = np.zeros(shape=(width, height))
Vector2D = namedtuple("Vector2", ["x", "y"])

seed = 0

def lerp(left, right, amount):
    return (1 - amount) * left + amount * right


def get_seed(a, b):
    rng = random.Random(-a)
    a_new = rng.randrange(0, 10000000)
    rng = random.Random(b)
    b_new = rng.randrange(0, 10000000)
    return a_new + b_new + seed


def get_noise_value(x, y):
    x_min = int(x)
    y_min = int(y)
    x_max = x_min + 1
    y_max = y_min + 1

    rng = random.Random(get_seed(x_min, y_min))
    g0 = Vector2D(rng.random() * 2 - 1, rng.random() * 2 - 1)
    rng = random.Random(get_seed(x_max, y_min))
    g1 = Vector2D(rng.random() * 2 - 1, rng.random() * 2 - 1)
    rng = random.Random(get_seed(x_min, y_max))
    g2 = Vector2D(rng.random() * 2 - 1, rng.random() * 2 - 1)
    rng = random.Random(get_seed(x_max, y_max))
    g3 = Vector2D(rng.random() * 2 - 1, rng.random() * 2 - 1)

    p0 = Vector2D(x - x_min, y - y_min)
    p1 = Vector2D(x - x_max, y - y_min)
    p2 = Vector2D(x - x_min, y - y_max)
    p3 = Vector2D(x - x_max, y - y_max)

    d0 = dot(p0.x, p0.y, g0.x, g0.y)
    d1 = dot(p1.x, p1.y, g1.x, g1.y)
    d2 = dot(p2.x, p2.y, g2.x, g2.y)
    d3 = dot(p3.x, p3.y, g3.x, g3.y)

    x_fade = fade(x - x_min)
    y_fade = fade(y - y_min)

    lerp1 = lerp(d0, d1, x_fade)
    lerp2 = lerp(d2, d3, x_fade)

    return lerp(lerp1, lerp2, y_fade)


def dot(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def fade(t):
    return 6*math.pow(t, 5) - 15 * math.pow(t, 4) + 10*math.pow(t, 3)


rnd = random.Random(seed)
offsets = []
for i in range(octaves):
    offsets.append(Vector2D(rnd.randrange(0, 10000), rnd.randrange(0, 10000)))

for y in range(height):
    for x in range(width):
        amplitude = 1
        frequency = 1
        noiseValue = 0
        for i in range(octaves):
            sampleX = x / scale * frequency + offsets[i].x
            sampleY = y / scale * frequency + offsets[i].y
            rawNoise = get_noise_value(sampleX, sampleY)
            noiseValue += rawNoise * amplitude
            amplitude *= persistence
            frequency *= lacunarity
        noise[x][y] = noiseValue

fig = plt.figure(frameon=False)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(noise, cmap='gray')
ax.axis('off')
fig.savefig("out.png")
fig.show()
