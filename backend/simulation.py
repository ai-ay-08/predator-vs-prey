import random
import torch

from model import PreyBrain

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Prey:
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.food_eaten = 0

        self.brain = brain if brain is not None else PreyBrain()

    def move(self, food_particles):
        food_particles = sorted(
            food_particles,
            key = lambda food: 
            (food.x - self.x) ** 2 + (food.y - self.y) ** 2
        )[:3]

        inputs = []

        for i in range(3):
            if i < len(food_particles):
                food = food_particles[i]
                inputs.extend([
                    (food.x - self.x) / 500,
                    (food.y - self.y) / 500
                ])
            else:
                inputs.extend([0, 0])

        inputs = torch.tensor(inputs, dtype = torch.float32)

        with torch.no_grad():
            movement = self.brain(inputs)

        self.x += movement[0].item() * 2
        self.y += movement[1].item() * 2

        self.x = max(0, min(500, self.x))
        self.y = max(0, min(500, self.y))

class World:
    def __init__(self):
        self.width = 500
        self.height = 500

        self.prey = [
            Prey(
                random.uniform(0, 500),
                random.uniform(0, 500)
            )
            for _ in range(20)
        ]

        self.food = [
            Food(
                random.uniform(0, 500),
                random.uniform(0, 500)
            )
            for _ in range(50)
        ]

    def step(self):
        for prey in self.prey: 
            prey.move(self.food)
    
    def get_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "prey": {
                "x": self.prey.x,
                "y": self.prey.y,
            },
            "food": [
                {"x": food.x, "y": food.y}
                for food in self.food
            ]
        }