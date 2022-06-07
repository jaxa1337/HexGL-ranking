import logging
from pydantic import BaseModel

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import saved_user_score
class UserData(BaseModel):
    nick: str
    score: float

app = FastAPI(title="HexGL")

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse())
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/user_data")
async def post_user_data(request: Request, user_data: UserData):
    logger.debug(f"POST -> DATA: {user_data}")
    nick = user_data.nick
    score = user_data.score
    score_status = saved_user_score(nick, score)
    
    if score_status:
        return JSONResponse(content="Score saved", status_code=200)
    else:
        return JSONResponse(content="Score is lower then previos one!", status_code=409)
    







