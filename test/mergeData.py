import pandas as pd
import time
from datetime import datetime



# 두 CSV 파일에서 데이터를 읽어옵니다.
df1 = pd.read_csv('file1.csv')
df2 = pd.read_csv('file2.csv')

# 두 데이터프레임을 병합합니다.
merged_df = pd.concat([df1, df2])

# title을 기준으로 그룹화하여 중복된 데이터를 하나로 합치고, platform은 리스트로 변환합니다.
merged_df = merged_df.groupby('title').agg({
    'url': 'first',
    'date': 'first',
    'imageurl': 'first',
    'platform': lambda x: list(set(x))
}).reset_index()

# 병합된 결과를 출력합니다.
print(merged_df)
