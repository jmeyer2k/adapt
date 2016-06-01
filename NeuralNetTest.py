from __future__ import print_function

import os
import pickle

from neat import nn, population, statistics
from main import MainSimulation

NUM_ORGANISMS = 10

main_simulation = MainSimulation()

def eval_fitness(genomes):
    main_simulation.eval_fitness(genomes)
    while not main_simulation.sim_over:
        main_simulation.loop()
    main_simulation.simulation.organisms = [];

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'neuron_config')
pop = population.Population(config_path)
pop.run(eval_fitness, 500)

print('Number of evaluations: {0}'.format(pop.total_evaluations))

# Display the most fit genome.
winner = pop.statistics.best_genome()
print('\nBest genome:\n{!s}'.format(winner))

with open('nn_winner_genome', 'wb') as f:
    pickle.dump(winner, f)

# # Visualize the winner network and plot/log statistics.
# visualize.plot_stats(pop.statistics)
# visualize.plot_species(pop.statistics)
# visualize.draw_net(winner, view=True, filename="xor2-all.gv")
# visualize.draw_net(winner, view=True, filename="xor2-enabled.gv", show_disabled=False)
# visualize.draw_net(winner, view=True, filename="xor2-enabled-pruned.gv", show_disabled=False, prune_unused=True)
# statistics.save_stats(pop.statistics)
# statistics.save_species_count(pop.statistics)
# statistics.save_species_fitness(pop.statistics)
