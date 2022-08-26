

#--------------------------------------------------------------------------------------------------------
#Importaciones
#--------------------------------------------------------------------------------------------------------

#Python
from typing import List, Dict	
from uuid import UUID
from datetime import datetime, date
import pytz


#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi import Path, Body, Form


app = FastAPI()

japan_timezone = pytz.timezone('Asia/Tokyo')

tweeter_users = []

#--------------------------------------------------------------------------------------------------------
#Models
#--------------------------------------------------------------------------------------------------------

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    nick_name: str = Field(..., min_length=1, max_length=15)
#    birth_date: date = Field(...)
#    age: int = Field(..., ge= 0, lt= 120)
    last_name: str = Field(..., min_length=1, max_length=15)
    gived_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)  
      
class User(UserBase):
    password: str = Field(..., min_length=8, max_length=20)
    class Config:								
        schema_extra = {
            'example' : {
                'user_id': 1,
                'nick_name': 'Pochama',
                'birth_date': '2022-01-01',
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
    tweet_id: UUID = Field(...)
    text: str = Field(..., min_length=1, max_length=256)
    create_date: date = Field(default= datetime.now(japan_timezone))	                          
    update_date: date = Field(None)
    
    creator: UserOutput = Field(...)                                            ### Check user_id
    class Config:								
        schema_extra = {
            'example' : {
                'text': 'parangaricutirimicuaro',
                'creator_id': 1,
                'creator_nickname':'Pochama',
                }
        }




#--------------------------------------------------------------------------------------------------------
#Models creation trial
#--------------------------------------------------------------------------------------------------------

try_user1= User(
    user_id= 1,
    nick_name='Pochama1',
#    birth_date = 
#    age= 18,
    last_name= 'Popo1',
    gived_name= 'Chamachama1',
    email= 'pochama1@email.com',
    password= 123456789)

try_user2= User(
    user_id= 2,
    nick_name='Pochama2',
#    birth_date = 
#    age= 28,
    last_name= 'Popo2',
    gived_name= 'Chamachama2',
    email= 'pochama2@email.com',
    password= 123456789)
try_user3= User(
    user_id= 3,
    nick_name='Pochama3',
#    birth_date = 
#    age= 38,
    last_name= 'Popo3',
    gived_name= 'Chamachama3',
    email= 'pochama3@email.com',
    password= 123456789)
try_user4= User(
    user_id= 4,
    nick_name='Pochama4',
#    birth_date = 
#    age= 48,
    last_name= 'Popo4',
    gived_name= 'Chamachama4',
    email= 'pochama4@email.com',
    password= 123456789)
try_user5= User(
    user_id= 5,
    nick_name='Pochama5',
#    birth_date = 
#    age= 58,
    last_name= 'Popo5',
    gived_name= 'Chamachama5',
    email= 'pochama5@email.com',
    password= 123456789)
                
tweeter_users.append(try_user1)
tweeter_users.append(try_user2)
tweeter_users.append(try_user3)
tweeter_users.append(try_user4)
tweeter_users.append(try_user5)



#--------------------------------------------------------------------------------------------------------
#paths
#--------------------------------------------------------------------------------------------------------



#home
@app.get(path= "/", status_code= status.HTTP_200_OK)
async def home():
    return 'Welcome to the home page'


#Crear usuario
@app.post(path= '/create-user', response_model = UserOutput, status_code= status.HTTP_201_CREATED) 
async def create_user(
    user_id: UUID = Form(...),
    nick_name: str = Form(...),
#    birth_date: date = Form(...)
#    age: int = Form(...),
    last_name: str = Form(...),
    gived_name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
    ):
    
    user = User(                                            #Checar user como nombre de objeto User
        user_id = user_id, 
        nick_name = nick_name,
#        birth_date = birth_date,
#        age = age, 
        last_name = last_name, 
        gived_name = gived_name,
        email= email,
        password= password) 
    
    tweeter_users.append(user)
    return user


#Ver todos los Usuarios                                                  XXXX
@app.get(path= '/users', status_code= status.HTTP_200_OK)
async def users():
#    global tweeter_users
#    all_users: List[str]
#    for i in tweeter_users:
#        users_nickname: str= i.nick_name
#        all_users.append(users_nickname)
#    return all_users
    all_users: Dict[str,str] = {'a':'a'}
#    for i in tweeter_users:
#        all_users.update({i : i.nick_name})
    return all_users   #    return {'msg':'all_users'}


#Ver Usuario especifico                                                   xxx
@app.get(path= '/users/search/{user_name}}', status_code=status.HTTP_302_FOUND)
async def user_search(user_name: str= Path(..., min_length=1, max_length=15)):
    users: List[str]
    for i in tweeter_users:
        if user_name == i.nick_name:
            users.append(str(i.user_id))
            users_id_str: str = f'->{str(i.user_id)}\n'
            all_users_id_str: str =  all_users_id_str + users_id_str 
    if len(users) == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'User not found')
    else:
        return_message: str = f'we have register {len(users)} users with the name: {user_name} /n their id is: {all_users_id_str}' 
        return return_message


#Actualizar usuario                                                       xxxx
@app.put(path='/update-user/{user_id}}', status_code=status.HTTP_202_ACCEPTED) 
async def update_user(
    user_id: UUID = Path(...),
    nick_name: str = Form(...),                              #Quiero que como datos default entren los datos ya creados previamente por el usuario  
#    birth_date: date = Form(...)
#    age: int = Form(...),                                         
    last_name: str = Form(...),                              
    gived_name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
    ):
    global tweeter_users 
    
    for i in tweeter_users:
        if user_id == i.user_id:
            user_index= tweeter_users.index(i)
    user= tweeter_users[user_index]
    
    user.nick_name = nick_name, 
    user.age = age, 
    user.last_name = last_name, 
    user.gived_name = gived_name,
    user.email= email,
    user.password= password
    
    tweeter_users[user_index] = user
    
    return user


#Borrar usuario    
#@app.delete(path='/delete-user/{user_id}}', status_code=status.HTTP_202_ACCEPTED) 
#async def delete_user():
#    pass




'''
/{}
/create-user
/update-user/{}
/delete-user/{}
/users
/users/search
'''


#Crear Tweet
#@app.post(path='/create_tweet') 

#Ver Tweet
#@app.get(path='/tweet/{tweet_id}')

#Modificar tweet
#@app.put(path='/tweet/{tweet_id}'/update) 


#Borrar tweet
#@app.put(path='/tweet/{tweet_id}'/delete) 


