from __future__ import print_function, division
import sys, os
import pickle
from floor_plans.genome import Genome
from floor_plans.config import Config
from floor_plans.indexer import Indexer, InnovationIndexer
from floor_plans.visualize import View
from floor_plans.floorplan import FloorPlan
from main import evaluate, create_scores
from floor_plans.hallways import create_hallways
from floor_plans.hallway_smoothing import smooth
from floor_plans.hallway_geometry import create_geometry
from floor_plans import floorplan_statistics as fps

# todo
def grid_search(floor):
    best_score = 999999999
    best_args = None
    decay = .2
    k = 10
    start_pheromone = 0
    iters = 15
    alpha = 2
    for k in range(1, 20, 2):
        args = {'alpha':alpha, 'iters':iters, 'k':k,
                'pheromone_decay':decay,
                'start_pheromone':start_pheromone}
        create_hallways(floor, verbose=False, **args)
        floor.hallway_geometry = create_geometry(floor)
        floor.stats = fps.calculate_all(floor)
        print('alpha=',round(alpha, 2), 'k=',k, 'decay=',decay, 'ha=', floor.stats['ha'])

        if floor.stats['fe'] < best_score:
            best_args = args
            best_score = floor.stats['fe']
    create_hallways(floor, verbose=False, **best_args)
    floor.hallway_geometry = create_geometry(floor)
    floor.stats = fps.calculate_all(floor)
    smooth(floor)
    return floor

def main(genome, cache=False, save_path=None, scale=1.8):
    bounds = (int(750.*scale), int(750.*scale))
    view = View(*bounds, scale=scale)
    floor = FloorPlan.from_genome(genome, view=view, cache=cache)
    view.draw_floorplan(floor, genome=None)

    if save_path:
        view.save(save_path)
    view.hold()

if __name__ == '__main__':
    genome = pickle.load(open('winner_genome.p', 'rb'))
    main(genome, 
         cache=True, 
         scale=2, 
         save_path=os.path.join(os.path.dirname("./"), 'render.png'))
