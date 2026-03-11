from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from models import WorkoutSummary, ExerciseCreate
from tracker import WorkoutTracker

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
       await tracker.load()
    except FileNotFoundError:
        pass 
    yield

app = FastAPI(lifespan=lifespan)
tracker = WorkoutTracker()

@app.get("/exercises")
async def get_exercises():
    exercises = tracker.get_exercises()
    return exercises

@app.post("/exercises")
async def add_exercise(body: ExerciseCreate):
    await tracker.add_exercise(body.name, body.weight, body.category)
    return {"message": "Exercise added!"}

@app.get("/exercises/summary")
async def get_summary():
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.summary()

@app.get("/exercises/heaviest")
async def get_heaviest():
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.heaviest()

@app.get("/exercises/{category}")
async def get_by_category(category: str):
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.by_category(category)


@app.get("/")
async def root():
    return {"message": "Hello Python!"}