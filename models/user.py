"""
User models.
"""
# Python
from uuid import UUID
from uuid import uuid1
from datetime import date
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserBase(BaseModel):
	user_id: UUID = Field(
		...,
		example=uuid1()
	) # universal unique identifier
	email: EmailStr = Field(...)


class PasswordMixin(BaseModel):
	password: str = Field(
		...,
		min_length=8,
		max_length=64
	)


class UserLogin(UserBase, PasswordMixin):
	pass


class User(UserBase):
	first_name: str = Field(
		...,
		min_length=1,
		max_length=50,
		example="Paimon"
	)
	last_name: str = Field(
		...,
		min_length=1,
		max_length=50,
		example='iv'
	)
	birth_date: Optional[date] = Field(default=None)


class UserRegister(User, PasswordMixin):
	pass
