import pyxel
import math

from transforms import (
    mat_translate,
    mat_rotate,
    mat_mul,
    apply_matrix,
)


def get_shape_points(size=20):
    # Return the points of a square centered at (W / 2, H / 2)
    # This can be modified to return different shapes, but the purpose is to demonstrate
    # that a group of points can be transformed together using matrix operations.
    return [
        (W / 2 - size / 2, H / 2 - size / 2),
        (W / 2 + size / 2, H / 2 - size / 2),
        (W / 2 + size / 2, H / 2 + size / 2),
        (W / 2 - size / 2, H / 2 + size / 2),
    ]


# Start M as identity matrix - does not change points
M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# Set a current rotation angle
rotation_angle = 0.0  # radians

# Set window size and initialize pyxel
W = 160
H = 120
pyxel.init(W, H, title="matrix transforms")


def update():
    global M, rotation_angle

    # This is where we update the transformation matrix M

    # First, uncomment this next line, which translates the matrix by (30, -10)
    # M = mat_translate(30, -10)

    # When you update the matrix M, it then is applied to all points in the draw() function,
    # so you should see the shape move by (30, -10) pixels each frame.

    # Next, uncomment this next line, which rotates the matrix 45 degress.
    # Since we are overwriting M, the translation above is lost, and it should only rotate.
    # M = mat_rotate(math.radians(45))

    # Does this look correct? No! Why?...
    # The rotation is around the origin (0,0), which is the top-left corner of the window.
    # So the shape is rotating around that point, which makes it go off-screen.
    # To fix this, we need to rotate around the center of the shape.
    # To rotate around the center of the shape, we need to:
    # 1. Translate the shape so that its center is at the origin
    # 2. Apply the rotation
    # 3. Translate the shape back to its original position

    # Uncomment the following block to see the correct rotation around the center.
    # Notice, we are cascading matrix multiplications to build up the final transformation matrix.
    # This is like saying M = T_center * R * T_neg_center
    # cx, cy = W / 2, H / 2
    # M = mat_mul(
    #     mat_translate(cx, cy),
    #     mat_mul(mat_rotate(math.radians(45)), mat_translate(-cx, -cy)),
    # )

    # Let's animate the rotation instead of using a fixed 45 degree angle
    # We can increase the rotation angle each frame and then use that angle in the rotation matrix
    # Uncomment the following block to see the animated rotation
    # rotation_angle += math.radians(4)
    # M = mat_mul(
    #     mat_translate(cx, cy),
    #     mat_mul(mat_rotate(rotation_angle), mat_translate(-cx, -cy)),
    # )

    # Now, what is we want to rotate our shape around the center offset by 30 pixels from the center?
    # To do that, we just translate the whole transformation by (30, 30), by uncommenting the next line:
    # M = mat_mul(M, mat_translate(30, 30))

    # Just to experiment, let's see what happens if we reverse the order of the matrix multiplications above,
    # so instead of moving everything by (30,30) after the rotation, we move it first.
    # To do this, first put the comment back on the previous block, and then uncomment the next line:
    # M = mat_mul(mat_translate(30, 30), M)

    # Order of operations matters!


def draw():
    pyxel.cls(0)

    # Get the shape points
    points = get_shape_points()

    # Get a copy of the points with the transformation matrix applied
    # This is the beautiful part of using matrix transformations - we can apply
    # the same matrix to a whole set of points easily.
    # In this example, there are only 4 points, but imagine if there were hundreds or thousands!
    transformed_points = [apply_matrix(M, x, y) for (x, y) in points]

    # Draw original shape
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        pyxel.line(x1, y1, x2, y2, 7)  # original shape

    # Draw transformed shape
    for i in range(len(transformed_points)):
        x1, y1 = transformed_points[i]
        x2, y2 = transformed_points[(i + 1) % len(transformed_points)]
        pyxel.line(x1, y1, x2, y2, 8)  # transformed shape


pyxel.run(update, draw)
