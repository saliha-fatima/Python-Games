import random
import string

# Function to generate a single random password
def generate_password(length):
    # Define the possible characters (uppercase, lowercase, digits, special characters)
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select characters to create a password of the given length
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to generate multiple passwords
def generate_passwords(num_passwords, length):
    passwords = [generate_password(length) for _ in range(num_passwords)]
    return passwords

# Main code
if __name__ == "__main__":
    # Ask the user for the number of passwords and length of each password
    try:
        num_passwords = int(input("Enter the number of passwords to generate: "))
        length = int(input("Enter the length of each password: "))
        
        # Ensure valid input
        if num_passwords <= 0 or length <= 0:
            print("Please enter positive integers for the number and length of passwords.")
        else:
            # Generate the passwords
            generated_passwords = generate_passwords(num_passwords, length)
            print("\nGenerated Passwords:")
            for idx, password in enumerate(generated_passwords, 1):
                print(f"Password {idx}: {password}")
    
    except ValueError:
        print("Please enter valid integer values for both inputs.")
