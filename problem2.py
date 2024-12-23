import bcrypt
import string
import getpass
from typing import List

def get_users_from_pwd(file: string = "passwd.txt") -> List:
    """Return a list of users that are saved in the passwd.txt file"""
    with open(file, "rb") as file:
        lines = file.readlines()
    return [line.strip().split(b":") for line in lines]

def encode_password(username: str, password: str, file: string = "passwd.txt") -> bool:
    """Encode and save a given password to the password file"""
    bytes = password.encode()
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    with open(file, "a+") as f:
        f.write(f"{username}:{hash.decode()}\n")
    return True

def decode_password(username: str, password: str, file: string = "passwd.txt") -> bool:
    """Check if the hash of a given password matches the one saved for that username"""
    user_hashes = get_users_from_pwd(file)
    #if file empty then return false
    if not user_hashes:
        print("No users registered.")
        return False
    for user in user_hashes:
        if user[0].decode().strip() == username:
            return bcrypt.checkpw(password.encode(), user[1].strip())
        
    return False

def main():
    #Test decode with a username that is already in the system: sasha45, password: Nivetha45!
    print("\njustInvest System")
    print("------------------------------------------------------------")
    print("1. Enroll User")
    print("2. Sign In")

    #question: is it ok if we dont have validation here --> bad password will be mixed with good password
    choice = input("What would you like to do: ")
    if choice == "1":
        username = input("What is your name: ")
        password = getpass.getpass("What is your password: ")

        print("Encoding password: ", encode_password(username, password))
        print("Decoding password: ", decode_password(username, password))
    elif choice == "2":
        username = input("What is your username: ")
        password = getpass.getpass("What is your password: ")

        print("Decoding password: ", decode_password(username, password))

if __name__ == '__main__':
    main()

#emery blake: u = emery7, pwd = Christmas34!
#john doe: u = johnDoe, pwd = Password123!

