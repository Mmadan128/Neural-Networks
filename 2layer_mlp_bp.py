import torch
import torch.nn as nn
import torch.optim as optim

# Define a class for our 2-layer Multi-Layer Perceptron (MLP)
class TwoLayerMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(TwoLayerMLP, self).__init__()
        # First linear layer
        self.first_layer = nn.Linear(input_size, hidden_size)
        # Batch normalization after the first layer
        self.batch_norm_first = nn.BatchNorm1d(hidden_size)
        # Second linear layer
        self.second_layer = nn.Linear(hidden_size, output_size)
        # Batch normalization after the second layer
        self.batch_norm_second = nn.BatchNorm1d(output_size)

    def forward(self, input_data):
        # Forward pass through the model
        layer_output = self.first_layer(input_data)       # Linear layer
        layer_output = self.batch_norm_first(layer_output)  # Batch normalization
        layer_output = torch.tanh(layer_output)           # Tanh activation function
        layer_output = self.second_layer(layer_output)     # Second linear layer
        layer_output = self.batch_norm_second(layer_output)  # Second batch normalization
        return layer_output

# Create an instance of the model
input_size = 10   # Number of features in the input data
hidden_size = 5   # Number of neurons in the hidden layer
output_size = 3   # Number of output classes
model = TwoLayerMLP(input_size, hidden_size, output_size)

# Sample input data
input_data = torch.randn(1, input_size)  # Random input tensor
output = model(input_data)                # Get the model output
print("Output of the model:", output)

# Define target (true labels)
target_label = torch.tensor([1])  # Assuming class index 1 is the target

# Define the loss function (cross-entropy loss)
loss_function = nn.CrossEntropyLoss()
loss = loss_function(output, target_label)
print("Loss:", loss.item())

def manual_backpropagation(model, input_data, target_label):
    # Zero out the gradients for the model
    model.zero_grad()
    
    # Forward pass through the model
    output = model(input_data)
    
    # Calculate the loss
    loss = loss_function(output, target_label)

    # Step 1: Compute gradient of the loss with respect to output
    loss_gradient = torch.zeros_like(output)
    loss_gradient[target_label] = -1 / output.shape[0] * (torch.exp(output) / torch.sum(torch.exp(output)))  # Gradient for cross-entropy
    
    # Step 2: Backpropagate through the second layer
    second_layer_output = model.second_layer(model.batch_norm_first(model.first_layer(input_data)))
    second_layer_output_gradient = loss_gradient * (model.batch_norm_second.weight / model.batch_norm_second.running_var).view(1, -1)
    model.second_layer.weight.grad = torch.matmul(model.batch_norm_first(model.first_layer(input_data)).t(), second_layer_output_gradient)
    model.second_layer.bias.grad = second_layer_output_gradient.sum(dim=0)
    
    # Step 3: Backpropagate through batch normalization (for layer 2)
    batch_norm_second_gradient = second_layer_output_gradient * (1 - torch.tanh(second_layer_output) ** 2)
    model.batch_norm_second.weight.grad = batch_norm_second_gradient.sum(dim=0)
    
    # Step 4: Backpropagate through the first layer
    first_layer_output = model.first_layer(input_data)
    first_layer_output_gradient = batch_norm_second_gradient @ model.second_layer.weight * (1 - torch.tanh(first_layer_output) ** 2)
    model.first_layer.weight.grad = torch.matmul(input_data.t(), first_layer_output_gradient)
    model.first_layer.bias.grad = first_layer_output_gradient.sum(dim=0)

    # Step 5: Backpropagate through batch normalization (for layer 1)
    batch_norm_first_gradient = first_layer_output_gradient * (1 - torch.tanh(first_layer_output) ** 2)
    model.batch_norm_first.weight.grad = batch_norm_first_gradient.sum(dim=0)

    # Return the loss value
    return loss.item()

# Training loop to manually backpropagate and compute the loss
for epoch in range(100):  # Number of epochs
    loss = manual_backpropagation(model, input_data, target_label)
    print(f"Epoch {epoch+1}, Loss: {loss}")

    # You could use an optimizer here to update weights if needed
