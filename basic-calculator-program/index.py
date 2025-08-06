import time


def fancy_intro():
    print("="*40)
    print("🧮  Welcome to the Fancy Python Calculator  🧮")
    print("="*40)
    time.sleep(1)


def get_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Oops! That’s not a valid number. Try again.")


def get_operation():
    valid_ops = ['+', '-', '*', '/']
    while True:
        op = input("🔢 Enter operation (+, -, *, /): ").strip()
        if op in valid_ops:
            return op
        else:
            print("❌ Invalid operation. Please choose one of +, -, *, /")


def calculate(num1: float, num2: float, op: str):
    if op == '+':
        return num1 + num2, "➕"
    elif op == '-':
        return num1 - num2, "➖"
    elif op == '*':
        return num1 * num2, "✖️"
    elif op == '/':
        if num2 == 0:
            return None, "❌ Cannot divide by zero!"
        else:
            return num1 / num2, "➗"


def main():
    fancy_intro()
    while True:
        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")
        op = get_operation()

        result, symbol = calculate(num1, num2, op)

        if result is None:
            print(symbol)  # error message like divide by zero
        else:
            print(f"\n🎉 Result: {num1} {op} {num2} = {result} {symbol}")

        again = input("\n🔁 Do you want to calculate again? (y/n): ").lower()
        if again != 'y':
            print("👋 Thanks for using the Fancy Calculator. Bye!")
            break
        print("\n" + "-"*40 + "\n")


if __name__ == "__main__":
    main()
