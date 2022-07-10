"""
Tweets models
"""
# Python
from uuid import UUID
from uuid import uuid1
from datetime import date
from datetime import datetime
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Models
from models.user import User


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
