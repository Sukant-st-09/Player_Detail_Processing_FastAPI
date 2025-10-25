from typing import Optional
from pydantic import BaseModel,field_validator

class PlayerUpdate(BaseModel):
    Player_Name: Optional[str] = None
    Age: Optional[int] = None
    Gender: Optional[str] = None
    Sport: Optional[str] = None

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls,value):
        gen =  {"male","female","other"}
        if value.lower() not in gen:
            raise ValueError("Invalid gender")
        return value.capitalize()
    
    @field_validator("Age")
    @classmethod
    def validate_age(cls,value):
        if value<=0:
            raise ValueError("Invalid age")
        return value

class Players(BaseModel):
    id : int
    Player_Name : str
    Age : int
    Gender : str
    Sport : str

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls,value):
        gen =  {"male","female","other"}
        if value.lower() not in gen:
            raise ValueError("Invalid gender")
        return value.capitalize()
    
    @field_validator("Age")
    @classmethod
    def validate_age(cls,value):
        if value<=0:
            raise ValueError("Invalid age")
        return value