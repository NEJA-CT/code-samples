import pyxel

from circle import Circle

W, H = 720, 680
CIRCLE_SPEED = 20


def create_random_circle():
    x = pyxel.rndi(0, W)
    y = pyxel.rndi(0, H)
    angle = pyxel.rndf(0, 360)
    dx = pyxel.cos(angle) * CIRCLE_SPEED
    dy = pyxel.sin(angle) * CIRCLE_SPEED
    radius = pyxel.rndi(20, 60)
    color = pyxel.rndi(1, 15)
    return Circle(x, y, dx, dy, radius=radius, color=color)


class App:
    def __init__(self):
        pyxel.init(W, H, title="Circle")

        self.circles = []

        pyxel.run(self.update, self.draw)

    def update(self):
        for circle in self.circles:
            circle.update()
            circle.bounce_wall(W, H)

        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                self.circles[i].bounce_off(self.circles[j])

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            new_circle = create_random_circle()
            self.circles.append(new_circle)

    def draw(self):
        pyxel.cls(0)
        for circle in self.circles:
            circle.draw()


App()
