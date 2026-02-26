import pyxel


class Circle:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

    def bounce_wall(self, width, height):
        if self.x < self.radius or self.x > width - self.radius:
            self.x = min(max(self.x, self.radius), width - self.radius)
            self.vx = -self.vx

        if self.y < self.radius or self.y > height - self.radius:
            self.y = min(max(self.y, self.radius), height - self.radius)
            self.vy = -self.vy

    def bounce_off(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        min_dist = self.radius + other.radius
        dist_sq = dx * dx + dy * dy
        if dist_sq > min_dist * min_dist:
            return False

        if dist_sq == 0:
            dx, dy, dist = 1, 0, 1
        else:
            dist = dist_sq**0.5

        nx = dx / dist
        ny = dy / dist
        overlap = min_dist - dist
        if overlap > 0:
            correction = overlap / 2
            self.x -= nx * correction
            self.y -= ny * correction
            other.x += nx * correction
            other.y += ny * correction

        closing_speed = (self.vx - other.vx) * nx + (self.vy - other.vy) * ny
        if closing_speed <= 0:
            return True

        self.vx -= closing_speed * nx
        self.vy -= closing_speed * ny
        other.vx += closing_speed * nx
        other.vy += closing_speed * ny
        return True
