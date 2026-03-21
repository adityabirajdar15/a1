from fastapi import FastAPI
from pydantic import BaseModel
from database import users_collection, workouts_collection, diet_collection
from llm import generate_plan

app = FastAPI()


# ----------------------------
# DATA MODELS
# ----------------------------

class Goal(BaseModel):
    name: str
    goal: str
    target_weight: int


class Workout(BaseModel):
    exercise: str
    sets: int
    reps: int


class Diet(BaseModel):
    food: str
    calories: int
    protein: int


# ----------------------------
# BASIC TEST ENDPOINT
# ----------------------------

@app.get("/")
def home():
    return {"message": "AI Fitness Coach Backend Running"}


# ----------------------------
# SET USER GOAL
# ----------------------------

@app.post("/set-goal")
def set_goal(goal: Goal):

    goal_data = {
        "name": goal.name,
        "goal": goal.goal,
        "target_weight": goal.target_weight
    }

    users_collection.insert_one(goal_data)

    return {"message": "Goal saved successfully"}


# ----------------------------
# LOG WORKOUT
# ----------------------------

@app.post("/log-workout")
def log_workout(workout: Workout):

    workout_data = {
        "exercise": workout.exercise,
        "sets": workout.sets,
        "reps": workout.reps
    }

    workouts_collection.insert_one(workout_data)

    return {"message": "Workout logged successfully"}


# ----------------------------
# LOG DIET
# ----------------------------

@app.post("/log-diet")
def log_diet(diet: Diet):

    diet_data = {
        "food": diet.food,
        "calories": diet.calories,
        "protein": diet.protein
    }

    diet_collection.insert_one(diet_data)

    return {"message": "Diet logged successfully"}


# ----------------------------
# AI PLAN GENERATION
# ----------------------------

@app.get("/ai-plan")
def ai_plan():

    user = users_collection.find_one({}, {"_id": 0})
    workouts = list(workouts_collection.find({}, {"_id": 0}))
    diet_logs = list(diet_collection.find({}, {"_id": 0}))

    prompt = f"""
    You are a professional fitness coach.

    User Goal:
    {user}

    Workout History:
    {workouts}

    Diet Logs:
    {diet_logs}

    Based on this data, suggest:

    1. Next workout plan
    2. Diet improvement advice
    3. Tips to reach the goal faster
    """

    ai_response = generate_plan(prompt)

    return {
        "goal": user,
        "ai_plan": ai_response
    }