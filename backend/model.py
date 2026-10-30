import torch
import torch.nn as nn

class PreyBrain(nn.Module):
    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(6, 16),
            nn.Tanh(),
            nn.Linear(16, 2),
            nn.Tanh()
        )

    def forward(self, inputs):
        return self.network(inputs)