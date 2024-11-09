# Birthday Planner

Birthday Planner is a command-line application written in Python that helps users manage contacts and notes efficiently.

## Features
- **Contact Management**: Add, edit, delete, and search contacts.
- **Notes Management**: Add, edit, delete, and search notes, including tags.
- **Command Suggestion**: Intelligent command suggestion based on user input.

## Installation

To install Birthday Planner, you need to have Python 3.10 or above installed. You can install the package via pip:

```sh
pip install .
```

## Usage

After installation, you can run the Birthday Planner using the command:

```sh
birthday-planner
```

## Usage example

```sh
>> add_contact John Doe; Kyiv; +380123456789; john@example.com; 1990-01-01
Контакт 'John Doe' додано.

>> search_contacts John
{'name': 'John Doe', 'address': 'Kyiv', 'phones': ['+380123456789'], 'email': 'john@example.com', 'birthday': '1990-01-01'}

>> upcoming_birthdays 30
John Doe - день народження через 15 днів

>> add_note Shopping List; Buy milk and bread; shopping,groceries
Нотатку 'Shopping List' додано.

>> search_notes bread
{'title': 'Shopping List', 'content': 'Buy milk and bread', 'tags': ['shopping', 'groceries']}

>> exit
До побачення!
```

To exit the application, type `exit`.

## Requirements

- Python 3.10+

## Author

- **Minions Co.** - [dev@minions.co](mailto:dev@minions.co)
