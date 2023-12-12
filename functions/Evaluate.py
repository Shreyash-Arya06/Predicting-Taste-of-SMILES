import pandas as pd
from functions.WeightedEditDistanceAlgo import WeightedEditDistance

def evaluate(test_df, train_df):
    new_data = []

    for i, row1 in test_df.iterrows():
        score_dict = {}
        test_csmiles = row1[1]
        new_row = [test_csmiles]

        for j, row2 in train_df.iterrows():
            train_csmiles = row2[1]
            score = WeightedEditDistance(test_csmiles, train_csmiles)

            # calculate score and add to dictionary only if it is empty or the new score calculated is higher than the already stored
            # if the score is same as the already present key, append the taste value to the value set in the dictionary



        pass

    return new_data
