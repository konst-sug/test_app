#utils.py
import json


def get_users():
    """Получение списка словарей с данными пользователей"""
    with open('users.json', 'r') as file:
        us_data = json.load(file)
    return us_data


def save_users(data):
    """Запись списка словарей с данными пользователей"""
    with open('users.json', 'w') as file:
        json.dump(data, file)


# для стартового добавления пользователей в тестовый проект
# def main():
#data = [
#     {'user_name': 'admin', 'user_mail': 'admin@mail.ru','user_password': 'admin', 'role': 'admin', 'status': 'active'},
#     {'user_name': 'vasya', 'user_mail': 'vasya@mail.ru','user_password': 'qwerty', 'role': 'user', 'status': 'active'}
# ]
#     save_users(data)
#     print(get_users())


# if __name__ == '__main__':
#     main()
