#Pydantic

from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Path


app = FastAPI


class UserBase(BaseModel):
    user_id: int = Field(..., ge= 0)
    nick_name: str = Field(..., min_length=1, max_length=15)
    age: int = Field(..., ge= 0, lt= 120)
    
class User(UserBase):
    last_name: str = Field(..., min_length=1, max_length=15)
    gived_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)
    
class UserOutput(UserBase):
    pass

class Tweet(BaseModel):
    date: 

@app.get(path= '/', title= 'home', description= 'This is Tweeter s Home page', satus_code= status.HTTP_200_OK)
#'''home'''
def home():
    return {'message': 'Welcome to the home page'}



@app.post(path= '/User/create-user', title= 'Create User', description= 'API for create a user', satus_code= status.HTTP_201_CREATED) 
#'''Crear usuario'''
def create_user():
    pass



#@app.get()
#'''Ver Usuario'''

#@app.put() 
#'''Actualizar usuario'''


#@app.post() 
#'''Crear Tweet'''

#@app.get()
#'''Ver Tweet'''

#@app.put() 
#'''Modificar tweet'''
