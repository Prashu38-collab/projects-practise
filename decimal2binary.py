def decimaltobinary():
    decimal=int(input("Enter a number: "))
    if decimal==0:
        print("Binary: 0")
        return 
    binary=""
    while decimal >0:
        remainder=decimal%2
        binary=str(remainder) +binary
        decimal=decimal//2
    print("Binary: ", binary)
decimaltobinary()
   

    