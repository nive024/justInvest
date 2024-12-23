import json

from typing import Dict
from problem1 import *
from problem2 import *
import getpass

def display_roles():
    """Display the roles in a user friendly way"""
    roles = get_roles()
    print("Operations available on the system:")
    i = 1
    for r in roles.keys():
        print(f"{i}. {r}")
        i += 1

def find_repeat_seq(password: str) -> bool:
    """Find repetitive sequences in the given password"""
    checked = set()
    for length in range(3, len(password) // 2 + 1):
        for i in range(len(password) - length + 1):
            substring = password[i:i + length]
            if substring in checked:
                return True
            checked.add(substring)
    return False

def check_common_password(password: str) -> bool:
    """Check if the given password is in the common password file"""
    with open("common_passwords.txt", 'r') as f:
        passwords = [line.strip() for line in f.readlines()]
    return password.lower() in passwords

def validate_password(username:str, password: str) -> bool:
    """Check if the given password follows all the rules"""
    if "justinvest" in password.lower():
        return False, "Password cannot contain company name."
    try:
        if check_common_password(password):
            return False, "Password is too common, please choose another one."
    except FileNotFoundError:
            print(f"Error: Common passwords file common_passwords.txt not found.")
            return False
    if find_repeat_seq(password):
        return False, "Password must not contain one or more repeating sequences."
    if len(password) < 8 or len(password) > 12:
        return False, "Password must be between 8 to 12 characters long."
    if not any(chr in password for chr in ['!', '@', '#', '$', '%', '*', '&']):
        return False, "Password must include a special character from: !, @, #, $, %, *, &."
    if not any((chr in password and chr.isalpha()) for chr in password.upper()):
        return False, "Password must include at least one uppercase letter."
    if not any((chr in password and chr.isalpha()) for chr in password.lower()):
        return False, "Password must include at least one lowercase letter."
    if not any(chr.isdigit() for chr in password):
        return False, "Password must include at least one digit."
    if username.lower() in password.lower():
        return False, "Password must not contain your username."
    return True, ""

def username_exists(data: Dict, username: str = "") -> bool:
    """Check if the given username exists in the system"""
    for user_data in data.values():
        if user_data.get("username") == username:
            return True
    return False

def save_user(users:str, file:str):
    """Save user to json"""
    # Update the JSON file
    with open(file, "r") as f:
        data = json.load(f)
    data["users"] = users
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def get_valid_username(users: Dict[str, dict]) -> str:
    """Get a valid, unique username from the user."""
    username = input("Enter username: ")
    while username_exists(users, username):  
        print("Username already in use, please sign in or choose a new one.")
        username = input("Enter username: ")
    return username 

def get_valid_password(username: str) -> str:
    """Prompt for a valid password and confirm it."""
    password = getpass.getpass("Enter password: ")
    is_valid, msg = validate_password(username, password)
    while not is_valid:
        print(msg)
        password = getpass.getpass("Enter password: ")
        is_valid, msg = validate_password(username, password)
    
    confirm_password = getpass.getpass("Confirm password: ")
    while not password.strip() == confirm_password.strip():
        confirm_password = getpass.getpass("Passwords do not match, please try again: ")
    return password

def assign_role() -> str:
    """Display available roles and let the user choose one."""
    display_roles()
    role = int(input("What is your role: "))
    while role < 1 or role > len(get_roles()):
        print("Invalid input. Please select a valid role number.")
        role = int(input("What is your role: "))
    return list(get_roles().keys())[role - 1]

def enroll_user(role_perm_file: str = "roles_permission.json"):
    """Enroll the user"""
    users = get_users()

    name = input("What is your full name: ").lower()
    name_alr_there = name in users.keys()
    if name_alr_there:
        if users[name]["username"]:
            print("User already registered, please sign in.")
            return False
    username = get_valid_username(users)
    password = get_valid_password(username)

    # Encode the password and proceed with enrollment
    if encode_password(username, password):

        print("Successfully enrolled user!")
        if not name_alr_there:
            users[name] = {}
            users[name]["username"] = username
            users[name]["role"] = assign_role()
        
        try:
            save_user(users, role_perm_file)
        except (OSError, IOError) as e:
            print(f"Error saving user data: {e}")
            return False

        return True
        
    else:
        print("Error, please try again later!")
        exit(1)
    

if __name__ == '__main__':
    print("\njustInvest System")
    print("------------------------------------------------------------")
    enroll_user()
    
    