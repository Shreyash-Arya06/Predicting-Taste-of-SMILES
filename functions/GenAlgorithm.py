import numpy as np
import random
import os
import fitnessFunc

class Chromosome:
    def __init__(self, limit = 1, size = 3, insert = None, delete = None, substitute = None):
        self.LIMIT = limit
        self.size = size

        if insert is None:
            insert = random.uniform(0, self.LIMIT)
        if delete is None:
            delete = random.uniform(0, self.LIMIT)
        if substitute is None:
            substitute = random.uniform(0, self.LIMIT)

        self.genes = np.array([insert, delete, substitute])     # Creating the chromosome
        self.fitness = 0.0      # Initializing the fitness of chromosome

class Genetic:
    def __init__(self, data_path, mutation_threshold = 0.025, parent_threshold = 0.75, mutation_factor = 0.15, size_of_group = 10, max_generation = 5):
        self.data_path = data_path
        self.mutation_threshold = mutation_threshold
        self.parent_threshold = parent_threshold
        self.mutation_factor = mutation_factor
        self.size_of_group = size_of_group
        self.max_generation = max_generation
        self.chromosomeList = []

    # Creating the population
    def initChromosome(self):
        for i in range(self.size_of_group):
            self.chromosomeList.append(Chromosome())
            self.evaluateChromosome(self.chromosomeList[-1])
        
    # Evaluating the fitness of each chromosome
    def evaluateChromosome(self, chromosome):
        chromosome.fitness = fitnessFunc.calculateFitness(self.data_path, chromosome.genes[0], chromosome.genes[1], chromosome.genes[2])
        
        result_path = 'Datasets/Ignored-datasets/scores/Weights.txt'
        if os.path.exists(result_path):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        file = open(result_path,append_write)
        file.write(f'cost: {np.round_(chromosome.genes, 4)}, fitness: {round(chromosome.fitness, 4)}\n')
        file.close()

    # Selecting a parent from the population
    def selectParent(self):
        p1 = random.randrange(self.size_of_group)
        p2 = random.randrange(self.size_of_group)

        while (p1 == p2):
            p2 = random.randrange(self.size_of_group)
        
        if (self.chromosomeList[p1].fitness < self.chromosomeList[p2].fitness):
            p1, p2 = p2, p1

        if (self.parent_threshold > random.random()):       # Probability of choosing more fitted chromosome is more
            return p1
        else:
            return p2
    
    # Mutating the offspring to maintain variation
    def mutate(self, chromosome):
        for gene in range(chromosome.size):
            if random.random() < self.mutation_threshold:       # Probability of mutation is less
                chromosome.genes[gene] += random.uniform(-1, 1) * self.mutation_factor
                chromosome.genes[gene] = max(chromosome.genes[gene], 0)
                chromosome.genes[gene] = min(chromosome.genes[gene], chromosome.LIMIT)
                # After mutation, value of gene must no be equal to zero or the limit

        return chromosome
    
    # Generating the offspring
    def crossOver(self, p1, p2):
        offspring = Chromosome()
        parent1, parent2 = self.chromosomeList[p1], self.chromosomeList[p2]

        offspring.genes = (parent1.genes + parent2.genes) / 2.0     # Offspring's genes is the average of parents' genes

        return offspring
    
    # Substituting the child with a the worst fitting member of the population
    def replace(self, offspring):
        unfit = 0
        unfit_fitness = self.chromosomeList[0].fitness

        for i in range(1, self.size_of_group):
            new_fitness = self.chromosomeList[i].fitness
            if (unfit_fitness > new_fitness):
                unfit = i
                unfit_fitness = new_fitness
            
        self.chromosomeList[unfit].genes = offspring.genes
        self.chromosomeList[unfit].fitness = offspring.fitness

    # Selecting the best fitted chromosome from the population
    def bestFit(self):
        best_fit = 0
        best_fitness = self.chromosomeList[best_fit].fitness

        for i in range(1, self.size_of_group):
            if (self.chromosomeList[i].fitness > best_fitness):
                best_fit = i
                best_fitness = self.chromosomeList[best_fit].fitness

        return best_fit
    
    # Printing chromosomes' fitness after each epoch
    def print_population_statistics(self, epoch):
        fSum, fMax = 0.0, -1e9

        for chromosome in self.chromosomeList:
            fSum += chromosome.fitness
            fMax = max(fMax, chromosome.fitness)

        print(
            f'{epoch}/{self.max_generation} Average fitness: {round(fSum / self.size_of_group, 4)}, max fitness: {round(fMax, 4)}')
    
    def run(self):
        self.initChromosome()
        epoch = 0
        while epoch < self.max_generation:
            p1 = self.selectParent()
            p2 = self.selectParent()
            if p1 == p2:                # Both parents must not be same
                continue

            offspring = self.crossOver(p1, p2)
            self.mutate(offspring)
            self.evaluateChromosome(offspring)
            self.replace(offspring)
            self.print_population_statistics(epoch)

            epoch += 1

        best_fit = self.bestFit()
        best_chromosome = self.chromosomeList[best_fit]
        print(f'Best fitness: {round(best_chromosome.fitness, 4)}, weights: {np.round_(best_chromosome.genes, 4)}')

        return best_chromosome
    