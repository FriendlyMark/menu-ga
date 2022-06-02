import random
import operator
from data import name
from data import kcal
from parameters import *

# object definition
class Menu:
    def __init__(self, name, kcal, daily_kcal):
        self.name = name
        self.kcal = kcal
        self.gene = [0 for _ in name]
        self.rand = [random.randint(0, 100) for _ in name]
        self.cost = 1e6 # just something big
        self.daily_kcal = daily_kcal
    def set_genes(self):
        '''
        uses random draw to activate genes
        modifies self.gene in place
        '''
        for ind in range(len(self.rand)):
            if self.rand[ind] >= 50:
                self.gene[ind] = 1
    def overwrite_genes(self, new_gene):
        '''
        crossover and mutation results are passed here as a list

        why does this give me a None???
        '''
        self.gene = new_gene
    def get_name(self):
        return self.name
    def get_kcal(self):
        return self.kcal
    def get_genes(self):
        return self.gene
    def get_rand(self):
        return self.rand
    def get_cost(self):
        return self.cost
    def set_cost(self):
        '''
        calculates cost as absolute distance from self.daily calories
        '''
        x = 0
        for ind in range(len(self.gene)):
            if self.gene[ind] == 1:
                x += self.kcal[ind]
        self.cost = abs(self.daily_kcal - x)


# roulette wheel selection
def weighted_random_choice(population):
    '''
    takes the population of solutions as a list
    uses roulette wheel selection to pick an individual with probability proportional to cost
    '''
    choices = {obj: obj.get_cost() for obj in population}
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key

def generate_mating_pairs(population):
    '''
    takes the population of solutions as a list
    uses weighted_random_choice() to choose a pair of parents
    passes over the population until all parents have been removed
    returns a list of tuples [(parent1, parent2), (parent1, parent2),...]
    '''
    # copy population
    cpop = population.copy()
    mating_pairs = []

    for i in range(len(cpop)//2):
        if len(cpop) == 2:
            p1 = cpop[0]
            p2 = cpop[1]
            pair = (p1, p2)
            mating_pairs.append(pair)
        # more than two parents
        else:
            p1 = weighted_random_choice(cpop)
            cpop.remove(p1)
            p2 = weighted_random_choice(cpop)
            cpop.remove(p2)
            pair = (p1, p2)
            mating_pairs.append(pair)
    return mating_pairs

# single point crossover
def one_point_crossover(tuple):
    '''
    takes a tuple ontaining two parent objects
    performs genetic crossover
    outputs a tuple containing two children objects
    '''
    ceil = len(tuple[0].get_genes())
    #name = tuple[0].get_name
    #kcal = tuple[0].get_kcal
    ind = random.randint(1,ceil) # index location to swap

    g1,g2 = tuple[0].get_genes().copy(), tuple[1].get_genes().copy() # gene of each parent

    # crossing over
    for i in range(ind, ceil):
        g1[i], g2[i] = g2[i], g1[i]
    
    # initialising children
    c1 = Menu(name, kcal, daily_kcal)
    c2 = Menu(name, kcal, daily_kcal)

    c1.gene = g1
    c2.gene = g2

    return(c1,c2)

# mutation
def mutate(tuple, mutation_percent = 50):
    '''
    for each allele in the genome a number generator 1-100 is set off
    if the number is greater than the mutation chance nothing happens
    if the number is <= mutation chance the allele is inverted 1 <- 0 & 0 <- 1
    function modifies the genes of the object

    I NEED TO BE SURE THAT THIS WORKS. IF I SET MUTATION CHANCE TO 0.25 DOES IT CORRECTLY MUTATE ~25% OF GENES?
    '''
    for obj in tuple:
        g = obj.get_genes().copy()
        for idx in range(len(g)):
            r = random.randint(0,100)
            if r <= mutation_percent:
                g[idx] ^= 1 # bitwise XOR exchanges
        obj.overwrite_genes(g)
    return tuple

# population merge
def population_merge(population, children, npop = 10):
    '''
    children and population will both be lists of objects

    children are merged into population, all individuals are ranked by their cost

    fittest individuals within the population limit remain
    '''
    population.extend(children)
    merged = sorted(population, key = operator.attrgetter('cost'))
    return merged[:npop]