
class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 5
        self.energy = 5
        self.happiness = 5

    def show_status(self):
      
        print("Name:", self.name)
        print("Hunger:", self.hunger, "/ 10")
        print("Energy:", self.energy, "/ 10")
        print("Happiness:", self.happiness, "/ 10")

    def feed(self):
        if self.hunger > 0:
            self.hunger -= 2
            self.hunger = max(0, self.hunger)
            print(f"\nYou fed {self.name}. Yum!")
        else:
            print(f"\n{self.name} is not hungry!")

    def sleep(self):
        if self.energy < 10:
            self.energy += 3
            self.energy = min(10, self.energy)
            print(f"\n{self.name} had a nice nap!")
        else:
            print(f"\n{self.name} is already full of energy!")

    def play(self):
        if self.energy >= 2:
            self.energy -= 2
            self.happiness += 2
            self.happiness = min(10, self.happiness)
            self.hunger += 1
            self.hunger = min(10, self.hunger)
            print(f"\nYou played with {self.name}. So much fun!")
        else:
            print(f"\n{self.name} is too tired to play. Let it sleep!")

    def check_mood(self):
        if self.happiness >= 8:
            print(f"\n{self.name} is very happy! ")
        elif self.happiness >= 4:
            print(f"\n{self.name} is feeling okay. ")
        else:
            print(f"\n{self.name} is sad. Spend some time together! 😿")


def main():
    name = input("What is your pet's name? ")
    pet = Pet(name)

    print(f"\nWelcome! You adopted {pet.name}! ")

    while True:
       
        print("1. Feed your pet")
        print("2. Let your pet sleep")
        print("3. Play with your pet")
        print("4. Check pet status")
        print("5. Check pet mood")
        print("6. Exit")

        choice = input("Choose an option 1 to 6: ")

        if choice == "1":
            pet.feed()
        elif choice == "2":
            pet.sleep()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            pet.show_status()
        elif choice == "5":
            pet.check_mood()
        elif choice == "6":
            print(f"\nGoodbye! Take care of {pet.name}! ")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
