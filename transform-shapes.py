import pyxel
import math

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


pyxel.init(200, 150, title="Matrix Transform Demo")

# assign some positions for "stars"
stars = [
    (-80, -60),
    (-50, -20),
    (0, -70),
    (50, -50),
    (-30, 40),
    (20, 70),
    (70, 10),
    (-70, 20),
]

# state
angle = 0
M = [  # identiy matrix
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]


def update():
    global M, angle
    angle += 0.03

    # Pulsating scale
    s = 1 + 0.5 * math.sin(angle * 2)

    # Transform: scale → rotate → translate
    M_scale = mat_scale(s, s)
    M_rotate = mat_rotate(angle)
    M_translate = mat_translate(100, 75)

    M = mat_mul(M_translate, mat_mul(M_rotate, M_scale))


def draw():
    pyxel.cls(0)

    # Rendeer a triangle with the matrix transform
    tri_transformed(M, -20, -10, 20, -10, 0, 20, 11)

    # Render a rectangle
    quad_transformed(M, -15, -15, 15, -15, 15, 15, -15, 15, 8)

    # Alternatively, render a rectangle as two triangles
    tri_transformed(M, -5, -5, 5, -5, 5, 5, 9)
    tri_transformed(M, -5, -5, 5, 5, -5, 5, 9)

    # render some "stars"
    for sx, sy in stars:
        tx, ty = apply_matrix(M, sx, sy)
        pyxel.pset(int(tx), int(ty), 7)

    # flower shape
    num_petals = 8
    radius = 25

    for i in range(num_petals):
        a0 = (math.pi * 2 / num_petals) * i
        a1 = a0 + 0.4

        x1, y1 = (math.cos(a0) * radius, math.sin(a0) * radius)
        x2, y2 = (math.cos(a1) * radius, math.sin(a1) * radius)
        x3, y3 = (0, 0)  # center

        tri_transformed(M, x1, y1, x2, y2, x3, y3, 10)


pyxel.run(update, draw)
