from os import remove, system
from os import path
from cryptography.fernet import Fernet

import os
import random
import string
import json
import pyperclip


""" FILE ENCRYPTION """


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def encrypt(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(filename, "wb") as file:
        file.write(decrypted_data)


""" PASSWORD GENERATION """


def generate_pass(length, password=[]):
    for _ in range(length):
        password.append(random.choice([random.choice(string.ascii_letters), random.choice(
            string.punctuation), random.choice(string.digits)]))

    return ''.join(map(str, password))


def write_pass():
    email = input("Enter email: ")
    website = input("Enter site: ")
    length = int(input("Length of password (>= 24 is recommended): "))
    psswd = generate_pass(length)

    try:
        decrypt("passwords.txt", key)
        with open('passwords.txt', 'r') as f:
            data = json.load(f)

        if email in data:
            for dat in data[email]:
                dat["website"].append(website)
                dat["password"].append(psswd)

            with open('passwords.txt', 'w') as f:
                f.seek(0)
                json.dump(data, f)

        else:
            acc = {}
            acc[email] = []
            acc[email].append({
                "website": [website],
                "password": [psswd]
            })

            data.update(acc)
            with open('passwords.txt', 'w') as f:
                f.seek(0)
                json.dump(data, f)

    except FileNotFoundError:
        data = {}
        data[email] = []
        data[email].append({
            'website': [website],
            'password': [psswd]
        })

        with open('passwords.txt', 'w') as outfile:
            json.dump(data, outfile)

    print("\nPASSOWRD: ", psswd)
    pyperclip.copy(psswd)
    print("PASSWORD COPIED IN CLIPBOARD")

    encrypt("passwords.txt", key)


def look_pass():
    try:
        decrypt("passwords.txt", key)
        with open('passwords.txt', "r") as f:
            data = json.load(f)
            encrypt("passwords.txt", key)

        print("--- PASSWORDS ---")
        for email in data:
            print(email)
            for dat in data[email]:
                for i in range(len(dat["website"])):
                    print(dat["website"][i].upper(), " : ", dat["password"][i])

    except FileNotFoundError:
        print("No Accounts Created")


def remove_pass():
    erase_email = input("Email: ")
    erase_site = input("Site (If no restrictions, input 0): ")

    try:
        decrypt("passwords.txt", key)
        with open("passwords.txt", "r") as f:
            data = json.load(f)
            
            if erase_email in data:
                if erase_site == '0':
                    del data[erase_email]
                else:
                    for dat in data[erase_email]:
                        if erase_site in dat["website"]:
                            dat["password"].pop(dat["website"].index(erase_site))
                            dat["website"].remove(erase_site)
                        else:
                            print("No Site Found") 
            else:
                print("No Account Found")


            with open("passwords.txt", "w") as file:
                json.dump(data, file)
            
            encrypt("passwords.txt", key)
            
    except FileNotFoundError:
        print("File Not Found")


def main():
    print("1. Generate Password")
    print("2. Look at passwords")
    print("3. Remove a Password\n")
    choice = int(input("Enter number: "))
    if choice == 1:
        system("cls")
        write_pass()

    elif choice == 2:
        system("cls")
        look_pass()

    elif choice == 3:
        system("cls")
        remove_pass()


if __name__ == "__main__":
    if not path.exists("pass"):
        os.mkdir("pass")

    curr_path = os.getcwd()
    os.chdir(curr_path + "/pass")
    if not path.exists("key.key"):
        write_key()

    key = load_key()
    main()
