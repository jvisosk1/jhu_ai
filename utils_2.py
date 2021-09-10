
from random import gauss, random, uniform, sample, randrange
from main_2 import *

FITNESS_SCORE = 0
PHENOME = 1
GENOME = 2

params = {
    "f": lambda xs: sphere(0.5, xs),
    "minimization": True,
    "mutation_rate": 0.05,
    "crossover_rate": 0.9,
    "population_size": 200,  # should be ~200
    "generations": 300,  # should be ~300
    "gene_index": 4
}

params2 = {
    "f": lambda xs: sphere(0.5, xs),
    "minimization": True,
    "mutation_rate": 0.05,
    "crossover_rate": 0.9,
    "population_size": 200,  # should be ~200
    "generations": 200,  # should be ~300
    "gene_index": 70
}


def sphere(shift, xs):
    try:
        x = sum([(x - shift)**2 for x in xs])
        return x
    except:
        print('here is xs:', xs)


def mutate_real_ga(child):
    x = gauss(0, 0.8)
    random_index = randrange(0,10)

    if child[random_index] + x < 5.12:
        child[random_index] =  round(child[random_index] + x, 2)
    else: child[random_index] =  round(child[random_index] - x, 2)

    return child


def mutate_binary_ga(child):
    idx = randrange(0,100)
    # print(idx)
    if child[idx] == '1':
        child[idx] = '0'
    else: child[idx] = '1'

    return child


def reproduce(parent1, parent2, params):
    gene_index = params["gene_index"]
    if params["crossover_rate"] < random():
        return parent1[PHENOME], parent2[PHENOME]

    # perform crossover functions and mutate children
    child1 = parent1[PHENOME][:gene_index] + parent2[PHENOME][gene_index:]
    if params["mutation_rate"] < random():
        child1 = mutate_real_ga(child1)

    child2 = parent2[PHENOME][:gene_index] + parent1[PHENOME][gene_index:]
    if params["mutation_rate"] < random():
        child2 = mutate_real_ga(child2)

    return child1, child2


def reproduce_binary(parent1, parent2, params):
    gene_index = params["gene_index"]
    if params["crossover_rate"] < random():
        return parent1[PHENOME], parent2[PHENOME]



    # perform crossover functions and mutate children

    child1 = parent1[GENOME][:gene_index] + parent2[GENOME][gene_index:]
    # print('child1 before:', decode("".join(child1)))
    if params["mutation_rate"] < random():
        child1 = mutate_binary_ga(child1)
        # print('child1 after: ', decode("".join(child1)))

    child2 = parent2[GENOME][:gene_index] + parent1[GENOME][gene_index:]
    if params["mutation_rate"] < random():
        child2 = mutate_binary_ga(child2)

    # print('PARENT1:', "".join(parent1[GENOME]))
    # print('PARENT2:', "".join(parent2[GENOME]))
    # print('CHILD2: ', "".join(child2))

    # print('CHILD2:', decode("".join(child2)))
    # print('PARENT2:', parent2[PHENOME])

    return decode("".join(child1)), decode("".join(child2))


def to_print_dict(solution):
    solution_dict = {
        "fitness": round(solution[FITNESS_SCORE], 3),
        "f": round(sphere(0.5, solution[PHENOME]), 3),
        "solution": solution[PHENOME]
    }
    return solution_dict


def generate_random_population(N):
    random_population = []

    for i in range(N):
        individual = []
        for j in range(10):
            individual.append(round(uniform(-5.11, 5.11), 2))
        random_population.append(individual)

    return random_population
