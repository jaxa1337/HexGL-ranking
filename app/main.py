import logging
import json
import os
import typing
from pydantic import BaseModel

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from app.utils import saved_user_score, get_scores, get_times_json, sort_scores
class UserData(BaseModel):
    nick: str
    score: int

app = FastAPI(title="HexGL")

origins = [
    "http://localhost:8000/",
    "http://localhost:8000/user_data",
    "http://localhost:8000/times",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/user_data",
    "http://127.0.0.1:8000/times"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET'],
    allow_headers=['*'],
)

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")


@app.get("/", response_class=HTMLResponse())
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/user_data")
async def get_users_data(request: Request):
    scores = get_scores()
    return JSONResponse(content=scores, status_code=200)

@app.get("/times")
async def get_times(request: Request):
    scores = get_times_json()
    logger.debug(f"{scores}")
    return JSONResponse(content=scores, status_code=200)

@app.post("/user_data")
async def post_users_data(request: Request, user_data: UserData):
    logger.debug(f"POST -> DATA: {user_data}")
    nick = user_data.nick
    score = user_data.score
    score_status = saved_user_score(nick, score)
    sort_scores()
    
    if score_status:
        return JSONResponse(content="Score saved", status_code=200)
    else:
        return JSONResponse(content="Score is lower than previos one!", status_code=409)
    
@app.delete("/user")
def delete_user(request:Request, nick: str):
    logger.debug(f"delete user -> {nick}")
    scores = {}
    with open("app/data/users_scores.json") as json_file:
        scores = json.load(json_file)
        logger.debug(f"SCORES -> {scores}")
        for nickname in scores:
            logger.debug(nickname)
            if nickname == nick:
                scores.pop(nickname)
                logger.debug(scores)
                break
    with open("app/data/users_scores.json", "w") as json_file:
        json.dump(scores, json_file, indent=4)
        return 1

    sort_scores()
