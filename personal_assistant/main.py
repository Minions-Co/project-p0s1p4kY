import sys
from personal_assistant.contacts import ContactBook
from personal_assistant.notes import NoteBook
from personal_assistant.utils import parse_command, CommandHandler
from personal_assistant.exceptions import UnknownCommandError

def main():
    print("Вітаємо у Personal Assistant!")
    contact_book = ContactBook()
    note_book = NoteBook()
    handler = CommandHandler(contact_book, note_book)

    while True:
        try:
            user_input = input(">> ")
            command, args = parse_command(user_input)
            if command in ['exit', 'quit']:
                print("До побачення!")
                break
            else:
                handler.handle(command, args)
        except UnknownCommandError as e:
            print(f"Невідома команда: {e}")
        except Exception as e:
            print(f"Сталася помилка: {e}")

if __name__ == '__main__':
    main()
