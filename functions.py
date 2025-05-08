#functions.py

import pandas as pd
import os

all_users = []


def verify_user(ic_number, password):
    if len(ic_number) != 12 or not ic_number.isdigit():
        print("Invalid IC number. It must be 12 digits.")
        return False
    if password != ic_number[-4:]:
        print("Incorrect password. It should match the last 4 digits of the IC number.")
        return False
    return True

def get_income():
    """Ask for income and validate it - returns None if below taxable limit"""
    while True:
        try:
            income = float(input(" Enter your annual income: RM"))
            if income > 0:
                return income
            print("\nYou're below the taxable income limit (RM34,000) — no tax required.")
            return None  # Signal to return to menu
        except ValueError:
            print("Please enter a valid number (e.g. 50000)")

def safe_float_input(prompt, max_value=None):
    """Safe input for float values with optional max limit"""
    while True:
        try:
            value = float(input(prompt))
            if max_value is not None:
                value = min(max_value, value)
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")

def safe_int_input(prompt):
    """Safe input for integer values"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter an integer.")
            
def calculate_tax_relief():
    disabled_parents = "N"
    disabled_child = "N"
    disabled_spouse = "N"
    disabled_individual = "N"
    child_18_below= "N"
    childDisabilityTreatmentExpenses = 0     
    print("\n=== TAX RELIEF CALCULATION ===\n")
    tax_relief = 9000
    print(f"Personal relief: RM9,000 (auto-included)")   
    disabled_individual = input("Disabled individual? Y/N: ").upper()
    if disabled_individual == "Y":
        tax_relief += 6000      
    if input("Do you have spouse/alimony expense? Y/N: ").upper() == "Y":  
        alimony = safe_float_input("Total the alimony or spouse payment: RM", max_value=4000)
        tax_relief += alimony
        disabled_spouse = input("Is your spouse disabled? Y/N: ").upper()
        if disabled_spouse == "Y":
            tax_relief += 5000
    if input("Do you have expenses for parents? Y/N: ").upper() == "Y":
        medicalAndCareExpenses = safe_float_input("Total medical/care expenses for parents: RM")        
        completeMedicalExam = safe_float_input("Total cost of medical exam for parents: RM", max_value=1000)
        parents_tax_relief = medicalAndCareExpenses + completeMedicalExam
        tax_relief += min(8000, parents_tax_relief)  
    disabled_parents = input("Are your parents disabled? Y/N: ").upper()   
    if input("Do you have children? Y/N: ").upper() == "Y":       
        breastfeeding_equipment = safe_float_input("Total breastfeeding equipment expenses: RM", max_value=1000)
        tax_relief += breastfeeding_equipment   
        if input("Do you have child aged 6 years and below? Y/N: ").upper() == "Y":
            childcare_fees = safe_float_input("Total child care fees: RM", max_value=3000)
            tax_relief += childcare_fees     
        child_18_below = input("Do you have unmarried child under the age of 18 years old? Y/N: ").upper()
        if child_18_below == "Y":
            child_18_below_num = safe_int_input("Number of unmarried children under 18: 🔢 ")
            tax_relief += child_18_below_num * 2000      
        if input("Do you have unmarried child 18+ in full-time education? Y/N: ").upper() == "Y":
            child_18_above_edu = safe_int_input("Number of children in A-Level etc: 🔢 ")
            tax_relief += child_18_above_edu * 2000
            child_diploma_or_above = safe_int_input("Number of children in diploma or higher: 🔢 ")
            tax_relief += child_diploma_or_above * 8000     
        disabled_child = input("Do you have disabled children? Y/N: ").upper()
        if disabled_child == "Y":
            num_disabled_child = safe_int_input("Number of disabled children: 🔢 ")
            tax_relief += num_disabled_child * 6000
            disabled_child_higher_edu = safe_int_input("Number of disabled children in diploma or above: 🔢 ")
            tax_relief += disabled_child_higher_edu * 8000
    if disabled_individual == "Y" or disabled_child == "Y" or disabled_spouse == "Y" or disabled_parents == "Y":
        print(">>>  Purchase of Basic Supporting Equipment for disabled individual, spouse, child, or parent >>> ")
        supporting_equipment = safe_float_input("Total expenses on basic supporting equipment: RM")
        tax_relief += supporting_equipment  
    if input("Do you have Medical Expenses ? Y/N: ").upper() == "Y":   
        print(">>>  Medical Expenses i >>> ")    
        serious_diseases = safe_float_input("Total serious disease expenses: RM")
        fertility_treatment = safe_float_input("Total fertility treatment expenses: RM")
        vaccination = safe_float_input("Total vaccination expenses: RM", max_value=1000)
        Dental_treatment = safe_float_input("Total dental treatment expenses: RM", max_value=1000)      
        print(">>>  Medical Expenses ii >>> ")
        preventiveMedicalExpenses = safe_float_input("Total preventive medical expenses: RM", max_value=1000)        
        if child_18_below == "Y":
            print(">>>  Medical Expenses for child 18 and below >>> ")
            childDisabilityTreatmentExpenses = safe_float_input("Total expenses for child aged 18 and below: RM", max_value=4000)       
        total_medical_expenses = (
            serious_diseases + fertility_treatment + vaccination +
            Dental_treatment + preventiveMedicalExpenses + childDisabilityTreatmentExpenses
        )
        tax_relief += min(10000, total_medical_expenses)
    if input("Do you have Education Expenses ? Y/N: ").upper() == "Y":  
        education_general = safe_float_input("Total general education expenses: RM") 
        education_upskill = safe_float_input("Total upskill expenses: RM", max_value=2000)
        education = education_general + education_upskill
        tax_relief += min(7000, education)   
    if input("Do you have Lifestyle Expenses ? Y/N: ").upper() == "Y": 
        print(">>>  General Lifestyle Expenses >>> ")
        lifestyle_expenses = safe_float_input("Total lifestyle expenses: RM", max_value=2500)
        tax_relief += lifestyle_expenses 
        print(">>>  Additional Lifestyle Expenses >>> ")
        additional_lifestyle_expenses = safe_float_input("Total additional lifestyle expenses: RM", max_value=1000)
        tax_relief += additional_lifestyle_expenses
    print(">>>  SSPN Net Deposit >>> ")
    sspn_deposit = safe_float_input("Total SSPN deposit: RM", max_value=8000)
    tax_relief += sspn_deposit
    print(">>>  EPF and Life Insurance >>> ")
    epf = safe_float_input("Total EPF contributions: RM", max_value=4000)
    life_insurance = safe_float_input("Total life insurance contributions: RM", max_value=3000)
    totalEPF_insurance = epf + life_insurance
    tax_relief += min(7000, totalEPF_insurance)
    print(">>>  Deferred Annuity & PRS >>> ")
    prs = safe_float_input("Total PRS/annuity: RM", max_value=3000)
    tax_relief += prs
    print(">>>  Education and Medical Insurance >>> ")
    edu_med_insurance = safe_float_input("Total education/medical insurance: RM", max_value=3000)
    tax_relief += edu_med_insurance
    print(">>>  SOCSO Contribution >>> ")
    socso = safe_float_input("Total SOCSO contribution: RM", max_value=350)
    tax_relief += socso
    print(">>>  EV Charging Equipment Expenses >>> ")
    ev_charging = safe_float_input("Total EV charging expenses: RM", max_value=2500)
    tax_relief += ev_charging
    print("\n========= TOTAL TAX RELIEF (RM) =========")
    print(f"Your total tax relief is: RM{tax_relief:,.2f}")
    
    return tax_relief

def calculate_tax(income, relief):
    """Calculate tax payable based on Malaysian tax rates"""
    # Calculate the chargeable income by subtracting the relief from the income
    chargeable_income = income - relief
    # If the chargeable income is less than or equal to 0, return 0.0
    if chargeable_income <= 0:
        return 0.0
    # Define the tax brackets,(upper limit, tax rate, lower limit)    
    tax_brackets = [
        (5000, 0.00, 0),
        (20000, 0.01, 5000),
        (35000, 0.03, 20000),
        (50000, 0.06, 35000),
        (70000, 0.11, 50000),
        (100000, 0.19, 70000),
        (400000, 0.25, 100000),
        (600000, 0.26, 400000),
        (2000000, 0.28, 600000),
        (float('inf'), 0.30, 2000000)
    ]   
    tax = 0
    # Iterate through each tax bracket
    for bracket in tax_brackets:
        # If the chargeable income is less than or equal to the upper limit of the bracket, calculate the tax
        if chargeable_income <= bracket[0]:
            tax += (chargeable_income - bracket[2]) * bracket[1]
            break
        # Otherwise, calculate the tax for the entire bracket
        tax += (bracket[0] - bracket[2]) * bracket[1]
    return tax



def read_from_csv(filename):
    """Read user data from CSV file"""
    if os.path.exists(filename):
        try:
            df = pd.read_csv(
                filename,
                dtype={
                    "ID": 'string',
                    'IC Number': 'string',
                    'Password': 'string',
                    'Income': 'float64',
                    'Tax Relief': 'float64', 
                    'Tax Payable': 'float64'
                }
            )
            return df.to_dict('records')
        except pd.errors.EmptyDataError:
            print("Note: File exists but is empty")
            return []
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return []
    else:
        return None


def save_to_csv(data, filename):
    """
    Save the user's data (IC number, income, tax relief, and tax payable) to a CSV file. 
    If the file doesn't exist, create a new file with a header row. If the file exists, 
    append the new data to the existing file 
    """
    try:   
       pd.DataFrame(data).to_csv(filename, index=False)
    except PermissionError:
        # print an error message if the file is open in another program
        print("Error: File may be open in another program")
    except Exception as e:
        # if there is any other issue, print an error message
        print(f"Save failed: {str(e)}")

def view_tax_records():
    """View tax records in a formatted table - for specific user or all records"""
    try:
        # Read data from CSV
        records = read_from_csv("tax_records.csv")    
        if not records:
            print("No tax records available.")
            return
        print("\n" + "=" * 70)
        print("ALL TAX RECORDS".center(55))
        print("=" * 70)
        # Table header
        print(f"{'User ID':<15}{'IC Number':<15} {'Income':>12} {'Tax Relief':>12} {'Tax Payable':>12}")
        print("-" * 70)
        # Table rows
        for record in records:

            print(
                    f"{record['ID']:<15} " 
                    f"{record['IC Number']:<15} "
                    f"RM{record['Income']:>10,.2f} "
                    f"RM{record['Tax Relief']:>10,.2f} "
                    f"RM{record['Tax Payable']:>10,.2f}")
            print("=" * 70)       
    except Exception as e:
        print(f"Error reading tax records: {str(e)}")

