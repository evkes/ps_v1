import random
import json
import math

def clone_previous_quarter(data, growth_type="linear"):
    """
    Clones the previous quarter and adds a random number of employees to categories and countries.
    Growth can be linear, quadratic, exponential, bell curve, logistic, cyclic, stagnation-growth, decline, acquisition, or failure.
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
        
        # Determine employee growth type
        if growth_type == "linear":
            new_hires = random.randint(1, 3)
        elif growth_type == "quadratic":
            new_hires = random.randint(3, 7) ** 2 // 10
        elif growth_type == "exponential":
            new_hires = max(1, int(math.exp(random.uniform(0.5, 1.5))))
        elif growth_type == "bell_curve":
            midpoint = num_quarters // 2
            variance = max(1, int((midpoint - abs(midpoint - i)) ** 1.5))
            new_hires = random.randint(1, variance)
        elif growth_type == "logistic":
            k = 10
            new_hires = int(k / (1 + math.exp(-0.5 * (i - num_quarters // 2))))
        elif growth_type == "cyclic":
            new_hires = int(2 + 2 * math.sin(i * math.pi / 6))
        elif growth_type == "stagnation-growth":
            new_hires = random.randint(0, 1) if i % 3 != 0 else random.randint(5, 8)
        elif growth_type == "decline":
            new_hires = -random.randint(1, 3)  # Employee loss per quarter
        elif growth_type == "acquisition":
            new_hires = random.randint(1, 3)
            if i == num_quarters // 2:
                new_hires += random.randint(20, 50)  # Big spike in employees mid-way
        elif growth_type == "failure":
            new_hires = random.randint(1, 3)
            if i > num_quarters // 3:
                new_hires = -random.randint(2, 5)  # Gradual decline into failure
        
        # Expand or shrink employees in prioritized countries and occupations
        country_keys = list(previous_entry['Countries'].keys())
        occupation_keys = list(previous_entry['Occupations'].keys())
        
        country_weights = [0.5 if c in ['USA', 'India'] else 0.2 for c in country_keys]
        occupation_weights = [0.5 if o in ['Sales', 'Software Engineering'] else 0.2 for o in occupation_keys]
        
        for _ in range(abs(new_hires)):
            selected_country = random.choices(country_keys, weights=country_weights)[0]
            previous_entry['Countries'][selected_country] = max(0, previous_entry['Countries'][selected_country] + (1 if new_hires > 0 else -1))
        
        for _ in range(abs(new_hires)):
            selected_occupation = random.choices(occupation_keys, weights=occupation_weights)[0]
            previous_entry['Occupations'][selected_occupation] = max(0, previous_entry['Occupations'][selected_occupation] + (1 if new_hires > 0 else -1))
        
        previous_entry['Quarter'] = f"Q{i+1}-2022"
        data[i] = previous_entry  # Store the updated entry without modifying previous ones
    
    return data

def generate_initial_conditions(num_conditions, growth_type="linear"):
    """
    Generates multiple initial conditions and saves each to a JSON file.
    Growth type can be "linear", "quadratic", "exponential", "bell_curve", "logistic", "cyclic", "stagnation-growth", "decline", "acquisition", or "failure".
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
        
        for _ in range(11):
            data.append(json.loads(json.dumps(data[-1])))  # Ensure independent copies
        
        updated_data = clone_previous_quarter(data, growth_type)
        with open(f'company_data_{growth_type}_{i+1}.json', 'w') as f:
            json.dump(updated_data, f, indent=4)

# Generate different growth types
generate_initial_conditions(5, "linear")
generate_initial_conditions(5, "quadratic")
generate_initial_conditions(3, "exponential")
generate_initial_conditions(3, "bell_curve")
generate_initial_conditions(3, "logistic")
generate_initial_conditions(3, "cyclic")
generate_initial_conditions(3, "stagnation-growth")
generate_initial_conditions(3, "decline")
generate_initial_conditions(2, "acquisition")
generate_initial_conditions(2, "failure")