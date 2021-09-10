
from utils_2 import *


def encode(phenome):
    encoded_genome = ''
    for x_i in phenome:
        int_format = int(x_i * 100 + 512)
        binary_format = format(int_format, "010b")
        encoded_genome += binary_format
    return list(encoded_genome)


def decode(encoded_genome):
    split_genomes = []
    for idx in range(0,100,10):
        dec_value = ( int(encoded_genome[idx:idx + 10], 2) - 512) / 100
        split_genomes.append(dec_value)

    return split_genomes


def real_ga(parameters, debug=False):
    N = parameters["generations"]
    population = generate_random_population(N)
    best_fit = (0, [])

    for gen in range(N):
        next_gen = []
        # evaluate the population, append fitness score
        evaluated_population = [( 1 - sphere(0.5, x), x) for x in population]
        best_fit_this_gen = sorted(evaluated_population, reverse=True)[0]

        if debug and gen % int(N / 20) == 0:
            print(f'Gen {gen}:', to_print_dict(best_fit_this_gen))

        for _ in range(int(parameters["population_size"]/2)):
            # pick 2 fittest elements from random sample of 7 from population
            parent1, parent2 = sorted(sample(evaluated_population, 7), reverse=True)[:2]

            # reproduce for children
            child1, child2 = reproduce(parent1, parent2, parameters)

            # add children to next gen
            next_gen.extend([child1, child2])

        if best_fit[FITNESS_SCORE] < best_fit_this_gen[FITNESS_SCORE]:
            best_fit = best_fit_this_gen

        population = next_gen

    return to_print_dict(best_fit)


def binary_ga(parameters, debug):
    N = parameters["generations"]
    population = generate_random_population(N)
    best_fit = (0, [])

    for gen in range(N):
        next_gen = []

        # evaluate the population, append fitness score
        evaluated_population = [(1 - sphere(0.5, x), x, encode(x)) for x in population]

        best_fit_this_gen = sorted(evaluated_population, reverse=True)[0]
        # print(round(best_fit_this_gen[FITNESS_SCORE],3), best_fit_this_gen[PHENOME])

        if debug and gen % int(N / 20) == 0:
            print(f'Gen {gen}:', to_print_dict(best_fit_this_gen))
            for i in population[::50]:
                print(i)

        for _ in range(int(parameters["population_size"] / 2)):
            # pick 2 fittest elements from random sample of 7 from population
            parent1, parent2 = sorted(sample(evaluated_population, 7), reverse=True)[:2]

            # reproduce for children
            child1, child2 = reproduce_binary(parent1, parent2, parameters)
            # print(child1)

            # add children to next gen
            next_gen.extend([child1, child2])

        if best_fit[FITNESS_SCORE] < best_fit_this_gen[FITNESS_SCORE]:
            best_fit = best_fit_this_gen

        # print(best_fit[FITNESS_SCORE], best_fit[PHENOME])

        population = next_gen
        # break

    return to_print_dict(best_fit)


if __name__ == '__main__':

    # xs = [1.0, 2.0, -3.4, 5.0, -1.2, 3.23, 2.87, -4.23, 3.82, -4.61]
    # encoded = encode(xs)
    # print(encoded)
    # print("".join(encoded))
    # decode("".join(encoded))
    # print(f'original element: {xs}')
    # new_xs = mutate_real_ga(xs)
    # print(f'mutated element:  {new_xs}')

    print('Final:', binary_ga(params2, True))

