
#Python
from typing import List	
from datetime import datetime
from email import message
import pytz


#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi import Path, Body, Form


app = FastAPI()


japan_timezone = pytz.timezone('Asia/Tokyo')

users = []

class UserBase(BaseModel):
    user_id: int = Field(..., ge= 0, lt=1000000)
    nick_name: str = Field(..., min_length=1, max_length=15)
    age: int = Field(..., ge= 0, lt= 120)
    
class User(UserBase):
    last_name: str = Field(..., min_length=1, max_length=15)
    gived_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=20)

    class Config:								
        schema_extra = {
            'example' : {
                'user_id': 1,
                'nick_name': 'Pochama',
                'age': 18,
                'last_name' : 'Popo',
                'gived_name': 'Chamachama',
                'email': 'pochama@email.com',
                'password': 123456789
                }
        }
    
class UserOutput(UserBase):
    pass

class Tweet(BaseModel):
    create_date = datetime.now(japan_timezone)	                            ### No type
    text: str = Field(..., min_length=1, max_length=256)
    creator_id: int = Field(...)                                            ### Check user_id
    creator_nickname: str = Field(...)                                      ### Check nick_name

    class Config:								
        schema_extra = {
            'example' : {
                'text': 'parangaricutirimicuaro',
                'creator_id': 1,
                'creator_nickname':'Pochama',
                }
        }


'''
URL
---------------
/


/tweets
/tweets/{}
/create-tweet
/update-tweet/{}
/delete-tweet/{}


/{}
/create-user
/update-user/{}
/delete-user/{}
/users
/users/search
'''




@app.get(path= "/", status_code= status.HTTP_200_OK)
#'''home'''
async def home():
    return {'message': 'Welcome to the home page'}



@app.post(path= '/create-user', response_model = UserOutput, status_code= status.HTTP_201_CREATED) 
#'''Crear usuario'''
async def create_user(
    user_id: int = Form(...),
    nick_name: str = Form(...),
    age: int = Form(...),
    last_name: str = Form(...),
    gived_name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
    ):
    
    user = User(                                            #Checar user como nombre de objeto User
        user_id = user_id, 
        nick_name = nick_name, 
        age = age, 
        last_name = last_name, 
        gived_name = gived_name,
        email= email,
        password= password) 
    
    users.append(user)
    return user


@app.get(path= '/users', status_code= status.HTTP_200_OK)
#'''Ver todos los Usuarios'''
async def users():
    return {'message': 'Mira todos estos usuarios'}

@app.get(path= '/users/search/{user_name}}', status_code=status.HTTP_302_FOUND)
#'''Ver Usuario especifico'''
async def user_search(user_name: str= Path(..., min_length=1, max_length=15)):
    users: List[str]
    for i in users:
        if user_name == i.nick_name:
            users.append(i.user_id)
            users_id_str: str= f'->{i.user_id}\n' 
    if len(users) == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User not found')
    else:
        return_message: str = f'we have register {len(users)} users with the name: {user_name} /n their id is: {users_id_str}' 
        return return_message

@app.put(path='/update-user/{user_id}}', status_code=status.HTTP_202_ACCEPTED) 
#'''Actualizar usuario'''
async def update_user(user_id: int= Path(..., ge= 0, lt=1000000),
    nick_name: str = Form(default= 'user.nick_name'),
    age: int = Form(default= 'user.age'),
    last_name: str = Form(default= 'user.last_name'),
    gived_name: str = Form(default= 'user.gived_name'),
    email: EmailStr = Form(default= 'user.email'),
    password: str = Form(default= 'user.password')
    ):
    global users
    
    user= users.index(user_id)
    
    users[user.nick_name] = nick_name, 
    users[user.age] = age, 
    users[user.last_name] = last_name, 
    users[user.gived_name] = gived_name,
    users[user.email]= email,
    users[user.password]= password
    
    return {'message':' Datos fueron actualizados'}
    
#@app.put() 
#'''Borrar usuario'''



#@app.post() 
#'''Crear Tweet'''

#@app.get()
#'''Ver Tweet'''

#@app.put() 
#'''Modificar tweet'''

#@app.put() 
#'''Borrar tweet'''