import string

def check_password(password):

    score = 0
    feedback = []

    # Check minimum length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check uppercase
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Check lowercase
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Check digit
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    # Check special character
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
    }


def display_result(result):
    

    
    print("PASSWORD STRENGTH RESULT")
   

    print(f"Score: {result['score']}/5")
    print(f"Strength: {result['strength']}")

    if result["feedback"]:
        print("\nSuggestions:")
        for item in result["feedback"]:
            print(f"- {item}")
    else:
        print("\n✓ Great! Your password meets all requirements.")

  


def main():
    
    password = input("Enter a password: ")

    result = check_password(password)
    display_result(result)


if __name__ == "__main__":
    main()