import os
import pandas as pd
import numpy as np
import pybel


path="/vol/ml/candle_aesp/databases/ZINC15"
smile_arr=list()
id_arr = list()
for folder in os.listdir(path):
    folder_path=path+"/"+folder
    if not os.path.isdir(folder_path):
       continue
    for file in os.listdir(folder_path):
        file_path=folder_path+"/"+file
        if file.endswith(".smi"):
            #print(file_path)
            smile=[]
            id=[]
            try:
                df = pd.read_csv(file_path, sep=' ', dtype={'smiles': str, 'zinc_id': str})
             #   print(df["smiles"].values)
                smile_arr=smile_arr+df["smiles"].tolist()
                id_arr=id_arr+df["zinc_id"].tolist()
            except:
                try:
                    df = pd.read_csv(file_path, sep=' ', dtype={'#smiles': str, 'zinc_id': str})
                    smile_arr = smile_arr + df["#smiles"].tolist()
                    id_arr = id_arr + df["zinc_id"].tolist()
                except:
                    print("warning!!:",file_path)
        else:
            continue

data = { "smile":smile_arr,"name": id_arr}
df_out = pd.DataFrame(data)
df_out=df_out.drop_duplicates("smile")
df_out.to_csv("ZINC_UNIQUE_SMILE.csv", index=False)

drug=df_out["smile"]

canonical_smiles = [pybel.readstring("smi", smile).write("can").rstrip() for smile in drug]

data = {"canonical_smile":canonical_smiles,"name": df_out['name']}
df_out = pd.DataFrame(data)
df_out=df_out.drop_duplicates("canonical_smile")
df_out.to_csv("ZINC_UNIQUE_canonical.csv", index=False)
