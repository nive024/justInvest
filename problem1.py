import json
import sys
import datetime

class User:
    def __init__(self, name, role, permissions, time_restriction):
        self.name = name
        # self.username = username
        self.role = role
        self.permissions = permissions 
        self.time_restriction = time_restriction


    def has_permission(self, permission: int) -> bool:
        """Check if the user has a specific permission"""
        for i in self.permissions:
            if int(permission) == i:
                return True
        return False    
            
    def get_permissions(self) -> str:
        """Return a list of permission values for display or other uses"""
        return sorted([str(perm) for perm in self.permissions])
    
    def get_time_restrictions(self) -> tuple:
        """Return a tuple with the start and end time they can use the system,
        null if no restriction exists"""
        try:
            start = get_roles()[self.role]["time_restriction"]["start"]
            end = get_roles()[self.role]["time_restriction"]["end"]
            return (start, end)
        except:
            return ()


def load_json_data() -> tuple:
    """Load the user, role and permission data from the JSON"""
    #open and read the json to take in the permissions, users and roles 
    with open("roles_permission.json", "r") as f:
        data = json.load(f)
        permissions = data["permissions"] #will be used in a later problem
        users = data["users"]
        roles = data["roles"]
    
    #create users
    user_objs = {}
    for user in users:
        perms = roles[users[user]["role"]]["permissions"]
        time = {} #TODO: implement time
        try:
            time = roles[users[user]["role"]]["time_restriction"]
        except KeyError:
            pass 
        user_objs[user] = User(user, users[user]["role"], perms, time)
    return users, roles, permissions, user_objs

def get_users() -> dict:
    """Return a dictionary of the users"""
    return load_json_data()[0]

def get_roles() -> dict:
    """Return a dictionary of the roles"""
    return load_json_data()[1]

def get_permissions() -> dict:
    """Return a dictionary of the permissions"""
    return load_json_data()[2]

def get_user_objs() -> dict:
    """Return a dictionary of User objects"""
    return load_json_data()[3]

def get_user_by_username(data: dict, username: str) -> dict:
    """Get a user by a given username"""
    for name, info in data.items():
        if info.get("username") == username:
            return {"name": name, "info": info}
    return None

def check_time_restriction(times: tuple) -> bool:
    """Check if the current time is between the restricted time."""
    if times:
        hour = datetime.datetime.now().hour
        return hour > times[0] and hour < times[1]
    return True

def main():
    #ONLY WORKS FOR REGISTERED USERS!!!! (because enrolling is in P3)
    #test input: username = sasha45, role = CLIENT
    #test input: username = johndoe, role = TELLER (to test time restriction)
    print("\njustInvest System")
    print("------------------------------------------------------------")
    username = input("What is your username: ")

    #try to get a User object by the username, if KeyError then user doesn't exist in system
    try:
        user = get_user_objs()[get_user_by_username(get_users(), username)["name"]]
    except:
        print("User not registered.")
        return

    #if the user doesn't have a time restriction disallowing the user from using the system
    if check_time_restriction(user.get_time_restrictions()):
        perms = get_permissions()    
        print("Operations available on the system:")
        for p in perms.keys():
            print(f"{p}. {perms[p]}")
        print("Your authorized permissions are:", ",".join(user.get_permissions()))
        #keep looping until user wants to 'exit'
        while True:
            try:
                operation = input("Which operation would you like to perform? (Enter operation number or 'exit' to quit): ")
                if operation.lower() == "exit":
                    print("Exiting operation menu.")
                    sys.exit(0)
                if int(operation) > len(get_permissions()) or int(operation) <= 0:
                    raise KeyError
                if not user.has_permission(int(operation)):
                    print("You are not permitted to perform this operation.")
                    continue
                print(f"You have performed {get_permissions()[operation]}")
                continue
            except ValueError:
                print("Invalid input. Please enter a valid operation number or 'exit' to quit.")
            except KeyError:
                print("The specified operation does not exist.")
    else:
        print("You are not authorized to use the system at this time.")
    
if __name__ == '__main__':
    main()

