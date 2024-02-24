import json
import random
import os

def update_json_value():
    # Construct the path to data.json relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(base_dir, 'public', 'data', 'data.json')

    # Read the existing data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Update the 'value' field with a random float rounded to 2 decimal places
    data['value'] = str(round(random.uniform(100, 999), 2))

    # Write the modified data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    update_json_value()
