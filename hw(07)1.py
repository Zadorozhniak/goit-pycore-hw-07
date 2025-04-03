from datetime import datetime, timedelta
from collections import UserDict


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

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

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
                    if congratulation_date.weekday() == 5:  # Субота
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:  # Неділя
                        congratulation_date += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays


# Приклад використання
book = AddressBook()

record1 = Record("Maya Jonshon")
record1.add_birthday("24.03.1990")

record2 = Record("Laura McKlean")
record2.add_birthday("18.03.1995")

record3 = Record("Alivia Smith")
record3.add_birthday("23.03.1998")

book.add_record(record1)
book.add_record(record2)
book.add_record(record3)

print(book.get_upcoming_birthdays())
