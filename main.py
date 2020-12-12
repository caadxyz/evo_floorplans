#coding=utf-8
from __future__ import print_function, division
import os
import pickle
import math
import sys
import gzip
from itertools import combinations
from datetime import datetime

from floor_plans import population, concave_hull
from floor_plans.floorplan import FloorPlan, UnconnectedGenomeException, InvalidContraintException
from floor_plans.math_util import mean, geometric_mean, weighted_geometric_mean
from floor_plans.visualize import View
from floor_plans.visualize_evolution import plot_stats,  plot_species
from floor_plans.config import Config
from floor_plans.parallel import ParallelEvaluator
from floor_plans import statistics
from floor_plans.spec import BuildingSpec
from spec4test import spec
from floor_plans import floorplan_statistics
from pyvoro import voroplusplus
import networkx as nx
import sys
sys.dont_write_bytecode = True

def evaluate(genome):
    try:
       floor = FloorPlan.from_genome(genome)
       return floor, -floor.stats['wl']

    except UnconnectedGenomeException as e:
        sys.stdout.write('1')
        sys.stdout.flush()
        return (None, -99999999)
    except concave_hull.InvalidHullException as e:
        sys.stdout.write('2')
        sys.stdout.flush()
        return (None, -99999999)
    except voroplusplus.VoronoiPlusPlusError as e:
        sys.stdout.write('3')
        sys.stdout.flush()
        # pickle.dump(genome, open('debug/voronoi_genome.p', 'wb'))
        return (None, -99999999)
    except InvalidContraintException as e:
        sys.stdout.write('4')
        sys.stdout.flush()
        # pickle.dump(genome, open('debug/constraint_genome.p', 'wb'))
        return (None, -99999999)
    except Exception as e:
        sys.stdout.write('E')
        sys.stdout.flush()
        print(e,  end='')
        return (None, -99999999)

scale = 1.0
view = View(int(750.*scale), int(750.*scale), scale=scale)

def draw_genome(genome):
    floorplan = FloorPlan.from_genome(genome)
    view.draw_floorplan(floorplan)

def evaluate_all(genomes):
    for genome in genomes:
        _, fitness = evaluate(genome)
        genome.fitness = fitness
    best = max(genomes, key=lambda g: g.fitness)
    draw_genome(best)


if __name__ == '__main__':
    cores = 1
    generations = 3

    if len(sys.argv) > 1:
        out_root = sys.argv[1]
    else:
        out_root = os.getcwd()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = Config(config_path)

    # 此处初始化了各个房间的信息及相互之间的关系
    config.spec = spec
    pop = population.Population(config)

    if cores > 1:
        pe = ParallelEvaluator(cores, evaluate, draw=draw_genome)
        pop.run(pe.evaluate, generations)
        pe.pool.close()
    else:
        pop.run(evaluate_all, generations)

    out_dir = os.path.join(out_root, "out/school_{:%B_%d_%Y_%H-%M}".format(datetime.now()))
    assert not os.path.exists(out_dir)
    os.makedirs(out_dir)

    # 遗传完成并生成优胜者
    winner = pop.statistics.best_genome()
    pickle.dump(winner, open(os.path.join(out_dir,'winner_genome.p'), 'wb'))
    pickle.dump(pop, gzip.open(os.path.join(out_dir,'winner_school_population2.p.gz'), 'wb'))

    # 把graph翻译成平面图
    floorplan = FloorPlan.from_genome(winner)
    print('best fitness', winner.fitness)
    view.draw_floorplan(floorplan)
    view.save(os.path.join(out_dir, 'school_winner.png'))
    plot_stats(pop.statistics, filename=os.path.join(out_dir, 'avg_fitness.svg'))

    # todo mahaidong
    # plot_species(pop.statistics, filename=os.path.join(out_dir, 'speciation.svg'))
    with open(os.path.join(out_dir,'fitness.txt'), 'w') as fitness_file:
        fitness_file.write(str(winner.fitness))
    print('Number of evaluations: {0}'.format(pop.total_evaluations))
    view.hold()
