#!/usr/bin/python3

import random, math
import sys, os

# next task is to implement this code to be a script. 
# that means you can run it like this: "python3 main.py -e (for encrypt) -13 -text=/PATH/TO/TEXTFILE"
# then it prompts for a key-file, and if none is present, making a new one.
# same goes for decrypting

SYMBOLS = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"*@^\\#%&/(')=+?-_.,< >:~[|]{;}\n"""

while True:
    print("enter your mode here (encrypt/decrypt)")
    mode = input("> ")
    if mode == "encrypt" or mode == "decrypt":
        break
    else:
        print("check your spelling!")

while True:
    try:
        print("key number between 2 and 83:")
        key = int(input("> "))
        break
    except ValueError:
        print("it has to be an integer")

myMode = mode
print("enter the filename of the plaintext or ciphertext here:")
myMessage = input("> ")
with open(myMessage, "r") as f:
    myMessage = f.read()


def transDecryptMessage(key, message):

    numOfColumns = math.ceil(len(message) / key)
    numOfRows = key
    numOfShadeBoxes = (numOfColumns * numOfRows) - len(message)

    plaintext = [""] * numOfColumns

    col = 0
    row = 0

    for symbol in message:
        plaintext[col] += symbol
        col += 1

        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadeBoxes):
            col = 0
            row += 1

    return "".join(plaintext)

def transEncryptMessage(key, message):

    ciphertext = [""] * key

    for col in range(key):
        pointer = col

        while pointer < len(message):
            ciphertext[col] += message[pointer]

            pointer += key

    return "".join(ciphertext)

def convertToHex(ciphertext):
    unic = [ord(let) for let in ciphertext]

    hexa = []

    for num in unic:
        hexa.append("%02x" % num)
    
    return "".join(hexa)

def convertFromHex(ciphertext):
    return bytearray.fromhex(ciphertext).decode()

def adding(ciphertext):
    int_nums = [int(n) for n in ciphertext]

    SHIFT = [7, 5, 3]

    ret_nums = []
    counter = 0
    for num in int_nums:
        num += SHIFT[counter]
        if num >= 10:
            num -= 10
        ret_nums.append(num)
        counter += 1
        if counter >= 3:
            counter = 0
    
    ret_nums = [str(n) for n in ret_nums]

    return "".join(ret_nums)

def subtracting(ciphertext):
    cipher_nums = [int(n) for n in ciphertext]

    SHIFT = [7, 5, 3]
    plain_nums = []
    counter = 0
    for num in cipher_nums:
        num -= SHIFT[counter]
        if num < 0:
            num += 10
        plain_nums.append(num)
        counter += 1
        if counter >= 3:
            counter = 0

    plain_nums = [str(n) for n in plain_nums]

    return "".join(plain_nums)

def generate_estring(filename):
    L_symbols = list(SYMBOLS)

    encrypt_key = []

    count = len(L_symbols)

    while count > 0:
        num = random.randint(0, count - 1)
        encrypt_key.append(L_symbols[num])
        del(L_symbols[num])
        count -= 1

    e_string = "".join(encrypt_key)
    e_string = convertToHex(e_string)

    with open(filename + ".txt", "w") as f:
        f.write(e_string)

    print("------------------------")
    print("The encyption string is ready. It has been saved as " + filename + ".txt")
    print("it lies in the working directory.")
    print(">" + e_string + "<")
    print("------------------------")

    return e_string

def encrypt_message(message, e_string, e_string_list, key, filename):

    ret_string = ""

    for let in message:
        if let in e_string:
            num = e_string.find(let)
            num = num + key

            if num >= len(e_string_list):
                num -= len(e_string_list)
            elif num < 0:
                num += len(e_string_list)
            
            ret_string = ret_string + e_string_list[num]

    if key < len(ret_string) / 2:
        ret_string = transEncryptMessage(key, ret_string)
    else:
        ret_string = transEncryptMessage(3, ret_string)

    ret_string = convertToHex(ret_string)
    ret_string = transEncryptMessage(3, ret_string)
    ret_string = convertToHex(ret_string)
    ret_string = adding(ret_string)

    print("your message has been encrypted and put in the file: ciphertext.txt")
    with open("ciphertext.txt", "w") as f:
        f.write(ret_string)

    return ret_string

def decrypt_message(key, message, filename):
    string_file = open(filename + ".txt", "r")
    e_string = string_file.read()
    string_file.close()

    e_string = convertFromHex(e_string)

    message = subtracting(message)
    message = convertFromHex(message)
    message = transDecryptMessage(3, message)
    message = convertFromHex(message)

    if key < len(message) / 2:
        message = transDecryptMessage(key, message)
    else:
        message = transDecryptMessage(3, message)

    ret_string = ""

    for let in message:
        if let in e_string:
            num = e_string.find(let)
            num = num - key

            if num >= len(e_string):
                num -= len(e_string)
            elif num < 0:
                num += len(e_string)
            
            ret_string = ret_string + e_string[num]

    print("your message has been decrypted and put in the file: plaintext.txt")
    with open("plaintext.txt", "w") as f:
        f.write(ret_string)

    return ret_string

def main(mode, message, key):
    if mode == "encrypt":
        print("Do you want to use an existing e_string? y/n")
        prompt = input("> ")
        if prompt == "y":
            print("enter the name of the e_string file, excluding .txt")
            filename = input("> ")
            with open(filename + ".txt", "r") as f:
                e_string = f.read()
                e_string = e_string.split()
                e_string = convertFromHex(e_string[0])
        else:
            print("what should e_string file be called?")
            filename = input("> ")
            e_string = generate_estring(filename)
            e_string = convertFromHex(e_string)

        e_string_list = list(e_string)
        
        ciphertext = encrypt_message(message, e_string, e_string_list, key, filename)

        print("------------MESSAGE------------")
        print(ciphertext)
        print("------------MESSAGE------------")

    if mode == "decrypt":
        print("what is the filename of the e_string (excluding .txt)")
        filename = input("> ")
        plaintext = decrypt_message(key, message, filename)
        print("------------MESSAGE------------")
        print(plaintext)
        print("------------MESSAGE------------")

if __name__ == "__main__":
    main(myMode, myMessage, key)
