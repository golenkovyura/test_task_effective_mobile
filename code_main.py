from os import path
from typing import List, Tuple


class Contact:
    def __init__(self, last_name: str,
                 first_name: str, middle_name: str,
                 organization: str, work_phone: str, personal_phone: str):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def all_fields(self) -> Tuple[str]:
        """
        Вспомогательный метод для удобного поиска записей в
        телефонной книжке по всем полям.
        """
        return (self.last_name, self.first_name,
                self.middle_name, self.organization,
                self.work_phone, self.personal_phone)


class Phonebook:
    def __init__(self, filename: str):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self) -> None:
        """
        Метод читает данные из файла и создает объекты контактов,
        которые затем сохраняются в списке 'self.contacts'
        для дальнейшего использования.
        """
        if path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    contact = Contact(*data)
                    self.contacts.append(contact)

    def save_contacts(self) -> None:
        """Метод добавления нового контакта в записную книжку."""
        with open(self.filename, 'w') as file:
            for contact in self.contacts:
                file.write(
                    f"{contact.last_name}, {contact.first_name}, "
                    f"{contact.middle_name}, "
                    f"{contact.organization}, "
                    f"{contact.work_phone}, {contact.personal_phone}\n")

    def add_contact(self, contact: Contact) -> None:
        """Метод добвляет контакт в список 'contacts'."""
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, index: int, new_contact: Contact) -> None:
        """
        Метод, изменяющий выбранный конктакт и
        сохраняющая изменения в файле.
        """
        self.contacts[index] = new_contact
        self.save_contacts()

    def search_contacts(self, query: str) -> List[Contact]:
        """
        Поиск контактов из записной книжки по всем возможным полям.
        Возвращает список со всеми найденными контактами.
        """
        result = []
        for contact in self.contacts:
            if query in [field.lower().strip() for field in
                         contact.all_fields()]:
                result.append(contact)
        return result

    def display_contacts(self) -> None:
        """
        Метод, отображающий список всех контактов из
        телефонной книги в терминале.
        """
        if len(self.contacts) == 0:
            print('Нет записей в телефонной книге')
        for index, contact in enumerate(self.contacts):
            print(
                f"{index + 1}) {contact.last_name} {contact.first_name} "
                f"{contact.middle_name}, "
                f"{contact.organization}, {contact.work_phone}, "
                f"{contact.personal_phone}"
            )


def entering_information() -> Tuple[str]:
    """
    Вспомогательная функция для ввода информации о контакте
    в телефонной книге. Результат - кортеж со всеми полями контакта.
    """
    last_name = input("Фамилия: ")
    first_name = input("Имя: ")
    middle_name = input("Отчество: ")
    organization = input("Организация: ")
    work_phone = input("Рабочий телефон: ")
    personal_phone = input("Личный телефон: ")
    return (last_name, first_name, middle_name,
            organization, work_phone, personal_phone)


def main():
    """Основная функция для запуска программы."""
    phonebook = Phonebook("phonebook.txt")

    while True:
        print("\n1. Вывод записей\n2. Добавление записи\n"
              "3. Редактирование записи\n4. Поиск записей\n5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            phonebook.display_contacts()
        elif choice == '2':
            new_contact = Contact(*entering_information())
            phonebook.add_contact(new_contact)
        elif choice == '3':
            phonebook.display_contacts()
            index = int(input("Введите номер записи для редактирования: ")) - 1
            if 0 <= index < len(phonebook.contacts):
                new_contact = Contact(*entering_information())
                phonebook.edit_contact(index, new_contact)
            else:
                print("Неверный номер записи.")
        elif choice == '4':
            query = input("Введите строку для поиска: ").lower()
            results = phonebook.search_contacts(query)
            if results:
                print("Результаты поиска:")
                for index, contact in enumerate(results):
                    print(
                        f"{index + 1}) {contact.last_name} "
                        f"{contact.first_name} {contact.middle_name}, "
                        f"{contact.organization}, {contact.work_phone}, "
                        f"{contact.personal_phone}"
                    )
            else:
                print("Записей не найдено.")
        elif choice == '5':
            break
        else:
            print("Неверное действие.")


if __name__ == "__main__":
    main()
