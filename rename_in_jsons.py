import os
import json

def rename_quarters_in_json(folder_path):
    json_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".json")], key=lambda x: int(x.split('.')[0]))
    
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Renaming quarters with increasing year every 4 quarters
        for i, entry in enumerate(data, start=1):
            year = 2022 + (i - 1) // 4
            quarter = (i - 1) % 4 + 1
            entry["Quarter"] = f"Q{quarter}-{year}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f"Updated {json_file}")

folder_path = "json"  # Update with the actual path
rename_quarters_in_json(folder_path)