import random
import pygame
import math

SPEED = 5

class Projectile:
    def __init__(self, id, x, y, r, main_game, parent):
        self._parentId = id
        self.main_game = main_game
        self._x = x
        self._y = y
        self._r = r
        self._sprite = main_game.sprites['projectile']
        self.alive = True
        self.parent = parent

    def updateLogic(self):
        if self.alive:
            self._x += math.cos(self._r / 180.0 * math.pi) * SPEED
            self._y += math.sin(self._r / 180.0 * math.pi) * SPEED
            rect = self._sprite.get_rect()
            rect.left = self._x
            rect.top = self._y
            for organism in self.main_game.simulation.organisms:
                if organism._id == self._parentId:
                    continue
                if organism._rect.colliderect(rect) and organism.alive:
                    organism.kill()
                    self.parent.hunger -= 1
                    self.alive = False

            if self._x > self.main_game.screen_width - 25:
                return False
            if self._y > self.main_game.screen_height - 25:
                return False
            if self._x < 0:
                return False
            if self._y < 0:
                return False
            return True

    def display(self, screen):
        if self.alive:
            screen.blit(self._sprite, (round(self._x), round(self._y)))
