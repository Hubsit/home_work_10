from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass



class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, phone):
        pass


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name] = record.phones


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
    name, phone = normalize_data(data)
    record = Record(name)
    record.add_phone(phone)
    users.add_record(record)
    return f'New contact added: {name}'


@input_error
def change_phone(data: list) -> str:
    name, phone = normalize_data(data)
    users[name] = phone
    return f'New phone number {phone} for {name}'


@input_error
def search_phone(name: list) -> str:
    user_name = name[0].capitalize()
    return f'{user_name}: {users[user_name]}'


@input_error
def show_all_users() -> str:
    all_users = ''
    for name, phone in users.items():
        all_users += f'{name}: {phone} \n'
    return all_users


@input_error
def wrong_command() -> str:
    return 'Wrong command. Try again...'


@input_error
def stop_work() -> str:
    return 'Good bye!'


user_commands = {
    'hello': hello_user,
    'add': add_contact,
    'change': change_phone,
    'phone': search_phone,
    'show all': show_all_users,
    'good bye': stop_work,
    'close': stop_work,
    'exit': stop_work,
}


def command_parser(input_message: str):
    input_command = [key for key in user_commands if input_message.lower().startswith(key)]
    input_command = ''.join(input_command)
    input_data = input_message.lower().replace(input_command, '').strip().split(' ')
    if input_command in user_commands.keys() and input_data[0]:
        return user_commands.get(input_command)(input_data)
    elif input_command in user_commands.keys() and not input_data[0]:
        return user_commands.get(input_command)()
    else:
        return wrong_command()


def normalize_data(data: list) -> tuple:
    name = data[0].capitalize()
    phone = data[1]
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
    # command_parser('close')
