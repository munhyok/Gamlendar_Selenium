import pandas as pd

df = pd.read_csv('./dummy_csv.csv',encoding='utf-8', header=1)

#df.loc[0]

title = df['title']

for i in title:
    print(i)
    
    
for index, row in df.iterrows():
    print(row['autokwd'].split(','))
    
    
