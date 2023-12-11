import pandas as pd
import os
from WeightedEditDistanceAlgo import WeightedEditDistance

def calculateFitness(ins_weight = 1, del_weight = 1, subs_weight = 1):
    path = '.\\processedDataset\\sepData'
    final_scores = []
    for files in os.listdir(path):
        df = pd.read_csv(os.path.join(path, files))
        CSmilesList = []
        for i, rows in df.iterrows():
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
                if (score != None):
                    row_total += score
                    count += 1
                row.append(score)

            row_score = row_total/count
            col_total += row_score
            row.append((row_score))
            new_data.append(row)
        
        column = ['CSMILES']
        column.extend(CSmilesList)
        column.append('Scores')
        final_row = ['' for i in range(len(CSmilesList) + 1)]
        col_score = col_total/len(CSmilesList)
        final_row.append(col_score)
        new_data.append(final_row)

        final_scores.append(col_score)

        rdf = pd.DataFrame(new_data, columns = column)
        result_path = os.path.join('resulted', files)
        print(result_path)
        rdf.to_csv(result_path, index = False)

    final_score = sum(final_scores) / len(final_scores)
    print(final_score)

    return final_score
