from Organism import Organism

class Simulation:
    def __init__(self, main_game):
        self.organisms = []
        self.main_game = main_game

    def eval_fitness(self, genomes):
        org_id = 0
        for g in genomes:
            self.organisms.append(Organism(org_id, self.main_game, g))
            org_id += 1

    def updateLogic(self):
        alive_organisms = 0
        for x in range(len(self.organisms)):
            if self.organisms[x].alive:
                alive_organisms += 1
            self.organisms[x].updateLogic()
        # print alive_organisms
        if alive_organisms <= 1:
            self.main_game.sim_over = True

    def display(self):
        for x in range(len(self.organisms)):
            self.organisms[x].display(self.main_game.screen)
