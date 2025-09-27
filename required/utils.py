from casioplot import *
from random import *
from math import *

# Reimplementation
def enumerate(iterable):
    n = 0
    for item in iterable:
        yield (n, item)
        n += 1

# Draw rectangles
def draw_rect(start_x, start_y, end_x, end_y, color):
    width = abs(end_x - start_x)
    height = abs(end_y - start_y)
    for x in range(width + 1):
        for y in range(height + 1):
            set_pixel(start_x + x, start_y + y, color)

# Span drawer for solid circles
def _plot_solid_octant_spans(cx, cy, x, y, color):
    for i in range(cx - x, cx + x + 1):
        set_pixel(i, cy + y, color) # Upper half
        set_pixel(i, cy - y, color) # Lower half
    if x != y:
        for i in range(cx - y, cx + y + 1):
            set_pixel(i, cy + x, color) # Upper half, inner section
            set_pixel(i, cy - x, color) # Lower half, inner section

# Plots the octant points of a circumference
def _plot_octant_pixels(cx, cy, x, y, place_pixel_func):
    set_pixel(cx + x, cy + y, color)
    set_pixel(cx - x, cy + y, color)
    set_pixel(cx + x, cy - y, color)
    set_pixel(cx - x, cy - y, color)
    set_pixel(cx + y, cy + x, color)
    set_pixel(cx - y, cy + x, color)
    set_pixel(cx + y, cy - x, color)
    set_pixel(cx - y, cy - x, color)

# Circle drawer shared backend
def _bresenham_core(cx, cy, r, color, plot_func):
    if r < 0: return
    x = 0
    y = r
    p = 1 - r # Initial decision parameter
    plot_func(cx, cy, x, y, color)
    while x < y:
        x += 1
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * x - 2 * y + 1
        plot_func(cx, cy, x, y, color)

# Draw a solid circle
def draw_circle_solid(cx, cy, radius, color):
    _bresenham_core(cx, cy, radius, color, _plot_solid_octant_spans)

# Draw a circle circumference
def draw_circle_circumference(cx, cy, radius, thickness, color):
    half_thickness_floor = thickness // 2
    half_thickness_ceil = (thickness + 1) // 2
    r_min = max(0, radius - half_thickness_floor)
    r_max = radius + half_thickness_ceil - 1
    for r in range(r_min, r_max + 1):
        _bresenham_core(cx, cy, r, color, _plot_octant_pixels)

# My splash screen - For games
def splash_screen():
    clear_screen()
    draw_string(20,20,"Made by Alex")
    draw_string(20,40,"casio.alexvde.dev")
    show_screen()
    for x in range(1):
        ramp_up = range(1, 255, 4) 
        ramp_down = range(255, -1, -4) 
        g = 0
        for g in ramp_up:
            draw_rect(9, 20, 11, 60, (255, g, 0))
            show_screen()
        r = 255
        for r in ramp_down:
            draw_rect(9, 20, 11, 60, (r, 255, 0))
            show_screen()
        b = 0
        for b in ramp_up:
            draw_rect(9, 20, 11, 60, (0, 255, b))
            show_screen()
        g = 255
        for g in ramp_down:
            draw_rect(9, 20, 11, 60, (0, g, 255))
            show_screen()
        r = 0
        for r in ramp_up:
            draw_rect(9, 20, 11, 60, (r, 0, 255))
            show_screen()
        b = 255
        for b in ramp_down:
            draw_rect(9, 20, 11, 60, (255, 0, b))
            show_screen()
