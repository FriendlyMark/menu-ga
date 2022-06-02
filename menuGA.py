from menuFuncs import *
from data import name
from data import kcal
from parameters import *

# generate the initial population
population = [Menu(name, kcal, daily_kcal) for i in range(npop)]

for i in population: 
    i.set_genes() # randomly switch genes on
    i.set_cost() # absolute distance from daily_calories

## MAIN LOOP
gens = 0 # tells me how many generations I went through
solution = population[0] # any old solution to begin with

for i in range(ngens): # replace with a while loop
    gens += 1
    # check for perfect/tolerable solution
    if solution.get_cost() <= daily_kcal * tolerance:
        break
    # update the best solution
    for obj in population:
        if obj.get_cost() > solution.get_cost():
            solution = obj
    # select mating pairs from population without replacement
    crossover_pairs = generate_mating_pairs(population)
    offspring = []
    for pair in crossover_pairs:
        # produce children through crossover
        children = one_point_crossover(pair)
        # mutate children
        children = mutate(children)
        # append to list of children
        offspring.extend(children)

    # calculate cost for these offspring
    [obj.set_cost() for obj in offspring]

    # merge children and cull population
    population = population_merge(population, offspring, npop)

# output
print(f'####### best solution #######')
print(f'achieved at: {gens}')
print(f'cost: {solution.get_cost()}')