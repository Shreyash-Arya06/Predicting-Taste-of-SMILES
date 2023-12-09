import pandas as pd

def preprocess(data, final_data):
    number = 0
    for lines in data:
        row = lines.split("\t")
        if not number:      # To skip the first row
            number += 1
        else:
            data_row = []
            if len(row) == 7:
                data_row.append(row[3])     # Adding SMILES
                data_row.append(row[4])     # Adding Canonical SMILES
                if row[6] == 'True':
                    data_row.append(1)
                else:
                    data_row.append(0)

                final_data.append(data_row)
    
    return final_data

with open("Datasets/testset/bitter-test.tsv") as fb, open("Datasets/testset/sweet-test.tsv") as fs:
    datab = fb.read()
    datas = fs.read()
    datab.strip()
    datas.strip()
    datab = datab.split("\n")
    datas = datas.split("\n")

bitter_data = []
sweet_data = []
bitter_data = preprocess(datab, bitter_data)
sweet_data = preprocess(datas, sweet_data)

# Converting list to dataframes
dfb = pd.DataFrame(bitter_data, columns=['SMILES', 'Canonical SMILES', 'Bitter'])
dfs = pd.DataFrame(sweet_data, columns=['SMILES', 'Canonical SMILES', 'Sweet'])

# Droping duplicates
dfb.drop_duplicates(subset=['Canonical SMILES'], inplace=True)
dfs.drop_duplicates(subset=['Canonical SMILES'], inplace=True)

# Converting to csv file
dfb.to_csv('Datasets/Ignored-datasets/test/Bitter.csv', index=False)
dfs.to_csv('Datasets/Ignored-datasets/test/Sweet.csv', index=False)