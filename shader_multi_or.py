#!/usr/bin/env python
""" pg.examples.video
Experimental!
* dialog message boxes with messagebox.
* multiple windows with Window
* driver selection
* Renderer, Texture, and Image classes
* Drawing lines, rects, and such onto Renderers.
"""
import os
import pygame as pg
from crt_shader import Graphic_engine

if pg.get_sdl_version()[0] < 2:
    raise SystemExit(
        "This example requires pygame 2 and SDL2. _sdl2 is experimental and will change."
    )
from pygame._sdl2 import Window, Texture, Image, Renderer, get_drivers, messagebox

data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], "data")


def load_img(file):
    return pg.image.load(os.path.join(data_dir, file))


pg.display.init()
pg.key.set_repeat(1000, 10)

for driver in get_drivers():
    print(driver)


answer = messagebox(
    "I will open two windows! Continue?",
    "Hello!",
    info=True,
    buttons=("Yes", "No"),
    return_button=0,
    escape_button=1,
)
if answer == 1:
    import sys
    sys.exit(0)

pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
win = Window.from_display_module()
# win = Window("asdf", resizable=True)
renderer = Renderer(win)
screen = pg.Surface((800, 600)).convert((255, 65280, 16711680, 0))
img = pg.image.load('data/image.png')
screen.blit(img, (0, 0))
# tex = Texture.from_surface(renderer, load_img("image.png"))

# renderer.clear()
# tex.draw()
shader1 = Graphic_engine(screen)

running = True

x, y = 250, 50
clock = pg.time.Clock()

bg_index = 0


win2 = Window("2nd window", size=(256, 256), always_on_top=True)
win2.opacity = 1
# win2.set_icon(load_img("bomb.gif"))
renderer2 = Renderer(win2)
tex2 = Texture.from_surface(renderer2, load_img("image.png"))
renderer2.clear()
tex2.draw()
renderer2.present()
del tex2

full = 0


surf = pg.Surface((64, 64))
streamtex = Texture(renderer, (64, 64), streaming=True)
tex_update_interval = 1000
next_tex_update = pg.time.get_ticks()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif getattr(event, "window", None) == win2:
            if (
                event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE
                or event.type == pg.WINDOWCLOSE
            ):
                win2.destroy()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                if full == 0:
                    win.set_fullscreen(True)
                    full = 1
                else:
                    win.set_windowed()
                    full = 0

    # renderer.clear()
    # renderer.blit(screen)
    # renderer.present()
    shader1.render()

    clock.tick(60)
    win.title = str(f"FPS: {clock.get_fps()}")

pg.quit()