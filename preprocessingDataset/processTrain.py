import pandas as pd

def preprocess(data, final_data, condition):
    # condition - to choose the desired value for both columns
    
    number = 0
    for lines in data:
        row = lines.split("\t")
        if not number:      # To skip the first row
            number += 1
        else:
            data_row = []
            if len(row) == 6:
                data_row.append(row[3])     # Adding The SMILES
                data_row.append(row[4])     # Adding the Canonical SMILES
                if row[1] == "Tasteless":
                    data_row.append(0)
                    data_row.append(0)
                elif row[5] == condition:
                    data_row.append(1)
                    data_row.append(0)
                else:
                    data_row.append(0)
                    data_row.append(1)

                final_data.append(data_row)     # Appending each row to the final data
    
    return final_data

with open("Datasets/trainset/bitter-train.tsv") as fb, open("Datasets/trainset/sweet-train.tsv") as fs:
    datab = fb.read()
    datas = fs.read()
    datab.strip()
    datas.strip()
    datab = datab.split("\n")
    datas = datas.split("\n")

new_data = []
new_data = preprocess(datab, new_data, 'True')
new_data = preprocess(datas, new_data, 'False')


df = pd.DataFrame(new_data, columns=['SMILES', 'Canonical SMILES', 'Bitter', 'Sweet'])
df.drop_duplicates(subset=['Canonical SMILES'], inplace=True)
df.to_csv('Datasets/mergedtest/ProcessedTrain.csv', index=False)