import getpass
import re

def load_weak_passwords(filename):
    """Load weak passwords from a file into a set."""
    try:
        with open(filename, 'r') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return set()

def check_password_strength(password, weak_passwords):
    """Check password strength with multi-line feedback."""
    feedback = []
    strength_points = 0
    

    if len(password) < 8:
        feedback.append("✖ Too short (minimum 8 characters required)")
    else:
        strength_points += 1
        if len(password) >= 12:
            strength_points += 1
            feedback.append("✔ Good length (12+ characters)")
    

    if password.lower() in weak_passwords:
        feedback.append("✖ Commonly used weak password")
    else:
        strength_points += 1
    

    checks = [
        (r"[A-Z]", "uppercase letter"),
        (r"[a-z]", "lowercase letter"),
        (r"[0-9]", "number"),
        (r"[!@#$%^&*(),.?\":{}|<>]", "special character")
    ]
    
    for pattern, char_type in checks:
        if not re.search(pattern, password):
            feedback.append(f"✖ Missing {char_type}")
        else:
            strength_points += 1
    

    feedback.insert(0, "--- Password Analysis ---")
    

    rating = ""
    if strength_points >= 6:
        rating = "★ ★ ★ ★ ★ STRONG PASSWORD"
    elif strength_points >= 4:
        rating = "★ ★ ★ MODERATE PASSWORD"
    else:
        rating = "★ WEAK PASSWORD"
    
    return "\n".join(feedback) + f"\n\nStrength: {rating}\n" + "-"*30

def main():
    weak_passwords = load_weak_passwords("weak-passwords.txt")
    
    print("""
    =================================
     PASSWORD STRENGTH CHECKER
    =================================
    NOTE: Password input will be hidden
          Type 'exit' to quit
    =================================
    """)
    
    while True:
        try:
            password = getpass.getpass("\nEnter password : ")
            if password.lower() == 'exit':
                print("\nExiting... Goodbye!")
                break
                
            if not password:
                print("Error: Password cannot be empty")
                continue
                
            result = check_password_strength(password, weak_passwords)
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            break
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            break

if __name__ == "__main__":
    main()
