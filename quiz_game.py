print("Hello ! welcome to prashamsa's world!!")

playing_quiz=input("Do you want to play a quiz? ")

if playing_quiz!="yes":
    quit()
else:
    print("Lets play the game :) ")
count=0
answer =input("What is the capital city of Nepal? ")
if answer=="Kathmandu".lower().strip():
    print("Correct ! ")
    count+=1
else:
    print("Try Again!!! ")

answer=input("Who is the prime minister of nepal? ")
if answer =="balen shah".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")

answer=int(input("what is the result of 35 * 35? "))
if answer==1225:
    print("Correct!")
    count+=1
else:
    print("Try again ")

answer=int(input("what is the result of 45 * 45? "))
if answer==2025:
    print("Correct!")
    count+=1
else:
    print("Try again ")


answer=input("what does RAM stands for ? ")
if answer =="Random Access Memory ".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")


answer=input("what does Gpu stands for ? ")
if answer =="Graphical Processing Unit ".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")

answer=input("What is the capital of china? ")
if answer =="Beijing".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")


answer=input("what does Wifi stands for ? ")
if answer =="Wireless Feidility ".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")

answer=input("Which planet is also known as morning star ? ")
if answer =="Venus".lower().strip():
    print("Correct!!")
    count+=1
else:
    print("Try again ")

print(f"you got {str(count) }answers correct ! ")


      



 
    


