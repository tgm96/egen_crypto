
import math

def main():
    myMessage = "662d6c632f484978423425424395d2d476d32d4c52684c312f343f"
    myKey = 3

    plaintext = decryptMessage(myKey, myMessage)

    print(plaintext + "|")

def decryptMessage(key, message):

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

if __name__ == "__main__":
    main()
