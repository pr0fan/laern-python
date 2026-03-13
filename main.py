from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from models import WorkoutSummary, ExerciseCreate
from tracker import WorkoutTracker
from database import get_db

app = FastAPI()

async def get_tracker(db = Depends(get_db)):
    t = WorkoutTracker(database=db)
    await t.load()
    return t

@app.get("/exercises")
async def get_exercises(tracker: WorkoutTracker = Depends(get_tracker)):
    exercises = tracker.get_exercises()
    return exercises

@app.post("/exercises")
async def add_exercise(body: ExerciseCreate, tracker: WorkoutTracker = Depends(get_tracker)):
    await tracker.add_exercise(body.name, body.weight, body.category)
    return {"message": "Exercise added!"}

@app.get("/exercises/summary")
async def get_summary(tracker: WorkoutTracker = Depends(get_tracker)):
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.summary()

@app.get("/exercises/heaviest")
async def get_heaviest(tracker: WorkoutTracker = Depends(get_tracker)):
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.heaviest()

@app.get("/exercises/{category}")
async def get_by_category(category: str, tracker: WorkoutTracker = Depends(get_tracker)):
    if not tracker.get_exercises():
        raise HTTPException(status_code=400, detail="No exercises")

    return tracker.by_category(category)


@app.get("/")
async def root():
    return {"message": "Hello Python!"}