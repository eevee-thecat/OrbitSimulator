import itertools
import math
import random
import turtle
from time import sleep

SCREEN = None
WIDTH = 1400
HEIGHT = 1000


class Sun(turtle.Turtle):
    id: str = "Sun"
    size: int = 50
    mass: int = 10_000  # Mass is much larger than the planets
    x_vel: float = 0
    y_vel: float = 0

    # Position is fixed at 0,0

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("yellow")
        self.setposition(0, 0)

    def draw(self):
        self.setx(self.xcor() + self.x_vel)
        self.sety(self.ycor() + self.y_vel)
        self.clear()
        self.dot(self.size)


class Planet(turtle.Turtle):
    id: str = "Planet"
    size: int = 15
    mass: int
    x_vel: float
    y_vel: float

    def __init__(self, color: str, mass: int, x_pos: int, y_pos: int, x_vel: float, y_vel: float):
        super().__init__()
        self.color(color)
        self.setposition(x_pos, y_pos)
        self.mass = mass
        self.x_vel = x_vel
        self.penup()
        self.hideturtle()
        self.y_vel = y_vel

    def draw(self):
        self.setx(self.xcor() + self.x_vel)
        self.sety(self.ycor() + self.y_vel)
        self.clear()
        self.dot(self.size)


def accelerate(first, second):
    force = first.mass * second.mass / first.distance(second) ** 2
    angle = first.towards(second)
    reverse = 1
    for body in first, second:
        acceleration = force / body.mass
        acc_x = acceleration * math.cos(math.radians(angle))
        acc_y = acceleration * math.sin(math.radians(angle))
        body.x_vel += (reverse * acc_x)
        body.y_vel += (reverse * acc_y)
        reverse = -1


def collide(first, second) -> bool:
    if first.distance(second) < first.size / 2 + second.size / 2:
        return first.id == "Planet"


def loop():
    global SCREEN
    SCREEN = turtle.Screen()
    SCREEN.tracer(0)
    SCREEN.setup(WIDTH, HEIGHT)
    SCREEN.bgcolor("black")
    sun = Sun()
    sun.draw()
    planet_1 = Planet("blue", 1, -250, 0, 0, random.uniform(4, 6))
    planet_1.draw()
    planet_2 = Planet("green", 1, 100, 100, -5, random.uniform(4, 6))
    planet_2.draw()
    planet_3 = Planet("orange", 1, 350, 250, 0, random.uniform(4, 6))
    planet_3.draw()
    SCREEN.update()

    objects = [sun, planet_1, planet_2, planet_3]

    while True:
        for left_index in range(len(objects) - 1):
            for right_index in range(left_index + 1, len(objects)):
                accelerate(objects[left_index], objects[right_index])

        removes = [False for _ in range(len(objects))]
        for left_index in range(len(objects)):
            for right_index in range(len(objects)):
                if left_index != right_index:
                    removes[left_index] = collide(objects[left_index], objects[right_index])

        new_objects = []
        for index, remove in enumerate(removes):
            if not remove:
                new_objects.append(objects[index])
            else:
                objects[index].clear()
        objects = new_objects
        for object in objects:
            object.draw()

        SCREEN.update()
        sleep(0.01)

    # make sun


def main():
    loop()


if __name__ == '__main__':
    main()
    sleep(10000)
