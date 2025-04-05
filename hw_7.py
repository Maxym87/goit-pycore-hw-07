from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
        
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
         if not self.is_valid_phone(value):
              raise ValueError("Номер телефону має бути 10 цифр.")
         super().__init__(value)

    def is_valid_phone(self, phone: str) -> bool:
        return len(phone) == 10 and phone.isdigit()
    
class Birthday(Field):
     def __init__(self, value):
          try:
               self.value = datetime.strptime(value, "%d.%m.%Y")
          except ValueError:
               raise ValueError('Невірний фомат дати. Має бути ДД.ММ.РРРР')
          
     def __str__(self):
          return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
            self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
            for phone in self.phones:
                if phone.value == old_phone:
                    phone.value = new_phone
                    return
            raise ValueError("Телефон не знайдений")

    
    def find_phone(self, phone:str):
            for p in self.phones:
                if p.value == phone:
                    return p.value
            
            return None
    
    def add_birthday(self, birhday: str):
        self.add_birthday = Birthday(birhday)
        
    def __str__(self):
       phones = '; '.join(p.value for p in self.phones)
       bday = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
       return f"Contact name: {self.name.value}, phones: {phones}{bday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if today <= bday <= today + timedelta(days=7):
                    upcoming.append(f"{record.name.value}: {bday.strftime('%d.%m.%Y')}")
        return upcoming
    
    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Будь ласка, введіть правильні значення."
            except IndexError:
                return "Не вистачає аргументів для команди."
            except KeyError:
                return "Контакт не знайдено."
            except Exception as e:
                return f"Сталася помилка: {e}"
        return inner



@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Команда 'add' потребує ІМ’Я та ТЕЛЕФОН.")
    name, phone, *_ = args


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Команда 'change' потребує ІМ’Я, СТАРИЙ ТЕЛЕФОН та НОВИЙ ТЕЛЕФОН.")
    name, old_phone, new_phone = args

@input_error
def show_phones(args, book: AddressBook):
    if not args:
        raise ValueError("Команда 'phone' потребує ІМ’Я контакта.")
    name = args[0]

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Команда 'add-birthday' потребує ІМ’Я та ДАТУ НАРОДЖЕННЯ.")
    name, birthday = args

@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        raise ValueError("Команда 'show-birthday' потребує ІМ’Я.")
    name = args[0]


@input_error
def birthdays(args, book: AddressBook):
    return "\n".join(book.get_upcoming_birthdays()) or "No upcoming birthdays."


def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    return command, parts[1:]


def main():
    book = AddressBook()
    print("Вас вітає бот-асистент!")

    while True:
        user_input_str = input("Введіть команду: ")
        command, args = parse_input(user_input_str)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим я можу допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()