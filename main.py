"""
Clon de twitter con fastapi
"""
# Python
from uuid import UUID
from uuid import uuid1
from datetime import date
from datetime import datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# Fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path, Form
from fastapi import HTTPException

# Internal source code
from services import FileMannager

app = FastAPI()

# CONST
USERS_JSON_FILENAME = "users.json"
TWEET_JSON_FILENAME = "tweets.json"

# Models

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


class userLogin(UserBase, PasswordMixin):
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


class Tweet(BaseModel):
	tweet_id: UUID = Field(
		...,
		example=uuid1()
	)
	content: str = Field(
		...,
		max_length=256,
		min_length=1,
		example="Contenido del tweet"
	)
	created_at: datetime = Field(dafault=datetime.now())
	updated_at: Optional[datetime] = Field(default=None)
	by: User = Field(...)

# PATH OPERATIONS

## Users

### Register a user
@app.post(
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
@app.post(
	path="/login",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Login a User",
	tags=['Users']
)
def login():
	pass

### Show all users
@app.get(
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
@app.get(
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
@app.delete(
	path="/users/{user_id}/delete",
	response_model=User,
	status_code=status.HTTP_200_OK,
	summary="Delete a user",
	tags=['Users']
)
def delete_a_user():
	pass

### Update a user
@app.patch(
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
	birth_date: Optional[date] = Form(
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
	  - user_id: UUID
	  - Request body parameter.
	    - user: User

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

## Tweets

### Show all tweets
@app.get(
	path="/",
	response_model=List[Tweet],
	status_code=status.HTTP_200_OK,
	summary="Show all tweets",
	tags=['Tweets']
)
def home():
	"""
	Show all tweets

	This path operation shows all tweets in the app

	Parameters:
	-

	Returns a json list with all tweets in the app, with the following keys.
	  - tweet_id: UUID
	  - content: str
	  - created_at: datetime
	  - updated_at: Optional[datetime]
	  - by: User
	"""
	with open(TWEET_JSON_FILENAME, "r", encoding="utf-8") as f:
		results = json.loads(f.read())
		return results

### Post a tweet
@app.post(
	path="/tweets/post",
	response_model=Tweet,
	status_code=status.HTTP_201_CREATED,
	summary="Create a Tweet",
	tags=['Tweets']
)
def post(tweet: Tweet = Body(...)):
	"""
	Post a tweet

	This path operation post a tweet in the app.

	parameters:
	  - Request body parameter.
	    - tweet: Tweet

	Returns a json with the basic tweet information:
	  - tweet_id: UUID
	  - content: str
	  - created_at: datetime
	  - updated_at: Optional[datetime]
	  - by: User
	"""
	with open(TWEET_JSON_FILENAME, "r+", encoding="utf-8") as f:
		results = f.read()
		results = json.loads(results) # string a lista (Parse)

		tweet_dict = tweet.dict() # json a diccionario (Parse)
		tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"]) # Cast
		tweet_dict["created_at"] = str(tweet_dict["created_at"]) # Cast
		
		tweet_dict["updated_at"] = str(tweet_dict["updated_at"]) # Cast

		tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"]) # Cast
		tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"]) # Cast
		
		# agrego al usuario nuevo al json que cargamos
		results.append(tweet_dict)

		f.seek(0) # nos movemos al principio del archivo
		f.write(json.dumps(results)) # lista a json y escribo

		return tweet


### Show a tweet
@app.get(
	path="/tweets/{tweet_id}",
	response_model=Tweet,
	status_code=status.HTTP_200_OK,
	summary="Show a tweet",
	tags=['Tweets']
)
def show_a_tweet(
	tweet_id: str = Field(
		..., 
		title="Tweet ID",
		description="The tweet ID"
	)
):
	"""
	Show one tweet

	This path operation shows the tweet with the tweet_id in the path parameter if exists.

	Parameters:
	  - tweet_id: UUID

	Returns the tweet that match with the user_id
	  - tweet: Tweet
	"""
	tweets = FileMannager.read_file(TWEET_JSON_FILENAME)

	for tweet in tweets:
		if tweet['tweet_id'] == tweet_id:
			return tweet

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="The tweet_id is not valid."
	)


### Delete a tweet
@app.delete(
	path="/tweets/{tweet_id}/delete",
	response_model=Tweet,
	status_code=status.HTTP_200_OK,
	summary="Delete a Tweet",
	tags=['Tweets']
)
def delete_a_tweet():
	pass

### Update a tweet
@app.put(
	path="/tweets/{tweet_id}/update",
	response_model=Tweet,
	status_code=status.HTTP_200_OK,
	summary="Update a Tweet",
	tags=['Tweets']
)
def update_a_tweet():
	pass
