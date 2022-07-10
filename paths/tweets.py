"""
Tweets path operations
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
from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Path, Form
from fastapi import HTTPException

# Models
from models.tweet import Tweet

# Internal source code
from services import FileMannager

# Const
DIR_PATH = "data/"
TWEET_JSON_FILENAME = DIR_PATH + "tweets.json"


router = APIRouter()

# PATH OPERATIONS

## Tweets

### Show all tweets
@router.get(
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
@router.post(
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
@router.get(
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
@router.delete(
	path="/tweets/{tweet_id}/delete",
	response_model=Tweet,
	status_code=status.HTTP_200_OK,
	summary="Delete a Tweet",
	tags=['Tweets']
)
def delete_a_tweet():
	pass

### Update a tweet
@router.patch(
	path="/tweets/{tweet_id}/update",
	response_model=Tweet,
	status_code=status.HTTP_200_OK,
	summary="Update a Tweet",
	tags=['Tweets']
)
def update_a_tweet(
	tweet_id: str = Path(
		...,
		title="Tweet id",
		description="The tweet UUID"
	),
	content: str = Form(
		...,
		min_length=1, 
		max_length=150,
		title="Tweet content",
		description="This is the person name. It's between 1 and 50 characteres",
		example="Jose"
	),
):
	"""
	Update a tweet

	This path operation update the tweet content

	Parameters:
 	  - Path parameter:
	    - tweet_id: UUID
	  - Form:
	    - content: Optional[str]

	Returns a json with the basic tweet information:
	  - tweet_id: UUID
	  - content: str
	  - created_at: datetime
	  - updated_at: datetime
	  - by: User
	"""
	tweets = FileMannager.read_file(TWEET_JSON_FILENAME)
	
	for element in tweets:
		if element['tweet_id'] == tweet_id:
			element['content'] = content
			element['updated_at'] = str(datetime.now())

			FileMannager.write_file(TWEET_JSON_FILENAME, tweets)
			return element
	
	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="The user_id is not valid."
	)
