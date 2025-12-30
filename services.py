#services.py
import asyncio
from utils import get_users, save_users

async def change_data(cmd, username: str = '', useremail: str|None = None, 
                     userpassword: str|None = None, deluser: str|None = None):
    users_dict = get_users()
    msg = page = ''
    user_info = None
    for i, us in enumerate(users_dict):
        if us['user_mail'] == useremail:
            idx = i
            if deluser is not None and deluser != '':  # Явная проверка
                match cmd:
                    case 'user':
                        us['status'] = 'deleted'
                        save_users(users_dict)
                        msg = 'user deleted!'
                        page = 'index.html'
                        user_info = {'user_name': username, 'user_mail': useremail, 
                           'user_password': userpassword,'role': cmd }
                    case _:
                        us_removed = users_dict.pop(idx)
                        save_users(users_dict)
                        msg = 'user deleted from database!'
                        page = 'page.html'
                        user_info = {'user_name': username, 'role': cmd}
            else:
                us['user_name'] = username
                us['user_password'] = userpassword
                save_users(users_dict)
                msg = 'user data changed'
                page = 'page.html'
                user_info = {'user_name': username, 'user_mail': useremail, 
                           'user_password': userpassword, 'role': cmd}
            break 
    if not msg:  # Если пользователь не найден
        msg = 'user not found'
        page = 'error.html'
    
    return page, msg, user_info
