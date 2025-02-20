import pandas as pd

def csvSearch(game_title):
        
    df = pd.read_csv('dummy_csv.csv')
    contains = df[df['autokwd'].str.contains(fr'(^|,\s*){game_title}($|,\s*)', case=False, na=False, regex=True)]
    print(contains)
        
        
        
