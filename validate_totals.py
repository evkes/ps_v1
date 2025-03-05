import json

with open("company_a.json") as f:
    data = json.load(f)


def validate_totals(data):
    for entry in data:
        quarter = entry["Quarter"]
        total_countries = sum(entry["Countries"].values())
        total_occupations = sum(entry["Occupations"].values())
        
        print(f"{quarter}: Countries Total = {total_countries}, Occupations Total = {total_occupations}")
        
        if total_countries != total_occupations:
            print(f"Mismatch detected in {quarter}!")

validate_totals(data)
