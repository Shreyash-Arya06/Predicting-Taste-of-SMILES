import pandas as pd

data = pd.read_csv('Datasets/Ignored-datasets/mergedtrain/ProcessedTrain.csv')

tasteless_data = []     # Will contain all tasteless compounds
bitter_data = []        # Will contain all bitter compounds
sweet_data = []         # Will contain all sweet compounds

for i, rows in data.iterrows():
    new_row = [rows[0], rows[1]]        # Taking the SMILES and C-SMILES

    if (rows[2] == rows[3]):            # Equal only for the case (0,0), i.e. tasteless
        tasteless_data.append(new_row)
    elif (rows[2] == 1):                # If Bitter row's cell has a value of one
        bitter_data.append(new_row)
    else:
        sweet_data.append(new_row)

column = ['SMILES', 'Canonical SMILES']
dft = pd.DataFrame(tasteless_data, columns = column)
dfb = pd.DataFrame(bitter_data, columns = column)
dfs = pd.DataFrame(sweet_data, columns = column)

dft.to_csv('Datasets/Ignored-datasets/train/Tasteless.csv', index = False)
dfb.to_csv('Datasets/Ignored-datasets/train/Bitter.csv', index = False)
dfs.to_csv('Datasets/Ignored-datasets/train/Sweet.csv', index = False)