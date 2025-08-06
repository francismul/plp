def calculate_discount(price, discount_percent):
    if discount_percent >= 20:
        discount_amount = price * (discount_percent / 100)
        return price - discount_amount
    else:
        return price


def main():
    try:
        price = float(input("Enter the original price of the item: "))
        discount_percent = float(input("Enter the discount percentage: "))

        final_price = calculate_discount(price, discount_percent)

        if final_price < price:
            print(f"Discount applied! Final price: ${final_price:.2f}")
        else:
            print(f"No discount applied. Final price remains: ${price:.2f}")

    except ValueError:
        print("Invalid input! Please enter numeric values for price and discount.")


if __name__ == "__main__":
    main()
