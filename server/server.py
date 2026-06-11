from os import getcwd, path, mkdir
from main import config
from datetime import datetime
from shutil import copyfileobj
from os import makedirs
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database.database_manager import DatabaseManager
from database.stats import UserStatsManager

app = FastAPI()
# configuration
templates = Jinja2Templates(directory="server/templates")
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
    if not path.exists("uploads"):
        mkdir("uploads")
    pic_path =  f"{getcwd()}/uploads/{picture.filename}"
    with open(pic_path, "wb") as buf:
        copyfileobj(picture.file, buf)

    # generate roll_no
    roll_no = f"{name.split(" ")[0]}-{datetime.today().year}-{str(datetime.today().microsecond)[:-4]}"

    #init db)
    DatabaseManager.init_db(config.DB_NAME)
    DatabaseManager.add_student(name, roll_no, email, cnic,phone, password, pic_path)

    return f"<h1>Thank You! {name}</h1> <br> <h1>Your Roll No: {roll_no}</h1>"



@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    # Dynamically locate active database file path matching state parameters
    db_file_path = f"{getcwd()}/data.db" 
    
    # Extract structural analytical metrics via Agent 1 Manager
    global_stats = UserStatsManager.get_global_metrics(db_file_path)
    merit_list = UserStatsManager.get_top_performers(db_file_path, limit=5)
    student_roster = UserStatsManager.get_all_student_records(db_file_path)
    
    # Process dynamic layout rendering through Jinja2 context injector
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request,
            "stats": global_stats,
            "merit_list": merit_list,
            "roster": student_roster
        }
    )

# ── Add this route alongside admin_dashboard ─────────────────────────────────
@app.get("/admin/student/{student_id}", response_class=HTMLResponse)
async def student_detail(request: Request, student_id: int):
    db_file_path = f"{getcwd()}/data.db"
    student = UserStatsManager.get_student_by_id(db_file_path, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse(
        "student_detail.html",
        {"request": request, "student": student}
    )