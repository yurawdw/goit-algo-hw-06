import re

# Клас для базового поля (наприклад, ім'я або телефон)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required")
        super().__init__(value)

# Клас для зберігання номера телефону
class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

# Клас для запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)  # Ім'я контакту
        self.phones = []  # Список номерів телефонів

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def delete_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        self.delete_phone(old_phone)
        self.add_phone(new_phone)

    def __str__(self):
        phone_numbers = "; ".join([str(phone) for phone in self.phones])
        return f"Contact name: {self.name}, phones: {phone_numbers}"

# Клас для адресної книги
class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name.value] = record

    def find(self, name):
        return self.contacts.get(name)

    def delete(self, name):
        if name in self.contacts:
            del self.contacts[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.contacts.values())

# Приклад використання:

# Створення адресної книги
address_book = AddressBook()

# Додавання контактів
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
address_book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
address_book.add_record(jane_record)

# Виведення всіх записів
print(address_book)

# Редагування телефону для John
john = address_book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

# Пошук та видалення Jane
address_book.delete("Jane")
print(address_book)
