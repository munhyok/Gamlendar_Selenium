import json
import os

  # 파일이 존재하는지 확인

def load_json(filename):
    with open(filename, 'r') as file:
        index_ = json.load(file)
    print(index_['index'])



def save_json(index, filename):
    with open(filename, 'r+') as file:
        data = json.load(file)
        data["index"] = index

        
    json_file = open(filename, 'w', encoding='utf-8')
    json.dump(data, json_file)
    json_file.close()
     
        

#load_json('./test/db_index.json')

save_json(0, './test/db_index.json')

#load_json('./test/db_index.json')