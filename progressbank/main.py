initialAcNo = 50000000

import json
import acstatement


def update_data():
    file = open('users.txt', "w")
    content = ""
    for i in user_list:
        content = content + str(i) + "\n"
    file.write(content)


def Acdetails():
    print("Account Details\n")
    for i in user_data:
        if i == "password":
            continue
        print(i, ":", user_data[i])


def deposite(username):
    print("Deposit")
    amount = float(input("Enter the amount\n"))
    for i in user_list:
        if i['user_name'] == username:
            i["Ac_balance"] = i["Ac_balance"] + amount

    update_data()
    acstatement.createEntry(username, amount, "credit")
    print("Deposit successful")


def withdraw(username):
    print("Withdraw")
    amount = float(input("Enter the amount\n"))
    if amount > user_data["Ac_balance"]:
        print("Balance not enough")
        return
    for i in user_list:
        if i['user_name'] == username:
            i["Ac_balance"] = i["Ac_balance"] - amount
    print("Withdraw successful")

    update_data()
    acstatement.createEntry(username, amount, "debit")


def transfer(user):
    print("Transfer")
    acNumber = int(input("Enter the account number to which you want to transfer\n"))
    amount = float(input("Enter the amount\n"))
    if amount > user_data["Ac_balance"]:
        print("Balance not enough")
        return
    acExist = 0
    for i in user_list:
        if i["AcNo"] == acNumber:
            acExist = 1

    if acExist == 0:
        print("This account number does not belong to anyone\n")
        return
    for i in user_list:
        if i["user_name"] == user:
            i["Ac_balance"] = i["Ac_balance"] - amount
        if i["AcNo"] == acNumber:
            i["Ac_balance"] = i["Ac_balance"] + amount

    update_data()
    acstatement.createEntry(user, amount, "debit")
    print("Transfer successful")


def Acstatement():
    print("Account Statement")
    statfile = open("acstatement.txt")
    filecon = statfile.read()
    filesplt = filecon.split("\n")
    for i in filesplt:
        linesplt = i.split(" ")
        if linesplt[0] == user_name:
            print(i)


user_data = {}
user_list = []


def valid_user(username, password):
    global user_data
    global user_list
    users_data = open("users.txt", "r")
    content = users_data.read()
    splt = content.split("\n")

    for i in splt:
        if i.strip() == "":
            continue  # Skip empty lines
        to_dq = i.replace("'", "\"")
        try:
            user_list.append(json.loads(to_dq))
        except json.JSONDecodeError:
            print(f"Skipping malformed line: {i}")
            continue  # Skip invalid lines

    userfound = False
    for value in user_list:
        if value["user_name"] == username:
            userfound = True
            if value["password"] == password:
                user_data = value
                print("Login successful")
                return "success"
            else:
                print("Invalid password")
                return None
    if not userfound:
        print("Invalid username")
        return None


def getNumberOfUsers():
    users_file = open("users.txt")
    contant = users_file.read()
    consplit = contant.split("\n")
    NumberOfUsers = len(consplit)
    return NumberOfUsers


def register():
    userCount = getNumberOfUsers()
    AcNo = initialAcNo + userCount
    name = input("Enter your name\n")
    phno = input("Enter your phone number\n")
    adress = input("Enter your address\n")
    email = input("Enter your email ID\n")
    user_name = input("Enter a username\n")
    password = input("Enter a password\n")

    userData = {
        "name": name,
        "phno": phno,
        "adress": adress,
        "email": email,
        "user_name": user_name,
        "password": password,
        'AcNo': AcNo,
        "Ac_balance": 0
    }
    userdatastr = str(userData)
    userdatastr = userdatastr + "\n"
    users_file = open("users.txt", "a")

    users_file.write(userdatastr)
    print("Registration successful")


print("Welcome to Progress Bank. Please choose one of the following options")
option = input("1. Login\t2. Register\n")
if option == "1":
    user_name = input("Please enter your username\n")
    password = input("Please enter your password\n")
    valid = valid_user(user_name, password)
    if valid == "success":
        print("Select one of the following options:\n1. View account details\n2. Deposit\n3. Withdraw\n4. Transfer\n5. View account statement\n")
        option2 = input()
        if option2 == "1":
            Acdetails()
        elif option2 == "2":
            deposite(user_name)
        elif option2 == "3":
            withdraw(user_name)
        elif option2 == "4":
            transfer(user_name)
        elif option2 == "5":
            Acstatement()
        else:
            print("Invalid option")
elif option == "2":
    register()
else:
    print("Invalid option")
