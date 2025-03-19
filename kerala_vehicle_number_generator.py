import random
import os

# File paths for different categories
DB_FILES = {
    "super_elite": "super_elite.txt",
    "single_digit": "single_digit.txt",
    "others": "others.txt",
    "semi_fancy": "semi_fancy.txt",
    "existing_fancy": "existing_fancy.txt",
    "existing_numbers": "existing_numbers.txt"
}

# Prices for different categories
PRICES = {
    "super_elite": 500000,
    "single_digit": 300000,
    "others": 200000,
    "semi_fancy": 100000
}

# Fancy number categories
FANCY_NUMBERS = {
    "super_elite": ["0001"],
    "single_digit": [f"000{x}" for x in range(2, 10)],
    "others": ["0786", "1111", "7777", "9999", "1313"] + [f"{x:04}" for x in range(10, 100)],
    "semi_fancy": ["0100", "0666", "4444", "8000"]
}

def load_existing_numbers():
    existing_numbers = set()
    for file in DB_FILES.values():
        if os.path.exists(file):
            with open(file, "r") as f:
                existing_numbers.update(line.strip() for line in f)
    return existing_numbers

def generate_vehicle_number(custom_number=None):
    existing_numbers = load_existing_numbers()
    while True:
        district_code = f"KL{random.randint(1, 99):02}"
        series = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=random.randint(1, 2)))
        number = custom_number if custom_number else f"{random.randint(0, 9999):04}"
        vehicle_number = f"{district_code} {series} {number}"
        if vehicle_number not in existing_numbers:
            return vehicle_number

def save_number(filename, number):
    with open(filename, "a") as file:
        file.write(number + "\n")

def remove_number(filename, number):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            numbers = file.readlines()
        numbers = [num.strip() for num in numbers if num.strip() != number]
        with open(filename, "w") as file:
            file.writelines(num + "\n" for num in numbers)

def purchase_fancy_number():
    print("Select Fancy Number Category:")
    for i, category in enumerate(FANCY_NUMBERS.keys(), 1):
        print(f"{i}. {category.replace('_', ' ').title()}")
    print("5. Exit")
    
    choice = int(input("Enter your choice: "))
    if choice == 5:
        return
    
    category = list(FANCY_NUMBERS.keys())[choice - 1]
    
    if category == "semi_fancy":
        number = random.choice(FANCY_NUMBERS[category])
        vehicle_number = generate_vehicle_number(number)
        print(f"Generated {vehicle_number} for Rs. {PRICES[category]}")
        confirm = input("Do you wish to continue? (y/n): ").strip().lower()
        if confirm == "y":
            save_number(DB_FILES["existing_fancy"], vehicle_number)
            print("Number successfully registered!")
        else:
            print("Transaction cancelled.")
        return
    
    print("1. Choose from database")
    print("2. Generate new fancy number")
    if category != "super_elite":
        print("3. Enter a specific number")
    print("3. Exit" if category == "super_elite" else "4. Exit")
    
    sub_choice = int(input("Enter your choice: "))
    
    if (category == "super_elite" and sub_choice == 3) or sub_choice == 4:
        return
    
    if sub_choice == 2:
        number = random.choice(FANCY_NUMBERS[category])
    elif sub_choice == 3:
        number = input("Enter a specific number: ").strip()
        if category == "single_digit":
            if not number.isdigit() or int(number) < 2 or int(number) > 9:
                print("Invalid input! Single-digit numbers must be between 0002 and 0009.")
                return
            number = f"000{int(number)}"
        else:
            if number.isdigit():
                num_int = int(number)
                if num_int < 10:
                    print("Invalid input! Single-digit numbers are reserved for Single Digit category.")
                    return
                number = f"{num_int:04}"
    else:
        with open(DB_FILES[category], "r") as file:
            numbers = file.readlines()
        numbers = [num.strip() for num in numbers]
        if not numbers:
            print("No numbers available.")
            return
        
        for i, num in enumerate(numbers, 1):
            print(f"{i}. {num} - Rs. {PRICES[category]}")
        
        print("0. Exit")
        select = int(input("Select a number: "))
        if select == 0:
            return
        
        number = numbers[select - 1]
        remove_number(DB_FILES[category], number)
    
    vehicle_number = generate_vehicle_number(number)
    print(f"Generated {vehicle_number} for Rs. {PRICES[category]}")
    confirm = input("Do you wish to continue? (y/n): ").strip().lower()
    if confirm == "y":
        save_number(DB_FILES["existing_fancy"], vehicle_number)
        print("Number successfully registered!")
    else:
        save_number(DB_FILES[category], vehicle_number)
        print("Transaction cancelled. Number saved for future purchase.")

def register_random_number():
    vehicle_number = generate_vehicle_number()
    save_number(DB_FILES["existing_numbers"], vehicle_number)
    print(f"{vehicle_number} registered successfully!")

def main():
    for file in DB_FILES.values():
        if not os.path.exists(file):
            open(file, "w").close()
    
    while True:
        print("1. Purchase Fancy Number")
        print("2. Register Random Number")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            purchase_fancy_number()
        elif choice == "2":
            register_random_number()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
