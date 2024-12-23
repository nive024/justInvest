# justInvest

## Project Overview:
This is a python based system that handles:
- User registration with password validation
- User login with password checking
- Role based access to the system

## Features
### 1. User Registration
  - Validates password strength based on the following rules:
	- Length must be between 8 and 12 chars.
	- Password must include an uppercase letter, lowercase letter, digit and a special char.
	- Password must not be part of a list of common passwords.
	- Password must not contain repeating sequences of chars length 3.
	- Password must not contain the name of the system.
	- Password must not contain your username.
  - Ensures username uniqueness.
  - Prompts for role assignment from a predefined list, and applies time restriction if needed.

### 2. User Authentication
   - Encodes passwords securely using bcrypt and saves it to a password file.
   - Validates login credentials.

### 3. Role-Based Permissions
   - Associates roles with specific permissions.
   - Validates users' ability to perform operations based on their assigned role.
   - Ensures that certain roles cannot access the system during specific times 

### 4. Operations Management
   - Allows users to perform system-defined operations if permitted by their role.

## Predefined Roles
The following roles are pre-configured in roles_permission.json:
- CLIENT
- PREMIUM_CLIENT
- FINANCIAL_ADVISOR
- FINANCIAL_PLANNER
- TELLER (with time-based restrictions)

## Requirements
- Python 3.7+
- getpass (standard library)
- unittest for testing
- bcrypt 

## Usage

Run the script to use the system: <br/>
python main.py<br/>

This is how to run the unit tests:<br/>
python3 -m unittest test_problem1.py<br/>
python3 -m unittest test_problem2.py<br/>
python3 -m unittest test_problem3.py<br/>
python3 -m unittest test_problem4.py




