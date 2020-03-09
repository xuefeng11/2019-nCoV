from rdkit import Chem
from mordred import Calculator, descriptors
import pandas as pd

'''
df = pd.read_csv("ena+db.can", sep='\t',dtype={'canonical_smile':str,'name': str})
print(df.shape)

df2=df.drop_duplicates("canonical_smile")
df2.to_csv("ena_can_unique.csv",index=False)
print(df2.shape)

df3 = df[df.duplicated("canonical_smile")]
df3.to_csv("ena_can_duplicated.csv",index=False)
print(df3.shape)

df4 = df[df.duplicated(['canonical_smile', 'name'])]
df4.to_csv("ena_can_name_duplicated.csv",index=False)
print(df4.shape)
'''

df = pd.read_csv("ena_can_unique.csv", sep=',',dtype={'canonical_smile':str,'name': str})
#df = pd.read_csv("ena_can_unique.csv", sep=',',dtype={'canonical_smile':str,'name': str})
print(df.shape)

calc = Calculator(descriptors, ignore_3D=False)

descriptor_arr=[]
can_arr=[]
name_arr=[]
counter=0

for index  in df.index:
    try:
        can = df['canonical_smile'][index]
        name = df['name'][index]
        mol = Chem.MolFromSmiles(can)
        descriptor = calc(mol)
        descriptor.fill_missing("nan")
        can_arr.append(can)
        name_arr.append(name)
        descriptor_arr.append(descriptor)
        counter=counter+1
        if counter%1000==0:
           print("processed records No:",counter)
    except:
        print("warning!:",index)

ena_df=pd.DataFrame.from_dict(descriptor_arr, orient='columns')

print(ena_df.shape)
data_source_arr=["enamine&drugbank"] * len(can_arr)

ena_df["canonical_smile"]=can_arr
ena_df["name"]=name_arr
ena_df["data_source"]=data_source_arr

cols=ena_df.columns.tolist()
cols = cols[-3:] + cols[:-3]
ena_df=ena_df[cols]
ena_df.to_csv("unique_ena_descriptor.csv",index=False)
