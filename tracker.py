from database import db

class WorkoutTracker:
   def __init__(self):
        self._exercises: list[dict] = []

   def get_exercises(self) -> list[dict]:
        return self._exercises

   async def add_exercise(self, name: str, weight: int, category: str):
      exercise = {"name": name, "weight": weight, "category": category}
      await db["exercises"].insert_one(exercise)
      exercise["_id"] = str(exercise["_id"])
      self._exercises.append(exercise)

   def summary(self) -> WorkoutSummary:
      total      = len(self._exercises)
      weights    = [ex["weight"] for ex in self._exercises]
      return WorkoutSummary(
          total      = total,
          max_weight = max(weights),
          min_weight = min(weights),
          average    = round(sum(weights) / total, 1)
      )
   def by_category(self, category: str) -> list[dict]:
      return [ex for ex in self._exercises if ex["category"] == category]

   def heaviest(self) -> dict:
       return max(self._exercises, key=lambda ex: ex["weight"])

   def _check_not_empty(self):
      if not self._exercises:
        raise HTTPException(status_code=400, detail="No exercises")

   async def  load(self) -> None:
      exercises = await db["exercises"].find({}).to_list(100)

      for exercise in exercises:
        exercise["_id"] = str(exercise["_id"])

      self._exercises = exercises