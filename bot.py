from addressBook import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as error:
            # Отримуємо текст помилки
            error_message = str(error)
            
            if "not enough values to unpack" in error_message or "expected at least" in error_message:
                return "Give me name and phone please."
            
            return error_message
        except KeyError:
            # Виникає, коли ключа немає в словнику contacts
            return "Error: Contact not found."
        except IndexError:
            # Виникає, коли в args недостатньо елементів
            return "Error: Please provide the required arguments for the command."


    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
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
def change_contact(args, book: AddressBook):
    name, current_phone, new_phone, *_ = args
    record = book.find(name)
    if record is not None:
        record.edit_phone(current_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError

    return f"{name}'s phones: {' | '.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(birthday)
    return f"Birthday {birthday} has been added."
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    if record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"Birthday for {name} is not set."

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if len(upcoming) == 0:
        return "There are no upcoming birthdays."

    return "Upcoming birthdays:\n" + "\n".join(
        f"- {rec['congratulation_date']}: {rec['name']}" for rec in upcoming
    )

def show_all(book: AddressBook):
    records = "\n".join([str(record) for record in book.values()])

    if not records:
        return "The address book is empty."
    return records


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
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
            print(show_all(book))
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

