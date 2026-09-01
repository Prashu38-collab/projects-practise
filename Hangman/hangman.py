import random

words = ["python", "computer", "programming", "developer"]

word = random.choice(words)

hidden_word = []

for letter in word:
    hidden_word.append("_")

lives = 6
guessed_letters = []

print(" Welcome to Hangman!")

while "_" in hidden_word and lives > 0:

    print("\nWord:", " ".join(hidden_word))
    print("Lives:", lives)
    print("Guessed letters:", ", ".join(guessed_letters))

    guess = input("Guess a letter: ").lower()

    # Check if input is valid
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one letter.")
        continue

    # Check if letter was already guessed
    if guess in guessed_letters:
        print("You already guessed that letter!")
        continue

    # Store guessed letter
    guessed_letters.append(guess)

    # Check if guess is correct
    if guess in word:
        print("Correct! ")

        for index in range(len(word)):
            if word[index] == guess:
                hidden_word[index] = guess

    else:
        lives -= 1
        print("Wrong! You lost a life. ")


# Game result
if "_" not in hidden_word:
    print("\n YOU WON!")
    print("The word was:", word)

else:
    print("\n GAME OVER!")
    print("The word was:", word)