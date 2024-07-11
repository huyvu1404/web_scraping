import os
import json
import pandas as pd

def save_data_to_file(path, file_name, file):
    try:    
        with open(f'{path}/{file_name}.json', 'w', encoding='utf-8') as json_file:
            json.dump(file, json_file, ensure_ascii=False, indent=4)
        
        product_details_df = pd.DataFrame(file)
        product_details_df.to_csv(f'{path}/{file_name}.csv', index=False)
        
    except Exception as e:
        print("Error occured:", e)