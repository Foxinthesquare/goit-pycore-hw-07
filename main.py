from datetime import datetime, timedelta
from collections import UserDict
import re

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Некоректний номер телефону. Використовуйте 10 цифр.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Phone updated."
        return "Phone not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added."

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "No birthday set."

    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
        birthday = str(self.birthday) if self.birthday else "N/A"
        return f"{self.name.value}: {phones}, Birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        result = []
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if 0 <= (next_birthday - today).days < days:
                    result.append(record)
        return result

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} added/updated."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    return f"{name}'s birthday: {record.show_birthday()}"

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([str(record) for record in upcoming])

def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0], parts[1:]

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                print(record.edit_phone(old_phone, new_phone))
            else:
                print(f"Contact {name} not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            if record:
                phones = ", ".join([str(phone) for phone in record.phones])
                print(f"{name}'s phones: {phones}")
            else:
                print(f"Contact {name} not found.")

        elif command == "all":
            for record in book.data.values():
                print(record)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
