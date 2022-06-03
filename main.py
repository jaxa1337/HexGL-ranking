from pathlib import Path
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="HexGL")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse())
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})