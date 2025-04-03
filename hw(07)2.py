from datetime import datetime, timedelta
from collections import UserDict

def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Not enough arguments."
        except KeyError:
            return "Error: Contact not found."
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
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Phone updated."
        return "Phone not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday set"

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.show_birthday()
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


# Клас AddressBook
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                name = record.name.value
                birthday = record.birthday.value.replace(year=today.year)

                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)

                delta_days = (birthday - today).days

                if 0 <= delta_days <= 7:
                    congratulation_date = birthday
                    if congratulation_date.weekday() == 5:  
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:  
                        congratulation_date += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.change_phone(old_phone, new_phone)


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return f"Phones: {', '.join(p.value for p in record.phones)}"


@input_error
def show_all(args, book):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return f"Birthday of {name}: {record.show_birthday()}"


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming)


def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    return command, parts[1:]


# Основна функція роботи бота
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
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
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
