# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:02:58 2023

@author: sebas
"""
from dataclasses import dataclass
from math import log
import cmath
from PIL import Image
import matplotlib.cm
from PIL import ImageEnhance

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False) -> float:
        z = 0
        if c == 0:
            return self.max_iterations
        try:
            for iteration in range(self.max_iterations):
                z = cmath.exp((z ** 2 + z)/(c**(3/2)))
                if abs(z) > self.escape_radius:
                    if smooth:
                        return iteration + 1 - log(log(abs(z))) / log(2)
                    return iteration
        except:
            self.max_iterations
                
        return self.max_iterations

@dataclass
class Viewport:
    image: Image.Image
    center: complex
    width: float

    @property
    def height(self):
        return self.scale * self.image.height

    @property
    def offset(self):
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self):
        return self.width / self.image.width

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)

@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.getpixel((self.x, self.y))

    @color.setter
    def color(self, value):
        #print(self.x, self.y, value)
        self.viewport.image.putpixel((self.x, self.y), value)

    def __complex__(self):
        return (
                complex(self.x, -self.y)
                * self.viewport.scale
                + self.viewport.offset
        )

def paint(mandelbrot_set, viewport, palette, smooth):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        index = int(min(stability * len(palette), len(palette) - 1))
        pixel.color = palette[index % len(palette)]

def denormalize(palette):
    return [
        tuple(int(channel * 255) for channel in color)
        for color in palette
    ]

import numpy as np
from scipy.interpolate import interp1d

def make_gradient(colors, interpolation="linear"):
    X = [i / (len(colors) - 1) for i in range(len(colors))]
    Y = [[color[i] for color in colors] for i in range(3)]
    channels = [interp1d(X, y, kind=interpolation) for y in Y]
    return lambda x: [np.clip(channel(x), 0, 1) for channel in channels]


colormap = matplotlib.cm.get_cmap("twilight").colors
palette = denormalize(colormap)

#%%
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=1000)

width, height = 1080, 1080
scale = 0.003725
GRAYSCALE = "L"

image = Image.new(mode=GRAYSCALE, size=(width, height))
for y in range(height):
    for x in range(width):
        c = scale * complex(x - width / 2, height / 2 - y)
        if c == 0:
            continue
        try:
            instability = 1-mandelbrot_set.stability(c)
        except:
            continue
        image.putpixel((x, y), int(instability * 255))

image.show()

#%%

mandelbrot_set = MandelbrotSet(max_iterations=256, escape_radius=1000)

image = Image.new(mode="L", size=(512, 512))
for pixel in Viewport(image, center=-0.7435 + 0.1314j, width=0.002):
    c = complex(pixel)
    instability = 1 - mandelbrot_set.stability(c, smooth=True)
    pixel.color = int(instability * 255)

#image.show()

enhancer = ImageEnhance.Brightness(image)
enhancer.enhance(1.25).show()

#%%

mandelbrot_set = MandelbrotSet(max_iterations=512, escape_radius=1000)
image = Image.new(mode="RGB", size=(720, 720))
viewport = Viewport(image, center=-0.7435 + 0.1314j, width=0.002)
paint(mandelbrot_set, viewport, palette, smooth=True)
image.show()

#%%

exterior = [(1, 1, 1)] * 50
interior = [(1, 1, 1)] * 5
gray_area = [(1 - i / 44,) * 3 for i in range(45)]
palette = denormalize(exterior + gray_area + interior)

mandelbrot_set = MandelbrotSet(max_iterations=20, escape_radius=1000)
viewport = Viewport(image, center=-0.75, width=3.5)
paint(mandelbrot_set, viewport, palette, smooth=True)
image.show()
#%%

black = (0, 0, 0)
blue = (0, 0, 1)
maroon = (0.5, 0, 0)
navy = (0, 0, 0.5)
red = (1, 0, 0)

colors = [black, navy, blue, maroon, red, black]
gradient = make_gradient(colors, interpolation="cubic")

gradient(0.42)

num_colors = 256
palette = denormalize([
    gradient(i / num_colors) for i in range(num_colors)
])

image = Image.new(mode="RGB", size=(1800, 1260))
viewport = Viewport(image, center=0, width=3.5)
#viewport = Viewport(image, center=-0.7435 + 0.1314j, width=0.002)
mandelbrot_set = MandelbrotSet(max_iterations=20, escape_radius=1000)
paint(mandelbrot_set, viewport, palette, smooth=True)
image.show()