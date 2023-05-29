import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
#from sklearn.model_selection import train_test_split


# Define neural network architecture
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(8, 16)
        self.fc2 = nn.Linear(16, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.softmax(x, dim=1)


# Load data from CSV file
data = pd.read_csv('football_data.csv')

# Split data into training and test sets
train_data, test_data, train_labels, test_labels = train_test_split(
    data.drop('outcome', axis=1),
    data['outcome'],
    test_size=0.2,
    random_state=42
)

# Convert data to PyTorch tensors
train_data = torch.tensor(train_data.values, dtype=torch.float32)
test_data = torch.tensor(test_data.values, dtype=torch.float32)
train_labels = torch.tensor(train_labels.values, dtype=torch.long)
test_labels = torch.tensor(test_labels.values, dtype=torch.long)

# Train neural network
net = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

for epoch in range(1000):
    optimizer.zero_grad()
    outputs = net(train_data)
    loss = criterion(outputs, train_labels)
    loss.backward()
    optimizer.step()

# Evaluate model on test set
with torch.no_grad():
    outputs = net(test_data)
    _, predicted = torch.max(outputs.data, 1)
    total = test_labels.size(0)
    correct = (predicted == test_labels).sum().item()
    accuracy = correct / total

# Define input data for prediction
new_data = torch.tensor([[10, 7, 9, 2, 12, 9, 8, 1]], dtype=torch.float32)

# Predict outcome of new data
with torch.no_grad():
    outputs = net(new_data)
    prediction = outputs[0].tolist()

# Print predicted outcome in percentages
team1_name = 'Team XYZ'
team2_name = 'Team ZYX'
print(f'{team1_name} {prediction[0] * 100:.2f}% vs {team2_name} {prediction[1] * 100:.2f}%')


def train_and_save_model(data, labels, num_epochs, save_path):
    # Define your neural network architecture and optimizer
    model = torch.nn.Sequential(
        torch.nn.Linear(4, 16),
        torch.nn.ReLU(),
        torch.nn.Linear(16, 3)
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Convert data and labels to PyTorch tensors
    data_tensor = torch.Tensor(data)
    label_tensor = torch.LongTensor(labels)

    # Define the loss function
    loss_fn = torch.nn.CrossEntropyLoss()

    # Train the model for the specified number of epochs
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(data_tensor)
        loss = loss_fn(outputs, label_tensor)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print the loss every 10 epochs
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    # Save the trained model to a file
    torch.save(model, save_path)
