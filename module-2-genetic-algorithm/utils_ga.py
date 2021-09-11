

from random import gauss, random, uniform, sample, randrange
from pprint import pprint

FITNESS_SCORE = 0
PHENOME = 1
GENOME = 2


def sphere(shift, xs):
    x = sum([(x - shift)**2 for x in xs])
    return x


def to_print_dict(solution, is_binary=False):
    """
    This function creates a printable dictionary for a given solution.
    :param solution: list with fields for FITNESS_SCORE, PHENOME
    :return: child: returns the mutated child
    """
    solution_dict = {
        "fitness": round(solution[FITNESS_SCORE], 3),
        "f": round(sphere(0.5, solution[PHENOME]), 3),
        "solution": solution[PHENOME]
    }
    if is_binary:
        genotype = [int(x) for x in solution[GENOME]]
        solution_dict["genotype"] = genotype
    return solution_dict


def generate_random_population(N):
    random_population = []

    for _ in range(N):  # number of individuals in population
        individual = []
        for _ in range(10):  # each individual has 10 values
            individual.append(round(uniform(-5.11, 5.11), 2))
        random_population.append(individual)

    return random_population
