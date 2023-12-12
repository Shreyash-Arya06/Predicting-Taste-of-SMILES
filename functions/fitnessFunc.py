import pandas as pd
import os
from WeightedEditDistanceAlgo import WeightedEditDistance

def calculateFitness(path, ins_weight = 1, del_weight = 1, subs_weight = 1):

    final_scores = []
    for files in os.listdir(path):
        df = pd.read_csv(os.path.join(path, files))
        CSmilesList = []

        for i, rows in df.iterrows():       # Getting the list of all the C-SMILES
            CSmilesList.append(rows[1])
        
        new_data = []
        col_total = 0
        for CSmiles in CSmilesList:
            row = [CSmiles]
            row_total = 0
            count = 0
            for other_smiles in CSmilesList:
                similarity_score = WeightedEditDistance(CSmiles, other_smiles, ins_weight, del_weight, subs_weight)
                score = similarity_score.getScore()
                if (score != None):     # Accounting only those cells with not None value
                    row_total += score
                    count += 1
                row.append(score)

            row_score = row_total/count
            col_total += row_score
            row.append((row_score))
            new_data.append(row)
        
        column = ['CSMILES']
        column.extend(CSmilesList)
        column.append('Scores')     # Completeing the column heading row

        final_row = ['' for i in range(len(CSmilesList) + 1)]
        overall_score = col_total/len(CSmilesList)
        final_row.append(overall_score)
        new_data.append(final_row)

        final_scores.append(overall_score)

    final_score = sum(final_scores)/len(final_scores)
    print(final_score)

    return final_score

'''
Idea here is that while considering the three separated dataset, one at a time, and calculate total fitness from the overall fitness of each sheets.
1. First I have calculated the similarity score for each C-SMILES with every C-SMILES.
2. Then the average score for each C-SMILES (column) is obtained. Note: While calculating the average I have taken only cells having values in it as the ones with None value does not contribute to the similarity score.
3. the overall score is calculated by taking the average of scores of each C- SMILES, i.e. row.
4. Finally the average of all the three sheets is returned.
'''