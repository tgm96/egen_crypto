import random
import trans_cipher, trans_cipher_decr
import sys


SYMBOLS = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"*@^\\#%&/(')=+?-_.,< >:[]{;}"""


while True:
    print("enter your mode here (encrypt/decrypt")
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
print("enter the plaintext or ciphertext here:")
myMessage = input("> ")

def convertToHex(ciphertext):
    unic = [ord(let) for let in ciphertext]

    hexa = []

    for num in unic:
        hexa.append("%02x" % num)
    
    return "".join(hexa)

def convertFromHex(ciphertext):
    return bytearray.fromhex(ciphertext).decode()

def generate_estring():
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

    print("what should e_string file be called?")
    filename = input("> ")

    with open(filename + ".txt", "w") as f:
        f.write(e_string)

    print("------------------------")
    print("The encyption string is ready. It has been saved as " + filename + ".txt")
    print("it lies in the working directory.")
    print(">" + e_string + "<")
    print("------------------------")

    return e_string

def encrypt_message(message, e_string, encrypt_key, key):

    ret_string = ""

    for let in message:
        if let in e_string:
            num = e_string.find(let)
            
            num = num + key

            if num >= len(encrypt_key):
                num -= len(encrypt_key)
            elif num < 0:
                num += len(encrypt_key)
            
            ret_string = ret_string + encrypt_key[num]

    if key < len(ret_string) / 2:
        ret_string = trans_cipher.encryptMessage(key, ret_string)
    else:
        ret_string = trans_cipher.encryptMessage(3, ret_string)

    ret_string = convertToHex(ret_string)

    ret_string = trans_cipher.encryptMessage(3, ret_string)

    ret_string = convertToHex(ret_string)

    print("your message has been encrypted and put in the file: ciphertext.txt")
    with open("ciphertext.txt", "w") as f:
        f.write(ret_string)

    return "encrypted message: >" + ret_string + "<"

def decrypt_message(key, message, filename):

    message = convertFromHex(message)

    message = trans_cipher_decr.decryptMessage(3, message)

    message = convertFromHex(message)

    string_file = open(filename + ".txt", "r")
    e_string = string_file.read()
    string_file.close()

    e_string = convertFromHex(e_string)

    if key < len(message) / 2:
        message = trans_cipher_decr.decryptMessage(key, message)
    else:
        message = trans_cipher_decr.decryptMessage(3, message)

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

    return ">" + ret_string + "<"

def main(mode, message, key):
    if mode == "encrypt":
        print("Do you want to use an existing e_string? y/n")
        prompt = input("> ")
        if prompt == "y":
            print("enter the name of the e_string file, excluding .txt")
            usr_ans = input("> ")
            with open(usr_ans + ".txt", "r") as f:
                e_string = f.read()
                e_string = convertFromHex(e_string)
        else:
            e_string = generate_estring()
            e_string = convertFromHex(e_string)
        encrypt_key = list(e_string)
        ciphertext = encrypt_message(message, e_string, encrypt_key, key)

        print("------------------------")
        print(ciphertext)
        print("------------------------")


    if mode == "decrypt":
        print("what is the filename of the e_string (excluding .txt)")
        filename = input("> ")
        plaintext = decrypt_message(key, message, filename)
        print("------------------------")
        print(plaintext)
        print("------------------------")

if __name__ == "__main__":
    main(myMode, myMessage, key)

