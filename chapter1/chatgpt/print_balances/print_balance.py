# Ask the user to enter the current balance, note that we expect the user
# to enter a numeric value otherwise we will receive an error
current_balance = input("Enter current balance: ")  # A

# Print the entered balance in the desired format
print(f"Current Balance: ${float(current_balance):,.2f}")  # B
