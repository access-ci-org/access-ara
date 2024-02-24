import pandas as pd
import json
import os


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

directory_path = "./softwareInfoJSON"
data_dicts=[]

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        data = read_and_transform_json(file_path)
        if data is not None:
            data_dicts.append(data)

df = pd.DataFrame(data_dicts)
df.fillna('',inplace=True)

output_file_path = './combined_data.csv'
df.to_csv(output_file_path,index=False)

print(df)