from personal_assistant.exceptions import UnknownCommandError
from difflib import get_close_matches

def parse_command(user_input):
    parts = user_input.strip().split(' ', 1)
    command = parts[0]
    args = parts[1] if len(parts) > 1 else ''
    return command, args

class CommandHandler:
    def __init__(self, contact_book, note_book):
        self.contact_book = contact_book
        self.note_book = note_book
        self.commands = {
            'add_contact': self.add_contact,
            'search_contacts': self.search_contacts,
            'edit_contact': self.edit_contact,
            'delete_contact': self.delete_contact,
            'upcoming_birthdays': self.upcoming_birthdays,
            'add_note': self.add_note,
            'search_notes': self.search_notes,
            'search_notes_by_tags': self.search_notes_by_tags,
            'edit_note': self.edit_note,
            'delete_note': self.delete_note,
            'help': self.show_help,
        }

    def handle(self, command, args):
        if command in self.commands:
            self.commands[command](args)
        else:
            suggestion = self.suggest_command(command)
            raise UnknownCommandError(f"{command}. Можливо, ви мали на увазі: {suggestion}?")

    def suggest_command(self, command):
        matches = get_close_matches(command, self.commands.keys(), n=1)
        return matches[0] if matches else 'невідома команда'

    def show_help(self, args):
        print("Доступні команди:")
        for cmd in self.commands:
            print(f" - {cmd}")

    def add_contact(self, args):
        # Логіка додавання контакту
        try:
            data = args.split(';')
            name = data[0].strip()
            address = data[1].strip() if len(data) > 1 else ''
            phones = data[2].strip().split(',') if len(data) > 2 else []
            email = data[3].strip() if len(data) > 3 else ''
            birthday = data[4].strip() if len(data) > 4 else None
            contact = Contact(name, address, phones, email, birthday)
            self.contact_book.add_contact(contact)
        except Exception as e:
            print(f"Помилка при додаванні контакту: {e}")

    def search_contacts(self, args):
        results = self.contact_book.search_contacts(args)
        if results:
            for contact in results:
                print(contact.to_dict())
        else:
            print("Контактів не знайдено.")

    def edit_contact(self, args):
        try:
            data = args.split(';')
            name = data[0].strip()
            field = data[1].strip()
            value = data[2].strip()
            self.contact_book.edit_contact(name, field, value)
        except Exception as e:
            print(f"Помилка при редагуванні контакту: {e}")

    def delete_contact(self, args):
        self.contact_book.delete_contact(args.strip())

    def upcoming_birthdays(self, args):
        try:
            days = int(args.strip())
            contacts = self.contact_book.get_upcoming_birthdays(days)
            for contact in contacts:
                print(f"{contact.name} - день народження через {contact.days_to_birthday()} днів")
        except ValueError:
            print("Будь ласка, введіть коректну кількість днів.")

    def add_note(self, args):
        try:
            data = args.split(';')
            title = data[0].strip()
            content = data[1].strip() if len(data) > 1 else ''
            tags = data[2].strip().split(',') if len(data) > 2 else []
            note = Note(title, content, tags)
            self.note_book.add_note(note)
        except Exception as e:
            print(f"Помилка при додаванні нотатки: {e}")

    def search_notes(self, args):
        results = self.note_book.search_notes(args)
        if results:
            for note in results:
                print(note.to_dict())
        else:
            print("Нотаток не знайдено.")

    def search_notes_by_tags(self, args):
        tags = args.strip().split(',')
        results = self.note_book.search_by_tags(tags)
        if results:
            for note in results:
                print(note.to_dict())
        else:
            print("Нотаток з такими тегами не знайдено.")

    def edit_note(self, args):
        try:
            data = args.split(';')
            title = data[0].strip()
            content = data[1].strip() if len(data) > 1 else None
            tags = data[2].strip().split(',') if len(data) > 2 else None
            self.note_book.edit_note(title, content, tags)
        except Exception as e:
            print(f"Помилка при редагуванні нотатки: {e}")

    def delete_note(self, args):
        self.note_book.delete_note(args.strip())
