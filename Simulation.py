from Organism import Organism

NUM_ORGANISMS = 10
class Simulation:
    def __init__(self, main_game):
        self.organisms = []
        self.main_game = main_game
        self.initializeOrganisms()

    def initializeOrganisms(self):
        for x in range(NUM_ORGANISMS):
            self.organisms.append(Organism(x, self.main_game))

    def updateLogic(self):
        for x in range(len(self.organisms)):
            self.organisms[x].updateLogic()

    def display(self):
        for x in range(len(self.organisms)):
            self.organisms[x].display(self.main_game.screen)
