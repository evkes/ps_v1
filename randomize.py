import random
import json

def clone_previous_quarter(data):
    """
    Clones the previous quarter and adds a random number of employees to categories and countries.
    Employee growth is linear before a capital raise and quadratic afterward.
    Capital is only added once every 4-7 quarters.
    Prioritizes growth in the USA, India, Sales, and Software Engineering.
    """
    num_quarters = len(data)
    capital_increase_intervals = sorted(random.sample(range(4, 8), k=num_quarters // 6))
    capital_raised = False
    
    for i in range(1, num_quarters):
        previous_entry = json.loads(json.dumps(data[i - 1]))  # Deep copy to avoid overwriting previous entries
        
        # Determine if this quarter should have a capital increase
        if i in capital_increase_intervals:
            previous_entry['Capital'] += round(random.uniform(2.0, 5.0), 2)
            capital_raised = True
        else:
            capital_raised = False
        
        # Linear growth before capital raise, quadratic growth after
        if not capital_raised:
            new_hires = random.randint(1, 3)  # Linear growth
        else:
            new_hires = random.randint(3, 7) ** 2 // 10  # Quadratic growth with scaling
        
        # Expand employees in prioritized countries and occupations
        country_keys = list(previous_entry['Countries'].keys())
        occupation_keys = list(previous_entry['Occupations'].keys())
        
        country_weights = [0.5 if c in ['USA', 'India'] else 0.2 for c in country_keys]
        occupation_weights = [0.5 if o in ['Sales', 'Software Engineering'] else 0.2 for o in occupation_keys]
        
        for _ in range(new_hires):
            selected_country = random.choices(country_keys, weights=country_weights)[0]
            previous_entry['Countries'][selected_country] += 1
        
        for _ in range(new_hires):
            selected_occupation = random.choices(occupation_keys, weights=occupation_weights)[0]
            previous_entry['Occupations'][selected_occupation] += 1
        
        previous_entry['Quarter'] = f"Q{i+1}-2022"
        data[i] = previous_entry  # Store the updated entry without modifying previous ones
    
    return data

def generate_initial_conditions(num_conditions):
    """
    Generates multiple initial conditions and saves each to a JSON file.
    """
    for i in range(num_conditions):
        data = [
            {"Quarter": "Q1-2022", "Countries": {"USA": random.randint(1, 5), "India": random.randint(0, 5), 
                         "France": random.randint(0, 2), "UK": random.randint(0, 2), "Australia": random.randint(0, 2)},
             "Occupations": {"Sales": random.randint(1, 3), "Operations": random.randint(0, 1), 
                             "Software Engineering": random.randint(1, 4), "Information Technology": random.randint(0, 1),
                             "Marketing": random.randint(0, 1), "Administration": random.randint(0, 1), "Human Resources": random.randint(0, 1)}, 
             "Capital": round(random.uniform(0.1, 5.0), 2)}
        ]
        
        # Generate 12 quarters based on cloning previous quarters
        for _ in range(11):
            data.append(json.loads(json.dumps(data[-1])))  # Ensure independent copies
        
        updated_data = clone_previous_quarter(data)
        with open(f'company_data_{i+1}.json', 'w') as f:
            json.dump(updated_data, f, indent=4)

# Generate 25 different initial conditions
generate_initial_conditions(25)
