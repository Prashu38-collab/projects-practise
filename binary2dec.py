def binary2decimal():
    binary=input("Enter a number: ")
    decimal=0
    for i in binary:
        if i not in ("01"):
            print("Invalid numbers, please enter valid numbers either 0 or 1")
            break
        decimal=decimal*2 + int(i)
    else:
        print(f"Decimal number of binary digits {binary} is {decimal}. ")

binary2decimal()
        