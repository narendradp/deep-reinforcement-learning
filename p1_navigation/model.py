import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64, fc3v_units=32, fc3a_units=32):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3v = nn.Linear(fc2_units, fc3v_units)
        self.fc3a = nn.Linear(fc2_units, fc3a_units)
        self.fc4v = nn.Linear(fc3v_units, 1)
        self.fc4a = nn.Linear(fc3a_units, action_size)

    def forward(self, state):
        """Build a network that maps state -> action values."""
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        xv = F.relu(self.fc3v(x))
        v = self.fc4v(xv)
        xa = F.relu(self.fc3v(x))
        a = self.fc4a(xa)
        q = a + (v - a.mean(1, True))
        return v, a, q
