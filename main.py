from collections import UserDict
import re


# Класи для роботи з винятками
class PhoneNumberError(Exception):
    pass


class NameError(Exception):
    pass


class Field:
    # Базовий клас
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Клас для зберігання імені контакту. Обов'язкове поле.
    def __init__(self, value: str) -> None:
        if not value:
            raise NameError("Name is required")
        super().__init__(value)


class Phone(Field):
    # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value: str) -> None:
        if not self.__validate(value):
            raise PhoneNumberError(
                "Invalid phone number. It should be 10 digits.")
        super().__init__(value)

    @staticmethod
    def __validate(value) -> bool:
        # Перевірка формату телефону (10 цифр)
        return bool(re.match(r'^\d{10}$', value))


class Record:
    # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name: str) -> None:
        self.name = Name(name)  # Ім'я контактної особи (обов'язкове)
        self.phones = []

    def add_phone(self, phone_number: str) -> None:
        # Додавання телефону
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        # Видалення телефону за номером
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # Редагування телефону
        if self.find_phone(old_phone) and Phone(new_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def find_phone(self, phone_number) -> str | None:
        # Пошук телефону
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        raise ValueError(f"Error: phone number '{phone_number}' not found.")

    def __str__(self):
        phone_numbers = "; ".join([str(phone) for phone in self.phones])
        return f"Contact name: {self.name}, phones: {phone_numbers}"


class AddressBook(UserDict):
    # Клас для зберігання та управління записами.
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name) -> str:
        # Пошук запису за ім'ям
        return self.data.get(name)

    def delete(self, name) -> None:
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_phone("0504567890")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі

    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(book)
