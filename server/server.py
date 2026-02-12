import os
from main import config
from datetime import datetime
from shutil import copyfileobj
from os import makedirs
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database.database_manager import DatabaseManager

app = FastAPI()
# configuration
templates = Jinja2Templates(directory="templates")
makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@app.post("/signup", response_class=HTMLResponse)
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    cnic: str = Form(...),
    picture: UploadFile = File(...),
):
    # save pics
    pic_path =  os.getcwd() + "\\uploads\\" + picture.filename
    with open(pic_path, "wb") as buf:
        copyfileobj(picture.file, buf)

    # generate roll_no
    roll_no = f"{name}-{datetime.today().year}-{str(datetime.today().microsecond)[:-4]}"

    #init db
    DatabaseManager.init_db(f"../database/sqlite/{config.DB_NAME}")
    DatabaseManager.add_student(name, roll_no, email, cnic, password, pic_path)

    return f"<h1>Thank You! {name}</h1> <br> <h1>Your Roll No: {roll_no}</h1>"
