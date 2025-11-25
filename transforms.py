import math

# Standard transform functions


def translate(point, tx, ty):
    x, y = point
    return x + tx, y + ty


def scale(point, sx, sy):
    x, y = point
    return x * sx, y * sy


def rotate(point, angle_radians):
    x, y = point
    c = math.cos(angle_radians)
    s = math.sin(angle_radians)
    return x * c - y * s, x * s + y * c


# Matrix functions


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
