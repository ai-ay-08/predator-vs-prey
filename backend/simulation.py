import random
import torch

from model import PreyBrain

# Constants
WORLD_WIDTH = 1000
WORLD_HEIGHT = 1000
PREY_INITIAL_COUNT = 10
PREY_SPEED = 20 # Prey speed
PREY_RADIUS = 8
FOOD_RADIUS = 4
FOOD_COUNT = 200

STEP_INTERVAL_SECONDS = 0.02 # Frontend update interval
GENERATION_DURATION_SECONDS = 10 # Time for each generation

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

    def move(self, food_particles, world_width, world_height):
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
                    (food.x - self.x) / world_width,
                    (food.y - self.y) / world_height
                ])
            else:
                inputs.extend([0, 0])

        inputs = torch.tensor(inputs, dtype = torch.float32)

        with torch.no_grad():
            movement = self.brain(inputs)

        self.x += movement[0].item() * PREY_SPEED
        self.y += movement[1].item() * PREY_SPEED

        self.x = max(0, min(world_width, self.x))
        self.y = max(0, min(world_height, self.y))

class World:
    def __init__(self):
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.reset()

    def reset(self):
        self.elapsed_simulation_seconds = 0.0
        self.generation_elapsed_seconds = 0.0
        self.generation_number = 1

        self.prey = [
            Prey(
                random.uniform(0, self.width),
                random.uniform(0, self.height)
            )
            for _ in range(PREY_INITIAL_COUNT)
        ]

        self.food = [
            Food(
                random.uniform(0, self.width),
                random.uniform(0, self.height)
            )
            for _ in range(FOOD_COUNT)
        ]

    def step(self):
        self.elapsed_simulation_seconds += STEP_INTERVAL_SECONDS
        self.generation_elapsed_seconds += STEP_INTERVAL_SECONDS

        for prey in self.prey:
            prey.move(self.food, self.width, self.height)

            # Remove food as soon as the prey's body overlaps it. Iterate over
            # a copy so consumed particles can be removed from the world.
            for food in self.food[:]:
                dx = food.x - prey.x
                dy = food.y - prey.y
                contact_distance = PREY_RADIUS + FOOD_RADIUS
                if dx * dx + dy * dy <= contact_distance * contact_distance:
                    self.food.remove(food)
                    prey.food_eaten += 1

        if self.generation_duration_reached:
            self.end_generation()

    def end_generation(self):
        next_generation = []

        for prey in self.prey:
            if prey.food_eaten == 0:
                continue

            # Eating at least one piece lets the prey survive.
            next_generation.append(prey)

            if prey.food_eaten >= 2:
                offspring = Prey(
                    random.uniform(0, self.width),
                    random.uniform(0, self.height),
                    brain=prey.brain.mutated_copy()
                )
                next_generation.append(offspring)

            prey.food_eaten = 0

        self.prey = next_generation
        self.food = [
            Food(
                random.uniform(0, self.width),
                random.uniform(0, self.height)
            )
            for _ in range(FOOD_COUNT)
        ]
        self.generation_elapsed_seconds = 0.0
        self.generation_number += 1

    @property
    def generation_duration_reached(self):
        return self.generation_elapsed_seconds >= GENERATION_DURATION_SECONDS
    
    def get_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "elapsed_simulation_seconds": round(self.elapsed_simulation_seconds, 1),
            "generation_number": self.generation_number,
            "prey": [
                {"x": prey.x, "y": prey.y}
                for prey in self.prey
            ],
            "food": [
                {"x": food.x, "y": food.y}
                for food in self.food
            ]
        }
