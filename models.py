from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class WorkoutSummary:
    total: int
    max_weight: int
    min_weight: int
    average: float

class ExerciseCreate(BaseModel):
    name: str
    weight: int
    category: str