import pandas as pd
import json
import os


directory_path = "./softwareInfoJSON"

def read_and_transform_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # convert the lists into a comma separated string
        for key,value in data.items():
            if isinstance(value,list):
                data[key] = ', '.join(value)
        return data
    except json.JSONDecodeError:
        print(f"Skipping file due to JSONDecodeError: {file_path}")
        return None

data_dicts = [read_and_transform_json(os.path.join(directory_path,f)) 
              for f in os.listdir(directory_path) if f.endswith('.json')]

df = pd.DataFrame(data_dicts)

print(df)