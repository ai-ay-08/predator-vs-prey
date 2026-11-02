from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulation import World

app = FastAPI(title = "Predator vs. Prey")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:4200",
        "http://127.0.0.1:8000"
    ],
    allow_methods = ["*"],
    allow_headers = ["*"]
)   

world = World()

@app.get("/")
def home():
    return {"message": "Predator vs. Prey API is running!"}

@app.get("/simulation/state")
def get_state():
    return world.get_state()

@app.post("/simulation/step")
def step_simulation():
    world.step()
    return world.get_state()

@app.post("/simulation/reset")
def reset_simulation():
    world.reset()
    return world.get_state()
