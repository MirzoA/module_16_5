from fastapi import FastAPI, HTTPException, Path, Request
from pydantic import BaseModel
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
def post_user(user: User, username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username'
    , examples='Urban User')], age: int = Path(ge=18, le=120, description='Enter your age', examples='34')) -> str:
    if users:
        current_index = max(user.id for user in users) + 1
    else:
        current_index = 1
    user.id = current_index
    user.username = username
    user.age = age
    users.append(user)
    return f'User {current_index} is registered.'


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user: User, user_id: int = Path(ge=0), username: str = Path(min_length=5, max_length=20
    , description='Enter username', examples='Urban User'), age: int = Path(ge=18
    , le=120, description='Enter your age', examples='58')) -> str:
    for i in users:
        if i.id == user_id:
            try:
                i.username = username
                i.age = age
                return f'User {user_id} has been updated.'
            except IndexError:
                raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
def delete_user(user_id: int) -> str:
    for index, i in enumerate(users):
        if i.id == user_id:
            users.pop(index)
            return f'User ID {user_id} deleted'
    raise HTTPException(status_code=404, detail='User was not found.')