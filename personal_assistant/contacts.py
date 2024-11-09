import re
from datetime import datetime
from dateutil.parser import parse as parse_date
from personal_assistant.storage import Storage

class InvalidPhoneError(Exception):
    pass

class InvalidEmailError(Exception):
    pass

class Contact:
    def __init__(self, name, address='', phones=None, email='', birthday=None):
        self.name = name
        self.address = address
        self.phones = phones if phones else []
        self.email = email
        self.birthday = birthday

    def validate_phone(self, phone):
        pattern = r'^\+?\d{9,15}$'
        if not re.match(pattern, phone):
            raise InvalidPhoneError(f"Invalid phone number: {phone}")

    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, self.email):
            raise InvalidEmailError(f"Invalid email address: {self.email}")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            bday = datetime.strptime(self.birthday, '%Y-%m-%d')
            next_birthday = bday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'phones': self.phones,
            'email': self.email,
            'birthday': self.birthday,
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            name=data['name'],
            address=data.get('address', ''),
            phones=data.get('phones', []),
            email=data.get('email', ''),
            birthday=data.get('birthday', None),
        )

class ContactBook:
    def __init__(self):
        self.storage = Storage('contacts.json')
        self.contacts = self.load_contacts()

    def load_contacts(self):
        data = self.storage.load_data()
        return {name: Contact.from_dict(info) for name, info in data.items()}

    def save_contacts(self):
        data = {name: contact.to_dict() for name, contact in self.contacts.items()}
        self.storage.save_data(data)

    def add_contact(self, contact):
        contact.validate_email()
        for phone in contact.phones:
            contact.validate_phone(phone)
        self.contacts[contact.name] = contact
        self.save_contacts()
        print(f"Контакт '{contact.name}' додано.")

    def search_contacts(self, query):
        results = []
        for contact in self.contacts.values():
            if query.lower() in contact.name.lower():
                results.append(contact)
        return results

    def get_upcoming_birthdays(self, days):
        upcoming = []
        for contact in self.contacts.values():
            days_to_bday = contact.days_to_birthday()
            if days_to_bday is not None and days_to_bday <= days:
                upcoming.append(contact)
        return upcoming

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()
            print(f"Контакт '{name}' видалено.")
        else:
            print(f"Контакт '{name}' не знайдено.")

    def edit_contact(self, name, field, value):
        if name in self.contacts:
            contact = self.contacts[name]
            if field == 'address':
                contact.address = value
            elif field == 'email':
                contact.email = value
                contact.validate_email()
            elif field == 'birthday':
                contact.birthday = value
            elif field == 'phones':
                phones = value.split(',')
                for phone in phones:
                    contact.validate_phone(phone.strip())
                contact.phones = [phone.strip() for phone in phones]
            else:
                print(f"Невідоме поле '{field}'.")
                return
            self.save_contacts()
            print(f"Контакт '{name}' оновлено.")
        else:
            print(f"Контакт '{name}' не знайдено.")
