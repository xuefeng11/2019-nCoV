import pybel

from rdkit import Chem
import pandas as pd

df = pd.read_csv("smiles.pubchem.txt")

print(df.size)
df = pd.DataFrame(df)
print(df.shape)
youtube_ids=df["smile"]
youtube_ids2=list(dict.fromkeys(youtube_ids))
#print(youtube_ids2)
print(len(youtube_ids2))

data = {"unique_smile":youtube_ids2}
df_out = pd.DataFrame(data)
df_out.to_csv("pubchem_smile_unique.csv",index=False)

drug=df_out['unique_smile']

canonical_smiles=[]
name_arr=[]
counter=1


#ena_db_df = pd.read_csv("ena_can_unique.csv", sep=',',dtype={'canonical_smile':str,'name': str})
#ena_db_arr=ena_db_df['canonical_smile']
#df = pd.read_csv("ena_can_unique.csv", sep=',',dtype={'canonical_smile':str,'name': str})

for smile in drug:
    try:
        can=str(pybel.readstring("smi", smile).write("can")).rstrip()
 #       if can not in ena_db_arr:
        canonical_smiles.append(can)
        name_arr.append("PC-"+str(counter))
        counter=counter+1
    except:
        print("pubchem warning!:",smile)


data = { "canonical_smile":canonical_smiles,"name": name_arr}
df_out = pd.DataFrame(data)
df_out.to_csv("pubchem_canonical.csv", index=False)

