#app.py
from jinja2 import Template
from fastapi import Depends, Request, Response, FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from my_security import mySecurity, create_access_token, authorized, registration_check
from services import change_data
from utils import get_users, save_users

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

users_json = 'users.json'
users_dict = []


@app.on_event("startup")
def connect_to_fake_db():
    app.state.users = get_users()
    users_dict = get_users()


@app.get('/', response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/login')
async def user_page(request: Request, response: Response, login: str=Form(...), password: str = Form(...), 
                    auth_check=Depends(mySecurity)):
    user_info, users_dict = auth_check
    username = user_info['user_name']
    acc_token = create_access_token({"sub": username})
    response = templates.TemplateResponse('page.html', {'request': request, 'user': user_info, 'data': users_dict})
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {acc_token}",
        path="/",       
        domain=None,    
        secure=False,   
        httponly=True,  
        samesite="lax"  
    )
    return response


@app.get('/reg', response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse('reg.html', {'request': request})


@app.post('/logout', response_class=HTMLResponse)
async def logout_user(request: Request):
    response = templates.TemplateResponse('index.html', {'request': request})
    response.delete_cookie(key="Authorization")
    return response


@app.post('/add', response_class=HTMLResponse)
async def add_user(request: Request, newuser: str=Form(...), newmail: str=Form(...), newpassword: str = Form(...), 
                   session_check = Depends(authorized)):
    element = {"user_name": newuser, 'user_mail': newmail, 'user_password': newpassword, 'role': 'user', 'status': 'active'}
    users_dict = get_users()
    users_dict.append(element)
    save_users(users_dict)
    users_dict = get_users()
    user_info = {'user_name': session_check, 'role': 'admin'}
    return templates.TemplateResponse('page.html', {'request': request, 'user': user_info, 'data': users_dict})


@app.get('/protect', response_class=HTMLResponse)
async def protect_page(request: Request, session_check = Depends(authorized)):
    username = session_check
    users_dict = get_users()
    for us in users_dict:
        if username == us['user_name']:
            role = us['role']
            break
    if role == 'admin':
        user_info =  {'user_name': username, 'role': role}
        response = templates.TemplateResponse('protect.html', {'request': request, 'user': user_info})
        return response
    else:
        msg = 'Access denied. Error 401. Protected resource'
        response = templates.TemplateResponse('error.html', {'request': request, 'message': msg})
        return response


@app.post('/reg', response_class=HTMLResponse)
async def reg_new_user(request: Request, fio: str=Form(...), email: str=Form(...), password: str=Form(...), 
                       repeat: str=Form(...), reg_check = Depends(registration_check)):
    res, msg = reg_check
    if res:
        element = {"user_name": fio, 'user_mail': email, 'user_password': password, 'role': 'user', 'status': 'active'}
        users_dict = get_users()
        users_dict.append(element)
        save_users(users_dict)
    response = templates.TemplateResponse('index.html', {'request': request, 'message': msg})
    return response


@app.post('/change', response_class=HTMLResponse)
async def users_change_data(request: Request, username: str=Form(...), useremail: str=Form(...), userpassword: str|None=Form(None), 
                       deluser: str|None = Form(None)):
    users_dict = get_users()
    try:
       page, msg, users_dict = await change_data('user', username, useremail, userpassword, deluser )
       user_info = {'user_name': username, 'user_mail': useremail, 'user_password': userpassword, 'role': 'user'}
       response = templates.TemplateResponse(page, {'request': request, 'user': user_info,'message': msg})
    except Exception as error:
        print(str(error))
        msg = 'Error on del user from user page.'
        response = templates.TemplateResponse('error.html', {'request': request, 'message': msg})
    return response

            
@app.post('/adminchange', response_class=HTMLResponse)
async def users_change_data(request: Request, username: str=Form(...), useremail: str|None=Form(None), userpassword: str|None=Form(None), 
                       deluser: str|None = Form(None),session_check = Depends(authorized)):
    session_name = session_check
    try:
        page, msg, _ = await change_data('admin', username, useremail, userpassword, deluser )
        user_info = {'user_name': session_name, 'role': 'admin'}
        users_dict = get_users()
        response = templates.TemplateResponse(page, {'request': request, 'user': user_info, 'data': users_dict, 'message': msg})
    except Exception as error:
        print(str(error))
        msg = 'Error on del user from admin page.'
        response = templates.TemplateResponse('error.html', {'request': request, 'message': msg})
    return response


@app.get('/work', response_class=HTMLResponse)
async def work_page(request: Request, session_check = Depends(authorized)):
    username = session_check
    try:
        user_info =  {'user_name': username}
        response = templates.TemplateResponse('work.html', {'request': request, 'user': user_info})
        return response
    except Exception as error:
        print(str(error))
        msg = 'Error on work page.'
        response = templates.TemplateResponse('error.html', {'request': request, 'message': msg})
        return response


@app.get('/info', response_class=HTMLResponse)
async def info_page(request: Request, session_check = Depends(authorized)):
    username = session_check
    try:
        user_info =  {'user_name': username}
        response = templates.TemplateResponse('info.html', {'request': request, 'user': user_info})
        return response
    except Exception as error:
        print(str(error))
        msg = 'Error on info page.'
        response = templates.TemplateResponse('error.html', {'request': request, 'message': msg})
        return response