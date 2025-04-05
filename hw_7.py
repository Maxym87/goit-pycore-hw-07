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
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]


if __name__ == '__main__':
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    
    book.add_record(john_record)

    
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    
    for name, record in book.data.items():
        print(record)

    
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    
    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value}: {found_phone}")

    
    book.delete("Jane")

    
    print("Після видалення Jane:")
    for name, record in book.data.items():
        print(record)