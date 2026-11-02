import torch
import torch.nn as nn
import copy

MUTATION_STRENGTH = 0.1

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

    def mutated_copy(self):
        child = copy.deepcopy(self)

        with torch.no_grad():
            for param in child.parameters():
                param.add_(
                    torch.randn_like(param) * MUTATION_STRENGTH
                )

        return child