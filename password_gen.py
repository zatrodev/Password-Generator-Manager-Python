from os import system
from os import path
from cryptography.fernet import Fernet

import os
import random
import string
import json
import pyperclip


""" DATA ENCRYPTION """


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
        rand = random.randint(1, 3)
        if rand == 1:
            password.append(
                string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)])
        elif rand == 2:
            password.append(
                string.punctuation[random.randint(0, len(string.punctuation) - 1)])
        elif rand == 3:
            password.append(
                string.digits[random.randint(0, len(string.digits) - 1)])

    return ''.join(map(str, password))


def write_pass():
    email = input("Enter email: ")
    website = input("Enter site: ")
    length = int(input("Length of password (>= 24 is recommended): "))
    psswd = generate_pass(length)

    try:
        with open('passwords.txt', 'r+') as f:
            data = json.load(f)

            if email in data:
                for dat in data[email]:
                    """
                    if not isinstance(dat["website"], list) and not isinstance(dat["password"], list):
                        dat["website"] = [dat["website"]]
                        dat["password"] = [dat["password"]]
                    """

                    dat["website"].append(website)
                    dat["password"].append(psswd)

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
        with open('passwords.txt', "r+") as f:
            data = json.load(f)
            encrypt("passwords.txt", key)

        # email = input("Enter email: ")

        print("--- PASSWORDS ---")
        for email in data:
            print(email)
            for dat in data[email]:
                for i in range(len(dat["website"])):
                    print(dat["website"][i], " : ", dat["password"][i])

    except FileNotFoundError:
        print("No Accounts Created")


def main():
    print("1. Generate Password")
    print("2. Look at passwords\n")
    choice = int(input("Enter number: "))
    if choice == 1:
        system("cls")
        write_pass()

    elif choice == 2:
        system("cls")
        look_pass()


if __name__ == "__main__":
    if not path.exists("pass"):
        os.mkdir("pass")

    curr_path = os.getcwd()
    os.chdir(curr_path + "/pass")
    if not path.exists("key.key"):
        write_key()

    key = load_key()
    main()
