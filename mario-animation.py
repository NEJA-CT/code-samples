import pyxel

W, H = 320, 240
pyxel.init(W, H, title="mario moves")

mario_image = pyxel.Image.from_image("assets/mario.png")
pyxel.images[0] = mario_image


def draw_mario(mario_x, mario_y, mario_tile):
    mario_width = mario_image.width / 3
    pyxel.blt(
        mario_x,
        mario_y,  # position of Mario in the viewport
        0,  # image id
        (mario_width * mario_tile) - 1,
        0,  # top-left pixel in the Mario image
        mario_width,
        mario_image.height,  # width/height of the Mario image
    )


mario_frame = 0


def draw():
    pyxel.cls(0)
    draw_mario(30, 20, mario_frame)


def update():
    global mario_frame
    mario_frame = int(pyxel.frame_count / 4) % 3


pyxel.run(update, draw)
