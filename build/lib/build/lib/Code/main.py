from tabulate import tabulate
from termcolor import colored
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from Code.classes import *
from Code.sort import main as sort_main
import random
import random

address_book = AddressBook()
notebook = Notebook()

#Completer for commands in terminal:
sql_completer = WordCompleter([
    'hello', 'help', 'add contact', 'add phone', 'add email', 'add address',
    'change phone', 'change birthday', 'change name', 'change email',
    'change address', 'remove phone', 'remove email', 'remove address',
    'clear all', 'search by birthday', 'day to birthday', 'delete contact',
    'search', 'find phone', 'show all contacts', 'sort folder', 'create note',
    'change title', 'add tags', 'edit note', 'delete note', 'find note',
    'show all notes', 'find tags', 'sort notes', 'delete tags', 'good bye',
    'close', 'exit', '.'
], ignore_case=True)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter a correct information"
        except ValueError as ve:
            return f"ValueError: {str(ve)}"
        except IndexError:
            return "Invalid command format"
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

def hello():
    choices = ['Welcome to Your Address Book!', 'Have a good day!', 'A sprinkle of kindness today will sweeten your tomorrow.',
               "Your day is like a candy bar – full of delightful surprises!", "In the recipe of life, sweetness is the secret ingredient to your success.",
               "Life is a box of chocolates, and today, you'll find the extra special ones.",
               "Your future holds a cupcake of joy with extra frosting of love and laughter.",
               "Love you <3"]
    random_choice = random.choice(choices)
    return random_choice

def help():
    commands = [
        ("hello", "Be polite with our bot;)"),
        ("help", "See available commands and instructions."),
        ("add contact", "Add a new contact with an optional phone, email, address or birthday."),
        ("add phone", "Add an additional phone number to an existing contact."),
        ("add email", "Add an additional email to an existing contact."),
        ("add address", "Add an additional address to an existing contact."),
        ("change phone", "Change the phone number of an existing contact."),
        ("change birthday", "Change or add the birthday of an existing contact."),
        ("change name", "Change the name phone of an existing contact."),
        ("change email", "Change the email of an existing contact."),
        ("change address", "Change the address of an existing contact."),
        ("remove phone", "Remove a phone from an existing contact."),
        ("remove email", "Remove an email from an existing contact."),
        ("remove address", "Remove an address from an existing contact."),
        ("clear all", "Clear all contacts."),
        ("search by birthday", "Search contact by birthday."),
        ("day to birthday", "Show the number of days until the birthday for a contact."),
        ("delete contact", "Delete an entire contact."),
        ("search", "Search for contacts by name or phone number that match the entered string."),
        ("find phone", "Show all phone numbers for an contact."),
        ("show all contacts", "Show all existing contacts with phones, emails, addresses, birthday."),
        ("sort folder", "Sorts a folder by different types of files at the specified path."),
        ("create note", "Create a new note in the Notebook."),
        ("change title", "Change the title of an existing note."),
        ("add tags", "Adds tags to an existing note."),
        ("edit note", "Edit the content of an existing note."),
        ("delete note", "Delete an existing note."),
        ("find note", "Find notes containing the specified query in the title or body or by author."),
        ("show all notes", "Display all notes."),
        ("find tags", "Search for notes by tags."),
        ("sort notes", "Sort notes by tags in alphabetical order."),
        ("delete tags", "Remove a tag from a note."),
        ("good bye or close or exit or .", "Exit the program.")
    ]

    colored_commands = [
        (colored(command, 'cyan'), colored(description, 'green')) for command, description in commands
    ]

    table = tabulate(colored_commands, headers=["Command", "Description"], tablefmt="fancy_grid")
    print(table)
   
@input_error
def add_contact_interactive():
    name = input("Enter the contact's name: ").strip()
    record = Record(name)
    added_info = []
    while True:
        phone = input("Enter a phone number (or nothing to finish): ").strip()
        if phone.lower() == '':
            break
        try:
            record.add_phone(phone)
            added_info.append(f"Phone number: {phone}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")
    while True:
        email = input("Enter an email address (or nothing to finish): ").strip()
        if email.lower() == '':
            break
        try:
            record.add_email(email)
            added_info.append(f"Email: {email}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")
    while True:
        address = input("Enter an address (or nothing to finish): ").strip()
        if address.lower() == '':
            break
        try:
            record.add_address(address)
            added_info.append(f"Address: {address}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")
    while True:
        birthday = input("Enter the contact's birthday (or nothing if not available): ").strip()
        if birthday.lower() == '':
            break
        try:
            record.update_birthday(birthday)
            added_info.append(f"Birthday: {birthday}")
            break
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")

    address_book.add_record(record)

    return f"Contact {name} has been added : \n" + "\n".join(added_info)

@input_error
def get_phone():
    name = input("Enter the name to get phone numbers: ").strip()
    records = address_book.data.values()
    for record in records:
        if record.name.value.lower() == name.lower():
            phones_info = ', '.join(phone.value for phone in record.phones)
            if phones_info:
                return f"Phone numbers for {name}: {phones_info}"
    return f"No contact found for {name}"

@input_error
def show_all_contacts():
    records = address_book.data.values()
    if records:
        result = "All contacts:\n"
        for record in records:
            result += f"{record.name.value}:\n"
            phones_info = ', '.join(phone.value for phone in record.phones)
            if phones_info:
                result += f"  Phone numbers: {phones_info}\n"
            if record.birthday:
                result += f"  Birthday: {record.birthday}\n"
            email_info = ', '.join(email.value for email in record.emails)
            if email_info:
                result += f"  Email: {email_info}\n"
            address_info = ', '.join(address.value for address in record.addresses)
            if address_info:
                result += f"  Address: {address_info}\n"
        return result
    else:
        return "Contact list is empty"

def exit_bot():
    return "Good bye!"

@input_error
def unknown_command():
    return f"Unknown command: Type 'help' for available commands."

@input_error
def save_to_disk(filename):
    address_book.save_to_disk(filename)
    return f"Address book saved to {filename}"

@input_error
def load_from_disk(filename):
    address_book.load_from_disk(filename)
    return f"Address book loaded from {filename}"

@input_error
def search_contacts():
    query = input("Enter part of the name or phone number: ").strip()
    results = address_book.search_contacts(query)
    if results:
        result = f"Search results for '{query}':\n"
        for record in results:
            result += f"{record.name.value}:\n"
            phones_info = ', '.join(phone.value for phone in record.phones)
            if phones_info:
                result += f"  Phone numbers: {phones_info}\n"
            if record.birthday:
                result += f"  Birthday: {record.birthday}\n"
            email_info = ', '.join(email.value for email in record.emails)
            if email_info:
                result += f"  Email: {email_info}\n"
            address_info = ', '.join(address.value for address in record.addresses)
            if address_info:
                result += f"  Address: {address_info}\n"
        return result
    else:
        return(f"No results found for '{query}'.")
 
@input_error
def when_birthday():
    name = input("Enter the name to check for birthday: ").strip()
    record = address_book.find(name)
    if record:
        return f"Days until birthday for {name}: {record.days_to_birthday()} days."
    else:
        raise KeyError(f"No record found for '{name}' in the address book.")

@input_error
def update_birthday():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        new_birthday = input("Please enter the new birthday: ").strip()
        record.update_birthday(new_birthday)
        return f"Birthday for {name} updated to {new_birthday}."
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def sort_folder():
    try:
        source_folder = input("Enter the path of the folder you want to sort: ")
        if not source_folder:
            raise ValueError("Please specify the source folder.")
        sort_main(source_folder)
        return "\nThe folder is sorted \N{winking face}\nThank you for using our sorter \N{saluting face}\nHave a nice day \N{smiling face with smiling eyes}"
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "\nAn unexpected error occurred. Please check your input and try again."

@input_error
def delete_contact():
    name = input("Enter the name of the contact you want to delete: ").strip()
    try:
        address_book.delete(name)
        return f"Contact {name} deleted."
    except KeyError:
        return f"Contact {name} not found."

@input_error
def add_phone():
    name = input("Enter the name of the contact: ").strip()
    record = address_book.find(name)
    if record:
        phone = input("Enter the phone number to add: ").strip()
        phone_field = Phone(phone)
        record.add_phone(phone_field.value)
        return f"Phone {phone} added to contact {name}."
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def add_email():
    name = input("Enter the name of the contact to add email to: ").strip()
    record = address_book.find(name)
    if record:
        email = input("Enter the email to add: ").strip()
        email_field = Email(email)
        record.add_email(email_field.value)
        return f"Email {email} added to contact {name}."
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def search_contact_by_birthday():
    request = input("Enter the range for birthday search : ").strip()
    address = address_book.search_by_birthday(request)
    if len(address) == 0:
        return '\nContacts not found in this range!'
    result = ''
    for i in address:
        phones_info = ', '.join(phone.value for phone in i.phones)
        result += f"{i.name.value}:\n  Phone numbers: {phones_info}\n  Birthday: {i.birthday}\n"
    return result

@input_error
def add_address():
    name = input("Enter the name of the contact to add an address: ").strip()
    record = address_book.find(name)
    if record:
        address = input("Enter the address you want to add: ").strip()
        address_field = Address(address)
        record.add_address(address_field.value)
        return f"Address '{address}' added to contact '{name}'."
    else:
        raise KeyError(f"Contact '{name}' not found")

@input_error
def remove_phone_from_contact():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        phone = input("Please enter the phone number to remove: ").strip()
        result = record.remove_phone(phone)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def remove_email_from_contact():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        email = input("Please enter the email to remove: ").strip()
        result = record.remove_email(email)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def remove_address_from_contact():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        address = input("Please enter the address to remove: ").strip()
        result = record.remove_address(address)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def change_name():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        new_name = input("Please enter the new name: ").strip()
        new_name_field = Name(new_name)
        result = record.edit_name(new_name_field.value)
        return result
    else:
        raise KeyError(f"Contact {name} not found")
    

@input_error
def change_phone():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        old_phone = input("Please enter the old phone number: ").strip()
        new_phone = input("Please enter the new phone number: ").strip()
        new_phone_field = Phone(new_phone)
        result = record.edit_phone(old_phone, new_phone_field.value)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def change_email():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        old_email = input("Please enter the old email: ").strip()
        new_email = input("Please enter the new email: ").strip()
        new_email_field = Email(new_email)
        result = record.edit_email(old_email, new_email_field.value)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def change_address():
    name = input("Please enter the contact's name: ").strip()
    record = address_book.find(name)
    if record:
        old_address = input("Please enter the old address: ").strip()
        new_address = input("Please enter the new address: ").strip()
        new_address_field = Address(new_address)
        result = record.edit_address(old_address, new_address_field.value)
        return result
    else:
        raise KeyError

@input_error
def create_note():
    author = input("Enter the author's name: ").strip()
    title = input("Enter the note's title: ").strip()
    body = input("Enter the note's body: ").strip()    
    tags = notebook.tag_conversion(input("Enter the note's tags: ").strip())
    note = Note(author, title, body, tags)
    notebook.add_note(note)    
    return f"Note '{title}' by {author} has been added."

@input_error
def find_note():
    query = input("Enter search query for notes (author, title, or content): ").strip()
    if not query:
        return "Please provide a search query."
    results = notebook.find_notes(query)
    if results:
        result = "Found notes:\n"
        for note in results:
            result += f"Author: {note.author.value}\nTitle: {note.title.value}\nNote: {note.body}\nTags: {note.tags}\n\n"
        return result
    else:
        return "No notes found with the given query."

@input_error
def change_note_title():
    old_title = input("Enter the current title of the note: ").strip()
    new_title = input("Enter the new title for the note: ").strip()

    note = notebook.get_note(old_title)
    if note:
        notebook.delete_note(old_title)
        note.title.value = new_title
        notebook.add_note(note)
        return f"Note title changed from '{old_title}' to '{new_title}'."
    else:
        raise KeyError(f"Note '{old_title}' not found")

@input_error   
def edit_note_text():
    title = input("Enter the title of the note you want to edit: ").strip()
    note = notebook.get_note(title)
    if note:
        print(f"Current note text:\n{note.body}")
        new_body = input("Enter the new note text (or press Enter to keep the current text): ").strip()
        if new_body:
            note.edit_note(new_body)
            return f"Note '{title}' updated."
        else:
            return "Note text not changed."
    else:
        raise KeyError(f"Note '{title}' not found")

@input_error
def remove_note():
    title = input("Enter the title of the note you want to delete: ").strip()
    note = notebook.get_note(title)
    if note:
        notebook.delete_note(title)
        return f"Note '{title}' deleted."
    else:
        raise KeyError(f"Note '{title}' not found")
    
@input_error
def show_all_notes():
    notes = notebook.data.values()
    if notes:
        result = "\nAll notes:\n"
        for note in notes:
            result += f"Title: {note.title.value}\n"
            result += f"Author: {note.author.value}\n"
            result += f"Created at: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"Note: {note.body}\n"
            result += f"Tags: {note.tags}\n\n"
        return result
    else:
        return "No notes found in the address book"

@input_error
def add_tag():
    title = input("Enter the title where you want to add tags: ").strip()
    if title not in notebook.data.keys():
        raise ValueError(f"Note '{title}' not found")
    data_tags = notebook.data[title].tags
    tags = notebook.tag_conversion(input("Enter a tags: ").strip())
    tag_list = tags.split(', ')
    unique_tags = ''
    for tag in tag_list:
        if tag not in data_tags:    
            unique_tags += f'{tag}' if tag == tag_list[-1] else f'{tag}, '
    if len(unique_tags) != 0:
        notebook.add_tags(title, unique_tags)
    return 'Tags added'

def sort_notes_by_tags():
    sorted_notes = notebook.sort_notes_by_tags()
    result = "\nAll notes sorted by tags alphabetically:\n"
    for note in sorted_notes:
        result += f"\nTitle: {note.title.value}\n"
        result += f"Author: {note.author.value}\n"
        result += f"Created at: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Note: {note.body}\n"
        result += f"Tags: {note.tags}\n\n"
    return result

@input_error
def find_notes_by_tags():
    tags = input("Enter the tag by which to start searching: ").strip()
    results = notebook.find_notes_by_tags(tags)
    if not results:
        return f"No notes found with the specified tag: {tags}."
    result = f"\nHere are the notes found by tags '{tags}':\n"
    for note in results:
        result += f"\nAuthor: {note.author.value}\nTitle: {note.title.value}\nNote: {note.body}\n"
    return result
 
@input_error
def remove_tag():
    title = input("Enter the title from which you want to remove tags: ").strip()
    if title not in notebook.data.keys():
        raise ValueError(f"Note '{title}' not found")
    data_tags = notebook.data[title].tags
    tags_to_remove = notebook.tag_conversion(input("Enter tags to remove: ").strip())
    tags_to_remove_list = tags_to_remove.split(', ')
    updated_tags = [tag for tag in data_tags.split(', ') if tag not in tags_to_remove_list]
    notebook.data[title].tags = ', '.join(updated_tags)
    return 'Tags removed'

commands = {
    "hello": hello,
    "help": help,
    "add contact": add_contact_interactive,
    "add phone": add_phone,
    "add email": add_email,
    "add address": add_address,
    "change phone": change_phone,
    "change birthday": update_birthday,
    "change name": change_name,
    "change email": change_email,
    "change address": change_address,
    "remove phone": remove_phone_from_contact,
    "remove email": remove_email_from_contact,
    "remove address": remove_address_from_contact,
    "clear all": address_book.clear_all_contacts,
    "search by birthday": search_contact_by_birthday,
    "day to birthday": when_birthday,
    "delete contact": delete_contact,
    "search": search_contacts,
    "find phone": get_phone,
    "show all contacts": show_all_contacts,
    "sort folder": sort_folder,
    "create note": create_note,
    "change title": change_note_title,
    'add tags': add_tag,
    "edit note": edit_note_text,
    "delete note": remove_note,
    "find note": find_note,
    "show all notes": show_all_notes,
    "find tags": find_notes_by_tags,
    "sort notes": sort_notes_by_tags,
    "delete tags": remove_tag,
    "good bye": exit_bot,
    "close": exit_bot,
    "exit": exit_bot,
    ".": exit_bot
}

def choice_action(data, commands):
    for command in commands:
        if data.startswith(command):
            args = data[len(command):].strip()
            return commands[command], args if args else None
    return unknown_command, None

def main():
    filename = input("Enter the filename to load/create the address book: : ").strip()
    address_book.load_from_disk(filename, notebook)
    print("\nWelcome to Your Address Book!\nType 'help' to see available commands and instructions.")
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=sql_completer)
    while True:
        data = session.prompt("\nEnter command: ").lower().strip()
        func, args = choice_action(data, commands)
        result = func(args) if args else func()
        print(result)
        if result == "Good bye!":
            address_book.save_to_disk(filename, notebook)
            break

if __name__ == "__main__":
    main()
