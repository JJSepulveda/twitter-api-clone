"""
Clon de twitter con fastapi
"""
# Python
from uuid import UUID
from datetime import date
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# Fastapi
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

# Models

class UserBase(BaseModel):
	user_id: UUID = Field(...) # universal unique identifier
	email: EmailStr = Field(...)


class userLogin(UserBase):
	password: str = Field(
		...,
		min_length=8,
		max_length=64
	)


class User(UserBase):
	first_name: str = Field(
		...,
		min_length=1,
		max_length=50
	)
	last_name: str = Field(
		...,
		min_length=1,
		max_length=50
	)
	birth_date: Optional[date] = Field(default=None)


class Tweet(BaseModel):
	pass


@app.get(
	path="/", 
	status_code=status.HTTP_200_OK
)
def home():
	return {"Twitter API": "Working!"}
