from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from starlette.status import HTTP_303_SEE_OTHER
from database import SessionLocal, engine
import models
from models import Task
import schemas
import asyncio

app = FastAPI()

# Подключаем сессию для работы с flash-сообщениями
app.add_middleware(SessionMiddleware, secret_key='your_secret_key')

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/add", response_class=HTMLResponse)
async def add_task_form(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request, "task": None})

@app.post("/add", response_class=HTMLResponse)
async def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    # Используем сессию для flash-сообщений
    request.session.setdefault("messages", []).append({"type": "success", "text": "Задача добавлена!"})
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@app.get("/edit/{task_id}", response_class=HTMLResponse)
async def edit_task_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit.html", {"request": request, "task": task})

@app.post("/edit/{task_id}", response_class=HTMLResponse)
async def edit_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    is_done: str = Form(None),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = title
    task.description = description
    task.is_done = is_done == "on"
    db.commit()
    # Используем сессию для flash-сообщений
    request.session.setdefault("messages", []).append({"type": "success", "text": "Задача обновлена!"})
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@app.get("/delete/{task_id}", response_class=HTMLResponse)
async def delete_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    # Используем сессию для flash-сообщений
    request.session.setdefault("messages", []).append({"type": "danger", "text": "Задача удалена!"})
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@app.get("/toggle/{task_id}", response_class=HTMLResponse)
async def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_done = not task.is_done
    db.commit()
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

# Настройка маршрута для статических файлов
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
