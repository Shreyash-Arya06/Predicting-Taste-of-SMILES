import pandas as pd
import os
from functions.WeightedEditDistanceAlgo import WeightedEditDistance

def evaluate(test_df, train_df, value):
    new_data = []

    for i, row1 in test_df.iterrows():
        score_dict = {}
        test_csmiles = row1[1]
        new_row = [test_csmiles, row1[2]]

        for j, row2 in train_df.iterrows():
            train_csmiles = row2[1]
            score = WeightedEditDistance(test_csmiles, train_csmiles).getScore()

            if (score != None):
                if (len(score_dict.keys()) != 0):
                    prev_smiles = list(score_dict.keys())[0]
                    if (prev_smiles < score):
                        del score_dict[prev_smiles]
                        score_dict[score] = {row2[value]}
                    elif (prev_smiles == score):
                        score_dict[prev_smiles].add(row2[value])
                else:
                    score_dict[score] = {row2[value]}
        
        val = list(score_dict.values())[0]
        if (len(list(score_dict.values())[0]) != 1):
            new_row.append(-1)
        else:
            new_row.append(list(score_dict.values())[0].pop())
            
        new_data.append(new_row)
        
    return new_data

train_df = pd.read_csv('Datasets/Ignored-datasets/mergedtrain/ProcessedTrain.csv')
column = ['C-SMILES', 'Real', 'Predicted']

bdf = pd.read_csv('Datasets/Ignored-datasets/test/Bitter.csv')
new_df = pd.DataFrame(evaluate(bdf, train_df, 2), columns=column)
new_df.to_csv('Datasets/Ignored-datasets/resultData/Bitter.csv')

sdf = pd.read_csv('Datasets/Ignored-datasets/test/Sweet.csv')
new_df = pd.DataFrame(evaluate(sdf, train_df, 3), columns=column)
new_df.to_csv('Datasets/Ignored-datasets/resultData/Sweet.csv')