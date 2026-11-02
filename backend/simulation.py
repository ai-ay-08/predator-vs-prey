import random
import torch

from model import PreyBrain

# Constants
SPEED = 10
PREY_RADIUS = 8
FOOD_RADIUS = 4

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

        self.x += movement[0].item() * SPEED
        self.y += movement[1].item() * SPEED

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
            for _ in range(1)
        ]

        self.food = [
            Food(
                random.uniform(0, 500),
                random.uniform(0, 500)
            )
            for _ in range(20)
        ]

    def step(self):
        for prey in self.prey:
            prey.move(self.food)

            # Remove food as soon as the prey's body overlaps it. Iterate over
            # a copy so consumed particles can be removed from the world.
            for food in self.food[:]:
                dx = food.x - prey.x
                dy = food.y - prey.y
                contact_distance = PREY_RADIUS + FOOD_RADIUS
                if dx * dx + dy * dy <= contact_distance * contact_distance:
                    self.food.remove(food)
                    prey.food_eaten += 1
    
    def get_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "prey": [
                {"x": prey.x, "y": prey.y}
                for prey in self.prey
            ],
            "food": [
                {"x": food.x, "y": food.y}
                for food in self.food
            ]
        }
