# Temperature Converter Program

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def main():
    while True:
        print("\n=== Temperature Converter ===")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            try:
                celsius = float(input("Enter temperature in Celsius: "))
                fahrenheit = celsius_to_fahrenheit(celsius)
                print(f"🌡️ {celsius}°C = {fahrenheit:.2f}°F")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")

        elif choice == "2":
            try:
                fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                celsius = fahrenheit_to_celsius(fahrenheit)
                print(f"🌡️ {fahrenheit}°F = {celsius:.2f}°C")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")

        elif choice == "3":
            print("👋 Exiting Temperature Converter. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice, please try again.")


if __name__ == "__main__":
    main()
