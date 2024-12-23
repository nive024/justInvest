import sys
import getpass
from problem3 import *
from problem1 import *

def display_perms():
    """Display the permissions in a user friendly way"""
    perms = get_permissions()
    print("Operations available on the system:")
    for p in perms.keys():
        print(f"{p}. {perms[p]}")

def perform_operations(user):
    """Simulate performing the operation and checking if the operation is valid"""
    try:
        operation = input("Which operation would you like to perform? (Enter operation number or 'exit' to quit): ")
        if operation.lower() == "exit":
            print("Exiting operation menu.")
            sys.exit(0)
        if int(operation) > len(get_permissions())  or int(operation) <= 0:
            raise KeyError
        if not user.has_permission(int(operation)):
            print("You are not permitted to perform this operation.")
            return False
        print(f"You have performed {get_permissions()[operation]}")
        return True
    except ValueError:
        print("Invalid input. Please enter a valid operation number or 'exit' to quit.")
        return False
    except KeyError:
        print("The specified operation does not exist.")
        return False

def login_user(username: str, password: str, file: str = "passwd.txt") -> bool:
    """Login the user"""
    if (decode_password(username, password, file)):
        print("ACCESS GRANTED!")
        return True
    else:
        print("ACCESS DENIED!")
        return False

def check_password(username: str):
    """Check if the password matches the one on file"""
    password = getpass.getpass("Enter password: ")
    is_logged_in = login_user(username, password.strip())
    # Add rate limiting
    if not is_logged_in:
        for i in range(0, 3):
            print("Wrong username, or password. Please try again")
            if is_logged_in:
                break
            if i == 2:
                print("Tried too many times, exiting system.")
                exit(1)
            password = getpass.getpass("Enter password: ")
            is_logged_in = login_user(username, password.strip())

def simulate_login(is_signed_in: bool, username: str = ""):
    if is_signed_in:
        display_perms()
        users = get_user_by_username(get_users(), username)
        user_objs = get_user_objs()
        user = user_objs[users["name"]]
        perform_operations(user)
    else:
        username = input("Enter username: ")
        if (username_exists(get_users(), username=username)):
            check_password(username)
            users = get_user_by_username(get_users(), username)
            user_objs = get_user_objs()
            user = user_objs[users["name"]]

            if check_time_restriction(user.get_time_restrictions()):
                display_perms()

            while True:
                if check_time_restriction(user.get_time_restrictions()):
                    print("Your authorized permissions are:", ",".join(user.get_permissions()))
                    perform_operations(user)
                else:
                    print("You are not authorized to use the system at this time.")
                    sys.exit(0)
            
        else:
            print("Username, does not exist, please register.")
            return False

if __name__ == '__main__':
    #test input: username = sasha45, role = CLIENT
    #test input: username = johndoe, role = TELLER (to test time restriction)
    print("\njustInvest System")
    print("------------------------------------------------------------")
    simulate_login(False)