import re
from datetime import datetime

class Phonebook:
    def __init__(self, filename="phonebook.txt"):
        self.filename = filename
        self.entries = self.load()

    def load(self):
        entries = []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(", ")
                    if len(data) >= 3:
                        name, surname, phone, birthdate = data[0], data[1], data[2], data[3] if len(data) == 4 else None
                        entries.append({"name": name, "surname": surname, "phone": phone, "birthdate": birthdate})
        except FileNotFoundError:
            pass
        return entries

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for entry in self.entries:
                birthdate = entry["birthdate"] if entry["birthdate"] else ""
                f.write(f"{entry['name']}, {entry['surname']}, {entry['phone']}, {birthdate}\n")

    def validate_phone(self, phone):
        if re.match(r'^\d{11}$', phone):
            if phone.startswith('7'):
                phone = '8' + phone[1:]
            return phone
        return None

    def validate_birthdate(self, birthdate):
        try:
            datetime.strptime(birthdate, "%d-%m-%Y")
            return birthdate
        except ValueError:
            return None

    def get_valid_phone(self):
        while True:
            phone = input("Введите номер телефона (11 цифр, без '+'): ").strip()
            phone = self.validate_phone(phone)

            if phone:
                if any(entry['phone'] == phone for entry in self.entries):
                    print("Ошибка: Этот номер уже существует в справочнике.")
                else:
                    return phone
            else:
                print("Ошибка: Номер телефона должен состоять из 11 цифр и начинаться с '7'.")

    def get_valid_birthdate(self):
        while True:
            birthdate = input("Введите дату рождения (дд-мм-гггг): ").strip()
            birthdate = birthdate.replace('.', '-')
            birthdate = self.validate_birthdate(birthdate)
            if birthdate:
                return birthdate
            else:
                print("Ошибка: Неверный формат даты. Дата должна быть в формате 'дд-мм-гггг'.")

    def add_entry(self, name, surname, phone=None, birthdate=None):
        name = name.capitalize()
        surname = surname.capitalize()

        if any(entry["name"] == name and entry["surname"] == surname for entry in self.entries):
            print(f"Запись с именем {name} и фамилией {surname} уже существует.")
            return


        if not phone:
            phone = self.get_valid_phone()

        if not birthdate:
            birthdate = self.get_valid_birthdate()

        self.entries.append({"name": name, "surname": surname, "phone": phone, "birthdate": birthdate})
        self.save()
        print("Запись добавлена.")

    def delete_entry(self, name, surname):
        name = name.capitalize()
        surname = surname.capitalize()
        entry = next((entry for entry in self.entries if entry["name"] == name and entry["surname"] == surname), None)
        if entry:
            self.entries.remove(entry)
            self.save()
            print("Запись удалена.")
        else:
            print("Запись не найдена.")

    def update_entry(self, name, surname, phone=None, birthdate=None):
        name = name.capitalize()
        surname = surname.capitalize()
        entry = next((entry for entry in self.entries if entry["name"] == name and entry["surname"] == surname), None)
        if entry:
            if phone:
                phone = self.get_valid_phone()
                entry["phone"] = phone
            if birthdate:
                birthdate = self.get_valid_birthdate()
                entry["birthdate"] = birthdate
            self.save()
            print("Запись обновлена.")
        else:
            print("Запись не найдена.")

    def search_entries(self, name=None, surname=None):
        results = [entry for entry in self.entries if
                   (not name or name.lower() in entry["name"].lower()) and
                   (not surname or surname.lower() in entry["surname"].lower())]
        return results

    def view_entries(self):
        if not self.entries:
            print("Справочник пуст.")
            return
        print(f"{'Имя':<15}{'Фамилия':<15}{'Телефон':<15}{'Дата рождения'}")
        print("-" * 60)
        for entry in self.entries:
            print(f"{entry['name']:<15}{entry['surname']:<15}{entry['phone']:<15}{entry['birthdate'] or 'не указана'}")

    def print_age(self, name, surname):
        name = name.capitalize()
        surname = surname.capitalize()
        entry = next((entry for entry in self.entries if entry["name"] == name and entry["surname"] == surname), None)
        if entry and entry["birthdate"]:
            birthdate = datetime.strptime(entry["birthdate"], "%d-%m-%Y")
            age = (datetime.now() - birthdate).days // 365
            print(f"Возраст {name} {surname}: {age} лет.")
        else:
            print("Дата рождения не указана или запись не найдена.")

def main():
    phonebook = Phonebook()

    while True:
        print("\nКоманды:")
        print("1. Просмотр всех записей")
        print("2. Добавить новую запись")
        print("3. Удалить запись")
        print("4. Изменить запись")
        print("5. Поиск записи")
        print("6. Вывести возраст")
        print("7. Выйти")

        command = input("Введите команду: ").strip().lower()

        if command == "1":
            phonebook.view_entries()
        elif command == "2":
            name = input("Введите имя: ").strip()
            surname = input("Введите фамилию: ").strip()
            phone = phonebook.get_valid_phone()
            birthdate = phonebook.get_valid_birthdate()
            phonebook.add_entry(name, surname, phone, birthdate)
        elif command == "3":
            name = input("Введите имя: ").strip()
            surname = input("Введите фамилию: ").strip()
            phonebook.delete_entry(name, surname)
        elif command == "4":
            name = input("Введите имя: ").strip()
            surname = input("Введите фамилию: ").strip()
            phone = input("Введите новый номер телефона (или оставить пустым): ").strip() or None
            birthdate = input("Введите новую дату рождения (дд-мм-гггг) (или оставить пустым): ").strip() or None
            if phone:
                phone = phonebook.get_valid_phone()
            if birthdate:
                birthdate = phonebook.get_valid_birthdate()
            phonebook.update_entry(name, surname, phone, birthdate)
        elif command == "5":
            name = input("Введите имя для поиска (или оставить пустым): ").strip()
            surname = input("Введите фамилию для поиска (или оставить пустым): ").strip()
            results = phonebook.search_entries(name, surname)
            if results:
                print(f"{'Имя':<15}{'Фамилия':<15}{'Телефон':<15}{'Дата рождения'}")
                print("-" * 60)
                for entry in results:
                    print(
                        f"{entry['name']:<15}{entry['surname']:<15}{entry['phone']:<15}{entry['birthdate'] or 'не указана'}")
            else:
                print("Записи не найдены.")
        elif command == "6":
            name = input("Введите имя: ").strip()
            surname = input("Введите фамилию: ").strip()
            phonebook.print_age(name, surname)
        elif command == "7":
            print("Выход из программы...")
            break
        else:
            print("Неизвестная команда, попробуйте снова.")

main()
