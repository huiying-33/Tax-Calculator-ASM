import functions as f


filename = "tax_records.csv"
f.all_users = f.read_from_csv(filename) or []

   


while True:
    print("\n========== Malaysian Tax Calculator ==========")
    registered = input("Have you registered before? (Y/N)\n(V: View all records | Q: Quit)\n> ").strip().upper()
   

    if registered == "N":
        option = "1"  
    elif registered == "Y":
        option = "2"
    elif registered == "V":
        option = "3"
    elif registered == "Q":
        option = "4"   
    else:
        print("Invalid input. Please enter 'Y' , 'V' , 'Q' or 'N'.")
        continue  # Back to the top of while loop

    
    if option == "1":  # Register new user
        print("\n--- NEW USER REGISTRATION ---")
        user_id = input("Enter your user ID: ")
        ic = input("Enter your IC number (12 digits, numbers only): ").strip()
        
        if len(ic) == 12 and ic.isdigit():
            # Check if user already exists
            user_exists = False
            for user in f.all_users:
                if user["IC Number"] == ic:
                    user_exists = True
                    break
            
            if user_exists:
                print("User with this IC already exists. Please login instead.")
            else:
                password = ic[-4:]  # Last 4 digits as password
                new_user = {
                    "ID": user_id,
                    "IC Number": ic,
                    "Password": password,
                    "Income": 0.0,
                    "Tax Relief": 0.0,
                    "Tax Payable": 0.0
                }
                
                f.all_users.append(new_user)  # Add to global list
                f.save_to_csv(f.all_users, filename)  # Save to CSV
                print(f"Registration successful! Your password is: {password}")
                print("Please login with your credentials.")
        else:
            print("Invalid IC! Must be 12 digits with numbers only.")
    
    elif option == "2":  # Login existing user
        print("\n--- USER LOGIN ---")
        user_id = input("Enter your user ID: ")
        ic = input("Enter your IC number (12 digits): ").strip()
        password = input("Enter your password (last 4 digits of IC): ")
        
        if f.verify_user(ic, password):
            
            
            # Find current user
            current_user = None
            for user in f.all_users:
                if user["IC Number"] == ic:
                    if user["ID"] == user_id:
                        current_user = user
                        break   
                    else:
                        print("Incorrect user ID! Please try again.")
                        break
            
            if current_user:
                # Show user menu
                print(f"\nLogin successful! Welcome, {current_user['ID']}!")
                
                while True:
                    print("\n--- Tax Calculator Menu ---")
                    print("1. Calculate your tax")
                    print("2. View your previous calculation")
                    print("3. Return to main menu")
                    
                    
                    user_option = input("Choose an option (1-3): ")
                    
                    if user_option == "1":
                        # Get income and calculate tax
                        income = f.get_income()
                        if income is not None:  # If income is above taxable limit
                            relief = f.calculate_tax_relief()  # Calculate tax relief
                            tax = f.calculate_tax(income, relief)  # Calculate tax payable
                            
                            # Update user data
                            current_user.update({
                                "Income": income,
                                "Tax Relief": relief,
                                "Tax Payable": tax
                            })
                            
                            # Save to CSV
                            f.save_to_csv(f.all_users, filename)
                            
                            # Display tax calculation
                            print("\n=== FINAL CALCULATION ===")
                            print(f"Income: RM{income:,.2f}")
                            print(f"Tax Relief: RM{relief:,.2f}")
                            print(f"Chargeable Income: RM{max(0, income - relief):,.2f}")
                            print(f"Tax Payable: RM{tax:,.2f}")
                    
                    elif user_option == "2":
                        print("\n=== YOUR TAX RECORD ===")
                        print(f"User ID: {current_user['ID']}")
                        print(f"IC Number: {current_user['IC Number']}")
                        print(f"Income: RM{current_user['Income']:,.2f}")
                        print(f"Tax Relief: RM{current_user['Tax Relief']:,.2f}")
                        print(f"Chargeable Income: RM{max(0, current_user['Income'] - current_user['Tax Relief']):,.2f}")
                        print(f"Tax Payable: RM{current_user['Tax Payable']:,.2f}")
                    
                    elif user_option == "3":
                        break
                    
                    else:
                        print("Invalid option. Please choose 1, 2, or 3.")
        else:
            print("Login failed.")
    
    elif option == "3":  # View all tax records
        f.view_tax_records()
    
    elif option == "4":  # Exit program
        print("Thank you for using the tax calculator!")
        break
    
    else:
        print("Invalid input. Please select 1, 2, 3, or 4")