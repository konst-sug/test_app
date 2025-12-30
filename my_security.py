#my_security.py
import jwt

from datetime import datetime, timedelta
from fastapi import Form, HTTPException, Request
from utils import get_users

KEY =  'secret'
ALG = 'HS256'
EXPIRE_DELTA = 15


def mySecurity(login: str = Form(...), password: str = Form(...)):
    """Функция проверки пользователя в системе"""
    us_dict = get_users()
    for us in us_dict:
        if login == us['user_mail'] and password == us['user_password'] and us['status'] == 'active': 
            return us, us_dict
    raise HTTPException(status_code=401, detail="Access denied")


def create_access_token(data: dict):
    """Функция формирования jwt токена"""
    to_encode = data.copy()
    expire_delta = datetime.utcnow() + timedelta(minutes=EXPIRE_DELTA)
    to_encode.update({'exp': expire_delta})
    encoded = jwt.encode(to_encode, KEY, ALG)
    return encoded


def authorized(request: Request):
    """Функция проверки валидности jwt токена"""
    username = ''
    try:
        r = request.cookies.get('Authorization')
        if not r:
            raise HTTPException(status_code=401, detail="Not authorized")
        token = r.split()[1]
        payload = jwt.decode(token, KEY, ALG)
        username = payload.get('sub')
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Session expired")
    return username


def registration_check(fio: str= Form(...), email: str= Form(...), password: str= Form(...), repeat: str= Form(...)):
    """Функция проверки данных при регистрации"""
    us_dict = get_users()
    if password != repeat:
        msg = 'the passwords dont match. re-register!'
        return False, msg
    for us in us_dict:
        if email == us['user_mail'] or fio == us['user_name']:
            msg = 'the user name or email are already exists. re-register!'
            return False, msg
    return True, f'Welcome {fio}! Repeat the data entry'

