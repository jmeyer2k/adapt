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

        self.sim_over = False

        self.graphics_on = True

    def updateLogic(self):
        self.simulation.updateLogic()

    def eval_fitness(self, genomes):
        self.sim_over = False
        self.simulation.eval_fitness(genomes)

    def display(self):
        if self.graphics_on:
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
                if event.key == pygame.K_y:
                    self.graphics_on = not self.graphics_on



    def loop(self):
        # if not self.graphics_on:
        #     print len(self.simulation.organisms)
        self.handleEvents()
        if not STEPBYSTEP:
            self.updateLogic()
        self.display()

if __name__ == '__main__':
    sim = MainSimulation()
    while sim.running:
        sim.loop()
    exit(0)
