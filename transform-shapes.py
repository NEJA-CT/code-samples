import pyxel
import math
import random

# -------------------------------------------------
# Matrix Transform Functions
# -------------------------------------------------


def mat_translate(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1],
    ]


def mat_scale(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1],
    ]


def mat_rotate(a):
    c, s = math.cos(a), math.sin(a)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1],
    ]


def mat_mul(A, B):
    M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for r in range(3):
        for c in range(3):
            M[r][c] = sum(A[r][k] * B[k][c] for k in range(3))
    return M


def apply_matrix(M, x, y):
    tx = M[0][0] * x + M[0][1] * y + M[0][2]
    ty = M[1][0] * x + M[1][1] * y + M[1][2]
    return tx, ty


# -------------------------------------------------
# Rendering Functions
# -------------------------------------------------


def line_transformed(M, x1, y1, x2, y2, col):
    tx1, ty1 = apply_matrix(M, x1, y1)
    tx2, ty2 = apply_matrix(M, x2, y2)
    pyxel.line(tx1, ty1, tx2, ty2, col)


def quad_transformed(M, x1, y1, x2, y2, x3, y3, x4, y4, col, outline=False):
    # Transform each corner
    tx1, ty1 = apply_matrix(M, x1, y1)
    tx2, ty2 = apply_matrix(M, x2, y2)
    tx3, ty3 = apply_matrix(M, x3, y3)
    tx4, ty4 = apply_matrix(M, x4, y4)

    if outline:
        # Draw 4 edge lines
        pyxel.line(tx1, ty1, tx2, ty2, col)
        pyxel.line(tx2, ty2, tx3, ty3, col)
        pyxel.line(tx3, ty3, tx4, ty4, col)
        pyxel.line(tx4, ty4, tx1, ty1, col)

    else:
        # Draw filled quad as two triangles
        pyxel.tri(tx1, ty1, tx2, ty2, tx3, ty3, col)
        pyxel.tri(tx1, ty1, tx3, ty3, tx4, ty4, col)


def tri_transformed(M, x1, y1, x2, y2, x3, y3, col, outline=False):
    tx1, ty1 = apply_matrix(M, x1, y1)
    tx2, ty2 = apply_matrix(M, x2, y2)
    tx3, ty3 = apply_matrix(M, x3, y3)

    if outline:
        pyxel.trib(tx1, ty1, tx2, ty2, tx3, ty3, col)
    else:
        pyxel.tri(tx1, ty1, tx2, ty2, tx3, ty3, col)


def flower_transformed(M, cx, cy, r, col, num_petals=8):
    for i in range(num_petals):
        a0 = (math.pi * 2 / num_petals) * i
        a1 = a0 + 0.4

        x1, y1 = cx + math.cos(a0) * r, cy + math.sin(a0) * r
        x2, y2 = cx + math.cos(a1) * r, cy + math.sin(a1) * r

        tri_transformed(M, cx, cy, x1, y1, x2, y2, col)


def ellipse_transformed(M, cx, cy, rx, ry, col, segments=32, outline=False):
    # Precalculate the points of the circle
    points = []
    for i in range(segments):
        a = (i / segments) * math.tau
        x = cx + math.cos(a) * rx
        y = cy + math.sin(a) * ry
        tx, ty = apply_matrix(M, x, y)
        points.append((tx, ty))

    if outline:
        # Connect successive transformed points
        for i in range(segments):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % segments]
            pyxel.line(x1, y1, x2, y2, col)

    else:
        # Fill by triangulating around the center
        cx_t, cy_t = apply_matrix(M, cx, cy)
        for i in range(segments):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % segments]
            pyxel.tri(cx_t, cy_t, x1, y1, x2, y2, col)


def circle_transformed(M, cx, cy, r, col, segments=32, outline=False):
    # A circle is just an ellipse with the same x/y radius
    ellipse_transformed(M, cx, cy, r, r, col, segments, outline)


pyxel.init(200, 150, title="Matrix Transform Demo")

# assign some random positions for "stars"
stars = []
for _ in range(200):
    stars.append((random.randint(-200, 200), random.randint(-200, 200)))

# state
angle = 0
M = [  # identiy matrix
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]


def update():
    global M, angle
    angle += 0.03  # increment rotation every frame

    # Pulsating scale
    s = 1 + 0.5 * math.sin(angle * 2)

    # Transform: scale → rotate → translate
    M_scale = mat_scale(s, s)
    M_rotate = mat_rotate(angle)
    M_translate = mat_translate(100, 75)  # center around (0, 0)

    M = mat_mul(M_translate, mat_mul(M_rotate, M_scale))


def draw():
    pyxel.cls(0)

    # Rendeer a triangle
    tri_transformed(M, -20, -10, 20, -10, 0, 20, col=11)

    # Render a rectangle
    quad_transformed(M, -15, -15, 15, -15, 15, 15, -15, 15, col=8)

    # Render a rectangle outline
    quad_transformed(M, -20, -20, 20, -20, 20, 20, -20, 20, col=5, outline=True)

    # Alternatively, render a rectangle as two triangles explicitly
    tri_transformed(M, -5, -5, 5, -5, 5, 5, col=9)
    tri_transformed(M, -5, -5, 5, 5, -5, 5, col=9)

    # Render a flower shape
    flower_transformed(M, 0, 0, 25, col=10, num_petals=3)

    # Render a circle
    circle_transformed(M, 0, 0, 10, col=12)

    # Render a circle outline
    circle_transformed(M, 0, 0, 14, col=13, outline=True)

    # Render some "stars"
    for sx, sy in stars:
        tx, ty = apply_matrix(M, sx, sy)
        pyxel.pset(int(tx), int(ty), 7)


pyxel.run(update, draw)
