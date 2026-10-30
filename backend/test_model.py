import torch
from model import PreyBrain

brain = PreyBrain()

inputs = torch.tensor([
    0.2, -0.1,
    0.5, 0.3,
    -0.4, 0.6
])

movement = brain(inputs)

print("Movement: ", movement)