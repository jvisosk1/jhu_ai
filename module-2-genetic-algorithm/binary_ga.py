
from utils_ga import *

params_binary_ga = {
    "f": lambda xs: sphere(0.5, xs),
    "minimization": True,
    "mutation_rate": 0.05,
    "crossover_rate": 0.9,
    "population_size": 200,
    "generations": 200,
    "gene_index": 70
}

encode_dict = {}
decode_dict = {}


def encode(phenome):
    """
    This function encodes all elements within a phenome list. The input parameter will be a list of 10 phenome values
    [3.12, 1.98, -0.23, ...] and will return a list of 100 bits ['1','0','0'...] where each ten bits represents an
    element within the phenome. The encoding is performed using a predetermined binary value stored in 'encode_dict'.

    :param phenome: list containing 10 phenome values [3.12, 1.98, -0.23, ...]
    :return: genome: list of 100 bits ['1','0','0'...]
    """
    encoded_genome = ''

    # for each element use the encode_dict to convert from 3.12 to 0010100010 format
    for x_i in phenome:
        if str(x_i) == '0.0' or str(x_i) == '0':
            encoded_genome += encode_dict['-0.0']  # value in encode_dict is '-0.0'
        elif str(x_i) == '1':
            encoded_genome += encode_dict['1.0']  # value in encode_dict is '1.0'
        else: encoded_genome += encode_dict[str(x_i)]

    # convert to list where each bit is distinct element
    return list(encoded_genome)


def decode(encoded_genome):
    """
    This function decodes all elements within an encoded genome. The input parameter will be a list of 100 bits
    ['1','0','0'...] and will return a list of 10 phenome elements [3.12, 1.98, -0.23, ...]
    The decoding is performed using a predetermined decimal value per binary string which is stored in 'decode_dict'.

    If the 10 bit string is not found in the decode dictionary (this occurs due to lack of bounds when the mutation
    function is applied) we will generate a random float value between (-5.12, 5.12). Additionally, due to an unknown
    tendency of the algorithm to get stuck on the specific value -0.01, we also generate a random value if the
    decoded phenome value is -0.01.

    :param encoded_genome: list of 100 bits ['1','0','0'...]
    :return: phenome_list: list of phenome elements after being decoded [3.12, 1.98, -0.23, ...]
    """
    phenome_list = []
    # in each encoded genome there are 10 elements of 10 bits each
    for idx in range(0,100,10):
        binary_num = encoded_genome[idx:idx + 10]
        # if mutation has generated binary value not convertible to (-5.12, 5.12) then create random value
        if binary_num not in decode_dict or decode_dict[binary_num] == -0.01:
            dec_value = round(uniform(-5.11, 5.11), 2)
        else: dec_value = decode_dict[binary_num]

        phenome_list.append(dec_value)

    return phenome_list


def generate_encode_decode_dicts():
    """
    This function generates two dictionaries for quick access of encoded/decoded values to quickly convert from
    Phenome to Genome values for an element. The dictionaries are stored as globally accessible variables.
    The dictionaries will contain the binary values for each 2 decimal float value from (-5.12, 5.12) non inclusive.
    :param:
    :return: child: returns the mutated child
    """
    num = -5.11
    for i in range(1023):

        decimal_num = round(num, 2)  # ex. 4.23
        int_format = int(decimal_num * 100 + 512)  # ex. 423 + 512 = 935
        binary_num = format(int_format, "010b")  # ex. 1110100111

        encode_dict[str(decimal_num)] = binary_num
        decode_dict[str(binary_num)] = decimal_num

        num += 0.01
    return


def reproduce_binary_ga(parent1, parent2, params):
    """
    This function is the binary reproduction function of the Genetic Algorithm. It takes 2 parents and applies a
    crossover function to swap sections of each parent element to create 2 children and then potentially mutates them.
    The mutation is a simple flip of a single bit within the encoded child string (the Genome value).
    Crossover and mutation functions are conditional on the crossover and mutation rates passed in as parameters.

    :param parent1: 2 parents will reproduce 2 children or be returned themselves
    each parent has fields: parent[GENOME] ex: , ['1','0','1','1'...], parent[PHENOME] ex: [0.53, 0.48...] and
    parent[FITNESS]
    :param parent2: same as above
    :param params: specific binary ga macro parameters including gene_index, # of gens, population size, etc
    :return: child1, child2: children will be returned after possible mutation, otherwise parents returned
    """
    gene_index = params["gene_index"]
    if params["crossover_rate"] < random():
        return parent1[PHENOME], parent2[PHENOME]

    # perform crossover functions for children
    child1 = parent1[GENOME][:gene_index] + parent2[GENOME][gene_index:]
    child2 = parent2[GENOME][:gene_index] + parent1[GENOME][gene_index:]

    # mutate the children if mutation rate less than random
    if params["mutation_rate"] < random():
        idx1, idx2 = randrange(0, 100), randrange(0, 100)
        child1[idx1] = '0' if child1[idx1] == '1' else '1'
        child2[idx2] = '0' if child2[idx2] == '1' else '1'

    # decode the children genome values before returning them
    child1 = decode("".join(child1))
    child2 = decode("".join(child2))

    return child1, child2


def binary_ga(parameters, debug=False):
    """
    This function is the main function of the Genetic Algorithm using binary values. The function initially generates a
    random population where each element consists of 10 Phenome values. Then for each generation, the function
    evaluates the population assigning a fitness score and also encodes the Phenome value for each element which will
    be used in the reproduce function.

    In each generation the population reproduces a subsequent generation is generated by executing crossover and
    mutation functions on the parent elements.

    Best fitting element is calculated for each generation and also the best overall element.
    Debug option will print the best solution for 20 generations throughout the algorithm execution.

    :param params: child is represented by a list of 10 phenome values (3.12, 1.98, -0.23, etc)
    :return: child: returns the mutated child
    """
    N = parameters["generations"]
    population = generate_random_population(N)
    best_fit = (0, [])

    for gen in range(N):
        next_gen = []
        # evaluate the population, append fitness score
        evaluated_population = [(1 - sphere(0.5, x), x, encode(x)) for x in population]
        best_fit_this_gen = sorted(evaluated_population, reverse=True)[0]

        if debug and gen % int(N / 20) == 0:
            print(f'Gen {gen}:', to_print_dict(best_fit_this_gen, True))

        for _ in range(int(parameters["population_size"] / 2)):
            # pick 2 fittest elements from random sample of 7 from population
            parent1, parent2 = sorted(sample(evaluated_population, 7), reverse=True)[:2]
            # reproduce for children
            child1, child2 = reproduce_binary_ga(parent1, parent2, parameters)
            # add children to next gen
            next_gen.extend([child1, child2])

        if best_fit[FITNESS_SCORE] < best_fit_this_gen[FITNESS_SCORE]:
            best_fit = best_fit_this_gen
        population = next_gen
    return to_print_dict(best_fit, True)


if __name__ == '__main__':

    generate_encode_decode_dicts()
    print('########################\nBINARY GENETIC ALGORITHM\n########################')
    binary_ga(params_binary_ga, True)
    # solution = binary_ga(params_binary_ga)
    # print(solution)
