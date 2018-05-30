import random
import operator


def initial_population(population_size, number_of_nodes):
    init = []
    # generates a population according to population size
    for x in range(population_size):
        # generates a random binary string according to number of nodes
        random_set = ""
        for i in range(number_of_nodes):
            random_set = str(random.randrange(0, 2)) + random_set

        init.append(random_set)

    return init


def read_file(file_name):

    try:
        f = open(file_name) # opens file
    except:
        return False, 0, 0, 0, 0

    line = f.readline()

    counter = 0
    numberOfNodes = 0
    numberOfEdges = 0
    weightList = []

    while line:
        line = line.replace(",", ".")  # convert all "," to "." in a line

        if counter == 0:    # first line = number of nodes
            numberOfNodes = int(line)
            edgeMatrix = [[0 for i in range(numberOfNodes)] for j in range(numberOfNodes)]
        elif counter == 1:  # second line = number of edges
            numberOfEdges = int(float(line))
        else:
            if counter < numberOfNodes + 2:     # next lines(number of numberOfNodes) = a weight value
                weightList.append(float(line.split(" ")[1]))    # creates weight list with weight values of nodes
            else:
                source = int(line.split(" ")[0])
                destination = int(line.split(" ")[1])
                edgeMatrix[source][destination] = 1     # crates adjacency matrix with source and destination nodes

        line = f.readline()
        counter += 1
    f.close()
    return True, numberOfNodes, numberOfEdges, weightList, edgeMatrix


def get_fitness(set, weightList):   # returns fitness value of a binary string

    counter = 0
    fitness = 0
    for i in set:
        if i == '1':
            fitness = fitness + float(weightList[counter])

        counter = counter + 1

    return fitness


def add_fitness(pop_set, weightList):  # creates a tuple for all strings in the population with type (string,fitness)
    new_set = []
    for i in pop_set:
        new_set.append((i, get_fitness(i, weightList)))

    return new_set


def add_prob(set):  # creates a tuple for all strings i the population with type (string,fitness,fitness probability)
    list = []
    prob_number = 0
    for i in set:
        prob_number = prob_number + i[1]

    for i in set:
        list.append((i[0], i[1], i[1]/prob_number))

    return list


def pool_selection(set, population_size):

    pool = []

    for i in range(population_size):
        random_number = random.random()     # generates random number between 0 and 1

        for x in set:   # for all strings
            # if generated random probability greater than current string's fitness probability,
            # then adds string to new pool
            if x[2] < random_number:
                pool.append(x)
                break

    # if there are missed strings,
    # these missed strings are set as string that is end of the pool(max index)
    if len(pool) % 100 != 0:
        for a in range(100 - len(pool) % 100):
            pool.append(pool[-1])

    return pool


def crossover(set, population_size, crossover_prob):

    crossover_list = []
    i = 0

    while i < population_size:  # for all pair strings in population
        rand_number = random.random()   # random number for deciding whether crossover operation is performed or not
        if rand_number < crossover_prob:    # if crossover will be performed
            crossover_point = random.randrange(1, len(set[i]))     # this random number decides division digit

            data1 = set[i][0]   # parent 1
            data2 = set[i+1][0]     # parent 2

            # first child ( first n digit of parent 1 and last 1000-n digit of parent 2)
            dna1 = data1[0:crossover_point] + data2[crossover_point:]
            # second child ( first n digit of parent 2 and last 1000-n digit of parent 1)
            dna2 = data2[0:crossover_point] + data1[crossover_point:]

            crossover_list.append(dna1)
            crossover_list.append(dna2)
        else:
            # if crossover will not be performed
            crossover_list.append(set[i][0])
            crossover_list.append(set[i+1][0])

        i = i + 2

    return crossover_list


def swap(char):     # returns flipped value of digit
    if char == '0':
        return '1'
    if char == '1':
        return '0'


def mutation(set, population_size, mut_prob):

    mutation_list = []

    for i in range(population_size):
        child = set[i]
        rand_number = random.random()   # random number for deciding whether mutation will be performed or not

        if rand_number < mut_prob:
            for k in range(10):     # for random 10 digit
                rand_digit = random.randrange(0, 999)
                child = child[:rand_digit] + swap(child[rand_digit]) + child[rand_digit+1:]  # flips a digit in string

        mutation_list.append(child)

    return mutation_list


def repair(population):
    index = 0
    global weightList
    for population_string in population:    # for all strings in population

        # checks whether string is feasible and returns a list with unfeasible pairs
        feasible, unfeasible_list = is_feasible(population_string)
        if not feasible:
            for i in range(0, len(unfeasible_list)): # for all unfeasible pairs
                # if both pair in string are '1', then choose low weighted one and make it '0'
                if population_string[unfeasible_list[i][0]] == "1" and population_string[unfeasible_list[i][1]] == "1":
                    if weightList[unfeasible_list[i][0]] < weightList[unfeasible_list[i][1]]:
                        counter = unfeasible_list[i][0]
                    else:
                        counter = unfeasible_list[i][1]
                    # makes '0' low weighted node
                    population_string = population_string[0:counter] + "0" + population_string[counter + 1:]

        population[index] = population_string
        index += 1

    return population


def is_feasible(population_string):

    global status, numberOfNodes, numberOfEdges, weightList, edgeMatrix
    unfeasible_list = []
    feasibility = True
    # i in range 0 and N - 1
    for i in range(0, len(population_string) - 1):  # for all digits except last one
        for j in range(i+1, len(population_string)): # from i th digit to last digit
            # if ith and jth digits are '1' and digits that refers to nodes have an edge between them,
            # then add pair to unfeasible list
            if population_string[i] == "1" and population_string[j] == "1" and \
                    (edgeMatrix[i][j] == 1 or edgeMatrix[j][i] == 1):
                unfeasible_list.append((i, j))
                feasibility = False

    return feasibility, unfeasible_list


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 6:
        print("WRONG INPUT FORMAT")
        sys.exit()

    name_of_graph = sys.argv[1]
    number_of_generation = sys.argv[2]
    population_size = sys.argv[3]
    cross_prob = sys.argv[4]
    mutation_prob = sys.argv[5]

    global weightList
    status, numberOfNodes, numberOfEdges, weightList, edgeMatrix = read_file(name_of_graph)

    if not status:
        print("File is not found")
        sys.exit()
    else:
        print("Number of nodes: ", numberOfNodes)
        print("Number of edges: ", numberOfEdges)

    initial_pop = initial_population(int(population_size), numberOfNodes)   # initialization of population
    repaired_pop = repair(initial_pop)      # first repair

    for i in range(int(number_of_generation)):

        pop_fitness = add_fitness(repaired_pop, weightList)  # adds fitness values of strings -> (string,fitness)

        pop_sorted = sorted(pop_fitness, key=operator.itemgetter(1), reverse=True)  # Sorts population descending order

        pop_prob = add_prob(pop_sorted)  # adds fitness probability values of strings -> (string,fitness,fitness prob)

        pool = pool_selection(pop_prob, int(population_size))  # creates new pool with pool selection

        cross = crossover(pool, int(population_size), float(cross_prob))    # makes crossover with given probability

        mut = mutation(cross, int(population_size), float(mutation_prob))   # makes mutation with given probability

        repaired_pop = repair(mut)      # repairs population after mutation



    # Finds max and avg fitness of population that is generated in last iteration
    max_weight = 0
    average_fitness = 0
    for i in repaired_pop:
        fitness = get_fitness(i, weightList)
        average_fitness += fitness
        if fitness > max_weight:
            max_weight = fitness

    average_fitness /= int(population_size)
    print(name_of_graph, "-Number of Generation: ", number_of_generation, "-Population Size: ", population_size,
          "-Cross Prob: ", cross_prob, "-Mutation Prob: ", mutation_prob, "Maximum Weight of SET : ", max_weight,
          "Average Weight of SET : ", average_fitness)

    file = open("results.txt", "a")  # opens for appending
    # file = open("results.txt", "w") # opens for writing

    file.write(str(name_of_graph) + " Number of Generation: " + str(number_of_generation) +
               " Population Size: " + str(population_size) + " Cross Prob: " + str(cross_prob) +
               " Mutation Prob: " + str(mutation_prob) + " Maximum Weight of SET : " + str(max_weight) +
               " Average Weight : " + str(average_fitness))
    file.write("\n\n")
    file.close()
