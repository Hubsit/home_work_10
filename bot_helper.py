from classes import AddressBook, Record


users = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parameters, please try again.'

    return inner


@input_error
def hello_user() -> str:
    return 'How can I help you?'


@input_error
def add_contact(data: list) -> str:
    name, phones = normalize_data(data)
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    users.add_record(record)
    return f'New contact added: {name}'


@input_error
def change_phone(data: list) -> str:
    name, phones = normalize_data(data)
    record = users[name]
    record.edit_phones(phones)
    return f'New phone number for {name}'


@input_error
def search_phone(name: list) -> str:
    user_name = name[0].capitalize()
    return f'{user_name}: {users[user_name]}'


@input_error
def show_all_users() -> str:
    all_users = ''
    for name, phones in users.get_all_record().items():
        all_users += f'{phones.get_info()} \n'
    return all_users


@input_error
def wrong_command() -> str:
    return 'Wrong command. Try again...'


@input_error
def stop_work() -> str:
    return 'Good bye!'


@input_error
def delete_user(data):
    name, phones = normalize_data(data)
    users.remove_record(name)
    return f'You deleted the contact: {name}'


@input_error
def delete_phone(data):
    name, phone = normalize_data(data)
    print(phone)
    record = users[name]
    if record.delete_phone(phone[0]):
        return f'Phone {phone[0]} for {name} contact deleted.'
    return f'{name} contact does not have this number'


user_commands = {
    'hello': hello_user,
    'add': add_contact,
    'change': change_phone,
    'phone': search_phone,
    'show all': show_all_users,
    'good bye': stop_work,
    'close': stop_work,
    'exit': stop_work,
    'delete phone': delete_phone,
    'delete': delete_user
}


def command_parser(input_message: str):
    for key in user_commands:
        if input_message.lower().startswith(key):
            input_command = key
            break
    input_data = input_message.lower().replace(input_command, '').strip().split(' ')
    if input_command in user_commands.keys() and input_data[0]:
        return user_commands.get(input_command)(input_data)
    elif input_command in user_commands.keys() and not input_data[0]:
        return user_commands.get(input_command)()
    else:
        return wrong_command()


def normalize_data(data: list) -> tuple:
    name = data[0].capitalize()
    phone = data[1:]
    return name, phone


def main():
    while True:
        user_input = input('Enter command: ')
        output_message = command_parser(user_input)
        print(output_message)
        if output_message == 'Good bye!':
            break


if __name__ == '__main__':
    main()

