
#Python
from datetime import datetime
import pytz


#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Path, Body


app = FastAPI()


japan_timezone = pytz.timezone('Asia/Tokyo')

class UserBase(BaseModel):
    user_id: int = Field(..., ge= 0)
    nick_name: str = Field(..., min_length=1, max_length=15)
    age: int = Field(..., ge= 0, lt= 120)
    
class User(UserBase):
    last_name: str = Field(..., min_length=1, max_length=15)
    gived_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)

    class Config:								
        schema_extra = {
            'example' : {
                'user_id': 1,
                'nick_name': 'Pochama',
                'age': 18,
                'last_name' : 'Popo',
                'gived_name': 'Chamachama',
                'email': 'pochama@email.com'
                }
        }
    
class UserOutput(UserBase):
    pass

class Tweet(BaseModel):
    create_date = datetime.now(japan_timezone)	                            ### No type
    text: str = Field(..., min_length=1, max_length=256)
    creator_id: int = Field(...)                                   ### Check user_id
    creator_nickname: str = Field(...)                               ### Check nick_name

    class Config:								
        schema_extra = {
            'example' : {
                'text': 'parangaricutirimicuaro',
                'creator_id': 1,
                'creator_nickname':'Pochama',
                }
        }




@app.get(path= "/", status_code= status.HTTP_200_OK)
#'''home'''
async def home():
    return {'message': 'Welcome to the home page'}



@app.post(path= '/User/create-user', response_model = UserOutput, status_code= status.HTTP_201_CREATED) 
#'''Crear usuario'''
def create_user(user:User= Body(...)):
    return user


#@app.get()
#'''Ver todos los Usuarios'''

#@app.get()
#'''Ver Usuario especifico'''

#@app.put() 
#'''Actualizar usuario'''

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