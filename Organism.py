import random
import pygame
from pygame.locals import *

import math

from Projectile import Projectile
from FuzzyRayTracer import FuzzyRayTracer
from neat import nn, population, statistics

SPEED = 3

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Organism:
    def __init__(self, x, main_game, genome):
        self._id = x
        self.main_game = main_game
        self._x = random.randint(0, self.main_game.screen_width) * 1.0
        self._y = random.randint(0, self.main_game.screen_height) * 1.0
        self._r = random.randint(0, 360) * 1.0
        self._line = 0
        self._sprite = pygame.Surface((20, 20))
        pygame.draw.polygon(self._sprite, Color("Green"), ((6, 0), (0, 12), (12, 12)))

        self._net = nn.create_feed_forward_phenotype(genome)
        self._genome = genome
        self._rect = self._sprite.get_rect()
        self.projectiles = []
        self.alive = True
        self._genome.fitness = 0
        self.hunger = 0
        self.reload = 0

    def kill(self):
        self.alive = False
        self._genome.fitness += (10 - self.hunger) * 100

    def updateLogic(self):
        if self.alive:
            self.reload -= 1
            self.hunger += 0.01
            if self.hunger >= 10:
                self.kill()
            self._genome.fitness += 1
            points = []
            amount = 0
            for organism in self.main_game.simulation.organisms:
                amount += 1
                if self._id == organism._id:
                    continue
                if organism.alive:
                    points.append((organism._x, organism._y, -1))
                    for projectile in organism.projectiles:
                        if projectile.alive:
                            points.append((organism._x, organism._y, 1))
            rayTracer = FuzzyRayTracer(points, self._x, self._y, self._r)
            inputs = rayTracer.trace()
            inputs += [self._x / self.main_game.screen_width, self._y / self.main_game.screen_height]
            out = self._net.serial_activate(inputs)

            self._r += 10 * (out[0] - 0.5)

            if out[2] > 0.5 and self.reload <= 0:
                self.shoot()
                self.reload = 50

            self._r  %= 360
            if out[3] > 0.2:
                self._x += math.cos(self._r / 180.0 * math.pi) * SPEED * (out[3] - 0.2) * 1.2
                self._y += math.sin(self._r / 180.0 * math.pi) * SPEED * (out[3] - 0.2) * 1.2

            self._rect.left = self._x
            self._rect.top = self._y
            offset = 0
            for x in range(len(self.projectiles)):
                if self.projectiles[x - 1 + offset].updateLogic() == False:
                    del self.projectiles[x - 1 + offset]
                    offset -= 1
            if self._x > self.main_game.screen_width - 25:
                self._x = self.main_game.screen_width - 25
                self.hunger += 0.05
            if self._y > self.main_game.screen_height - 25:
                self._y = self.main_game.screen_height - 25
                self.hunger += 0.05
            if self._x < 0:
                self._x = 0
                self.hunger += 0.05
            if self._y < 0:
                self._y = 0
                self.hunger += 0.05
    def shoot(self):
        self.projectiles.append(Projectile(self._id, self._x, self._y, self._r, self.main_game, self))
        self.hunger += 0.2;

    def drawVector(self, r, l):
        pygame.draw.line(self.main_game.screen, Color("white"), (self._x + 6, self._y + 6), (self._x + 6 + math.cos(r) * l, self._y + 6 + math.sin(r) * l), 1)

    def display(self, screen):
        if self.alive:

            screen.blit(self._sprite, (round(self._x), round(self._y)))
            for x in range(len(self.projectiles)):
                self.projectiles[x - 1].display(screen)
            # self.drawVector(self._line, 100)
            self.drawVector(self._r / 180 * math.pi, 20)
            text_str = "food: " + str(10 - self.hunger) + ", fit: " + str(self._genome.fitness)
            font = pygame.font.Font(None, 15)
            text = font.render(text_str, 1, (255, 255, 255))
            screen.blit(text, (round(self._x), round(self._y) + 12))

            # for x in range(20):
            #     self.drawVector((self._r - 60 + 6*x) / 180 * math.pi, 100)
