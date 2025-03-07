import json
import math
import os

def calculate_revenue(employee_data):
    """
    Calculate revenue based on employee distribution across countries and job roles.
    
    Args:
        employee_data (dict): A dictionary containing employee distribution data.
        
    Returns:
        dict: Revenue calculations and related metrics.
    """
    # Default revenue multiplier (150K per FTE)
    revenue_multiplier = 150000
    revenue_reason = {}
    
    # Extract country and occupation data
    countries = employee_data.get("Countries", {})
    occupations = employee_data.get("Occupations", {})
    
    # Calculate total employees
    total_employees = sum(countries.values())
    
    if total_employees == 0:
        return {"revenue": 0, "reason": "No employees"}
    
    # Calculate percentages for job roles
    sales_employees = occupations.get("Sales", 0)
    engineering_employees = occupations.get("Software Engineering", 0) + occupations.get("Information Technology", 0)
    other_employees = total_employees - sales_employees - engineering_employees
    
    pct_sales = sales_employees / total_employees if total_employees > 0 else 0
    pct_engg = engineering_employees / total_employees if total_employees > 0 else 0
    pct_other = other_employees / total_employees if total_employees > 0 else 0
    
    # Default distribution if no employees in sales or engineering
    if pct_sales == 0 and pct_engg == 0 and pct_other == 1:
        pct_sales = 0.45
        pct_engg = 0.45
        pct_other = 0.1
    
    # Calculate western/eastern hemisphere percentages
    western_countries = ["USA", "Australia", "UK", "France"]  # Equivalent to USA, AUS, GBR, EUR in original code
    eastern_countries = ["India"]  # Equivalent to IND in original code
    
    western_employees = sum(countries.get(country, 0) for country in western_countries)
    eastern_employees = sum(countries.get(country, 0) for country in eastern_countries)
    
    pct_western = western_employees / total_employees if total_employees > 0 else 0
    pct_eastern = eastern_employees / total_employees if total_employees > 0 else 0
    
    # Calculate multipliers based on job type and location
    western_multiplier = (pct_sales * 150000) + (pct_engg * 100000) + (pct_other * 75000)
    eastern_multiplier = (pct_sales * 30000) + (pct_engg * 25000) + (pct_other * 20000)
    
    # Calculate final revenue multiplier
    revenue_multiplier = round(pct_western * western_multiplier + pct_eastern * eastern_multiplier)
    
    # Use default if calculation fails
    if revenue_multiplier <= 0:
        print(f"WARN: Revenue multiplier failed to be calculated, using default")
        revenue_multiplier = 150000
        revenue_reason["using_default"] = True
    else:
        revenue_reason["revenue_multiplier"] = revenue_multiplier
        revenue_reason["has_employee_breakdowns"] = True
    
    # Calculate final revenue
    revenue = total_employees * revenue_multiplier
    capital = employee_data.get("Capital", 0)
    
    return {
        "revenue": revenue,
        "revenue_per_employee": revenue_multiplier,
        "capital_to_revenue_ratio": capital * 1000000 / revenue if revenue > 0 else 0
    }

def update_json_files(json_files):
    """
    Update the specified JSON files with revenue information.
    
    Args:
        json_files (list): List of JSON filenames to update.
    """
    for filename in json_files:
        try:
            # Load the JSON data
            with open(filename, 'r') as file:
                company_data = json.load(file)
            
            # Add revenue information to each quarter
            for quarter in company_data:
                revenue_info = calculate_revenue(quarter)
                quarter["Revenue"] = revenue_info["revenue"]
                quarter["RevenuePerEmployee"] = revenue_info["revenue_per_employee"]
                quarter["CapitalToRevenueRatio"] = revenue_info["capital_to_revenue_ratio"]
            
            # Write the updated data back to the file
            with open(filename, 'w') as file:
                json.dump(company_data, file, indent=4)
            
            print(f"Updated {filename} with revenue information.")
            
            # Create a backup of the original file if it doesn't exist
            backup_filename = f"{filename}.backup"
            if not os.path.exists(backup_filename):
                with open(backup_filename, 'w') as backup_file:
                    json.dump(company_data, backup_file, indent=4)
                print(f"Created backup of original data at {backup_filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # List of JSON files to update
    json_folder = "json"
    json_files = [os.path.join(json_folder, f) for f in os.listdir(json_folder) if f.endswith('.json')]
    
    update_json_files(json_files)
    print("All JSON files have been updated with revenue information.")