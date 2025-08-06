from datetime import datetime

def get_greeting_and_message():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good morning", "Wishing you a bright and productive start! ☀️"
    elif 12 <= current_hour < 17:
        return "Good afternoon", "Keep pushing, the day's not over yet! 💪"
    elif 17 <= current_hour < 21:
        return "Good evening", "Time to wind down and relax. 🌇"
    else:
        return "Hello night owl! 🌙", "Burning the midnight oil, eh? Don’t forget to rest. 😴"

def main():
    name = input("What's your name? ")
    greeting, message = get_greeting_and_message()
    print(f"{greeting}, {name}! {message}")

if __name__ == "__main__":
    main()
