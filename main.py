import pygame
from Simulation import Simulation

STEPBYSTEP = False

class MainSimulation:
    def __init__(self):
        pygame.init()

        self.sprites = {
            'projectile': pygame.image.load('projectile.bmp')
        }

        self.screen_width, self.screen_height = 900, 700

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.simulation = Simulation(self)

        self.running = True

    def updateLogic(self):
        self.simulation.updateLogic()

    def display(self):
        self.screen.fill(0)
        self.simulation.display()
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and STEPBYSTEP:
                    self.updateLogic()


    def loop(self):
        self.handleEvents()
        if not STEPBYSTEP:
            self.updateLogic()
        self.display()

if __name__ == '__main__':
    sim = MainSimulation()
    while sim.running:
        sim.loop()
    exit(0)
