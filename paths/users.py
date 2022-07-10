"""
users path operations
"""
# Python
from datetime import date
from datetime import datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import EmailStr

# Fastapi
from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Path, Form
from fastapi import HTTPException

# Internal source code
from services import FileMannager

# Models
from models.user import User, UserLogin, UserRegister

# Const
DIR_PATH = "data/"
USERS_JSON_FILENAME = DIR_PATH + "users.json"


router = APIRouter()

# PATH OPERATIONS

## Users

### Register a user
@router.post(
	path="/signup",
	response_model=User,
	status_code=status.HTTP_201_CREATED,
	summary="Register a User",
	tags=['Users']
)
def signup(
	user: UserRegister = Body(...)
):
	"""
	Signup

	This path operation registers a user in the app

	parameters:
	  - Request body parameter.
	    - user: UserRegister

	Returns a json with the basic user information:
	  - user_id: UUID
	  - email: EmailStr
	  - first_name: str
	  - last_name: str
	  - birth_date: datetime
	"""
	with open(USERS_JSON_FILENAME, "r+", encoding="utf-8") as f:
		results = f.read()
		results = json.loads(results) # string a lista (Parse)

		user_dict = user.dict() # json a diccionario (Parse)
		user_dict["user_id"] = str(user_dict["user_id"]) # Cast
		user_dict["birth_date"] = str(user_dict["birth_date"]) # Cast
		# agrego al usuario nuevo al json que cargamos
		results.append(user_dict)

		f.seek(0) # nos movemos al principio del archivo
		f.write(json.dumps(results)) # lista a json y escribo

		return user

### Login a user
@router.post(
	path="/login",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Login a User",
	tags=['Users']
)
def login():
	pass

### Show all users
@router.get(
	path="/users",
	response_model=List[User],
	status_code=status.HTTP_200_OK,
	summary="Show all users",
	tags=['Users']
)
def show_all_users():
	"""
	Show all users

	This path operation shows all users in the app

	Parameters:
	-

	Returns a json list with all users in the app, with the following keys.
	  - user_id: UUID
	  - email: EmailStr
	  - first_name: str
	  - last_name: str
	  - birth_date: datetime
	"""

	with open(USERS_JSON_FILENAME, "r", encoding="utf-8") as f:
		results = json.loads(f.read())
		return results


### Show a user
@router.get(
	path="/users/{user_id}",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Show a user",
	tags=['Users']
)
def show_a_user(
	user_id: str = Path(
		..., 
		title="User ID",
		description="The user ID"
	)
):
	"""
	Show one user

	This path operation shows the user with the user_id passed in the path parameter if it exists.

	Parameters:
	  - user_id: UUID

	Returns the user that match with the user_id
	  - user: User
	"""
	users = FileMannager.read_file(USERS_JSON_FILENAME)
	# it doesn't need a cast because both are str.
	for user in users:
		if user['user_id'] == user_id:
			return user

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="The user_id is not valid."
	)

				


### Delete a user
@router.delete(
	path="/users/{user_id}/delete",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Delete a user",
	tags=['Users']
)
def delete_a_user():
	pass

### Update a user
@router.patch(
	path="/users/{user_id}/update",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Update a user",
	tags=['Users']
)
def update_a_user(
	user_id: str = Path(
		...,
		title="User id",
		description="The user UUID"
	),
	first_name: Optional[str] = Form(
		None,
		min_length=1, 
		max_length=50,
		title="Person name",
		description="This is the person name. It's between 1 and 50 characteres",
		example="Jose"
	),
	last_name: Optional[str] = Form(
		None,
		min_length=1, 
		max_length=50,
		title="Person name",
		description="This is the last name. It's between 1 and 50 characteres",
		example="Santos"
	),
	email: Optional[EmailStr] = Form(
		None,
		title="Email",
		description="This is the email",
		example="example@hotmail.com"
	),
	birth_date: Optional[datetime] = Form(
		default=None,
		title="Birth date",
		description="This is the birth date",
		example="dd/mm/yy"
	)
):
	"""
	Update a user

	This path operation update the user information

	Parameters:
	  - Path parameter:
	    - user_id: UUID
	  - Form:
	    - first_name: Optional[str]
	    - last_name: Optional[str]
	    - email: Optional[Emailstr]
	    - birth_date: Optional[date]

	Returns a json with the new user information, with the following keys.
	  - user_id: UUID
	  - email: EmailStr
	  - first_name: str
	  - last_name: str
	  - birth_date: datetime
	"""
	users = FileMannager.read_file(USERS_JSON_FILENAME)
	
	for element in users:
		if element['user_id'] == user_id:
			element['email'] = element['email'] if email is None else email
			element['first_name'] = element['first_name'] if first_name is None else first_name
			element['last_name'] = element['last_name'] if last_name is None else last_name
			element['birth_date'] = element['birth_date'] if birth_date is None else str(birth_date)

			FileMannager.write_file(USERS_JSON_FILENAME, users)
			return element
	
	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="The user_id is not valid."
	)
