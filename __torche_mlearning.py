import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd


# Define the FootballDataset class
class FootballDataset(Dataset):
    def __init__(self, data):
        self.data = data.drop('outcome', axis=1).values
        self.labels = data['outcome'].values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


# Load the data from a CSV file
data = pd.read_csv('football_data.csv')

# Split the data into training and testing sets
train_size = int(0.8 * len(data))
train_data, test_data = torch.utils.data.random_split(data, [train_size, len(data) - train_size])

# Define the data loaders for training and testing
train_loader = torch.utils.data.DataLoader(FootballDataset(train_data), batch_size=32, shuffle=True)
test_loader = torch.utils.data.DataLoader(FootballDataset(test_data), batch_size=32)


# Define the neural network model
class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(4, 10)
        self.fc2 = torch.nn.Linear(10, 2)

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Train the model
model = Net()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

for epoch in range(100):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs.float())
        loss = criterion(outputs, labels.long())
        loss.backward()
        optimizer.step()

# Test the model
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs.float())
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f'Accuracy: {accuracy:.2f}%')
