with open('sample.txt','w') as file:
    file.write("Hello its me prashamsa learning python")

with open('sample.txt','r') as file:
    result=file.read()
    print("Content of sample.txt: ",result)