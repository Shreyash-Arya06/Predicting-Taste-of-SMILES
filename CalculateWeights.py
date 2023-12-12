from functions.GenAlgorithm import *

def main():
    path = 'Datasets/Ignored-datasets/train'

    Genetic_Algo = Genetic(path)
    best_chromosome = Chromosome()

    best_chromosome = Genetic_Algo.run()

main()