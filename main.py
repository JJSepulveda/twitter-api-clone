"""
Clon de twitter con fastapi
"""
# Fastapi
from fastapi import FastAPI

#Local packages
from paths import users, tweets

app = FastAPI()

#Includes the paths from paths folder
app.include_router(users.router)
app.include_router(tweets.router)
