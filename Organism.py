import random
import pygame
from pygame.locals import *

import math

from Projectile import Projectile
from FuzzyRayTracer import FuzzyRayTracer

SPEED = 3

class Organism:
    def __init__(self, x, main_game):
        self._id = x
        self.main_game = main_game
        self._x = random.randint(0, self.main_game.screen_width) * 1.0
        self._y = random.randint(0, self.main_game.screen_height) * 1.0
        self._r = random.randint(0, 360) * 1.0
        self._line = 0
        font = pygame.font.Font(None, 36)
        self._sprite = font.render(str(x), 1, (255, 255, 255))

        self._rect = self._sprite.get_rect()
        self.projectiles = []
        self.alive = True

    def kill(self):
        self.alive = False

    def updateLogic(self):
        if self.alive:
            # print(self.projectiles)
            # print(self._id % 2 == 0)
            self._r  %= 360
            self._x += math.cos(self._r / 180.0 * math.pi) * SPEED
            self._y += math.sin(self._r / 180.0 * math.pi) * SPEED
            points = []
            for organism in self.main_game.simulation.organisms:
                if self._id == organism._id:
                    continue
                if organism.alive:
                    points.append((organism._x, organism._y))
            rayTracer = FuzzyRayTracer(points, self._x, self._y, self._r)
            rayTracer.trace()

            self._rect.left = self._x
            self._rect.top = self._y
            offset = 0
            if random.randint(1,50) == 1:
                pass
                # self.shoot()
            for x in range(len(self.projectiles)):
                if self.projectiles[x - 1 + offset].updateLogic() == False:
                    del self.projectiles[x - 1 + offset]
                    offset -= 1
            if self._x > self.main_game.screen_width - 25:
                self._x = self.main_game.screen_width - 25
            if self._y > self.main_game.screen_height - 25:
                self._y = self.main_game.screen_height - 25
            if self._x < 0:
                self._x = 0
            if self._y < 0:
                self._y = 0

    def shoot(self):
        self.projectiles.append(Projectile(self._id, self._x, self._y, self._r, self.main_game))

    def drawVector(self, r, l):
        pygame.draw.line(self.main_game.screen, Color("white"), (self._x, self._y), (self._x + math.cos(r) * l, self._y + math.sin(r) * l), 1)

    def display(self, screen):
        if self.alive:
            screen.blit(self._sprite, (round(self._x), round(self._y)))
            for x in range(len(self.projectiles)):
                self.projectiles[x - 1].display(screen)
            # self.drawVector(self._line, 100)
            self.drawVector(self._r / 180 * math.pi, 100)
            for x in range(20):
                self.drawVector((self._r - 60 + 6*x) / 180 * math.pi, 100)
