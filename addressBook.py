from collections import UserDict
from datetime import datetime, timedelta

birthday_format = "%d.%m.%Y"

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self._validate(value):
            raise ValueError("Invalid phone format. It must contain exactly 10 digits.")
        super().__init__(value)
    
    def _validate(self, value):
        return value.isdigit() and len(value) == 10
    
class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, birthday_format).date())
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, current_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == current_phone:
                self.phones[index] = Phone(new_phone)
                return True
        raise ValueError(f"Phone number {current_phone} was not found.")
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {' | '.join(p.value for p in self.phones)}, "
            f"birthday: {self.birthday or 'not set'}"
        )
    def __repr__(self):
        return (
            f"Contact name: {self.name.value}, phones:\n"
            f"{''.join(f' * {p.value}\n' for p in self.phones)}"
        )
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today = datetime.now().date()
        result = []

        for username in self.data:
            record = self.data[username]

            if not record.birthday:
                continue

            user_birthday_this_year = record.birthday.value.replace(year=today.year)

            if user_birthday_this_year < today:
                user_birthday_this_year = user_birthday_this_year.replace(year = today.year + 1)

            if(0 <= (user_birthday_this_year - today).days <= 7):
                weekday = user_birthday_this_year.weekday()

                if(weekday == 5 or weekday == 6):
                    user_birthday_this_year += timedelta(days= 7 - weekday)
                
                result.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": user_birthday_this_year.strftime(
                            birthday_format
                        ),
                    }
                )
        return result
	