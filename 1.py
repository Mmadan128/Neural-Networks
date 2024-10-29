import numpy as np

class Value:
    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.prev = []

    def backward(self):
        for v in self.prev:
            derivs = self.derivative()
            for i in range(len(derivs)):
                v.grad += self.grad * derivs[i]
            v.backward()

    def derivative(self):
        raise NotImplementedError("This method should be implemented in subclasses")


class Add(Value):
    def __init__(self, a, b):
        super().__init__(a.data + b.data)
        self.prev = [a, b]

    def derivative(self):
        return (1, 1)  # Both inputs contribute equally


class Subtract(Value):
    def __init__(self, a, b):
        super().__init__(a.data - b.data)
        self.prev = [a, b]

    def derivative(self):
        return (1, -1)  # The first input adds, the second subtracts


class Multiply(Value):
    def __init__(self, a, b):
        super().__init__(a.data * b.data)
        self.prev = [a, b]

    def derivative(self):
        return (self.prev[1].data, self.prev[0].data)  # Each input affects the result


class Divide(Value):
    def __init__(self, a, b):
        super().__init__(a.data / b.data)
        self.prev = [a, b]

    def derivative(self):
        return (1 / self.prev[1].data, -self.prev[0].data / (self.prev[1].data ** 2))  # Each input has a unique impact


class Tanh(Value):
    def __init__(self, a):
        super().__init__(np.tanh(a.data))
        self.prev = [a]

    def derivative(self):
        return (1 - np.tanh(self.prev[0].data) ** 2,)  # Reflects the change rate of tanh


def add(a, b):
    return Add(a, b)

def subtract(a, b):
    return Subtract(a, b)

def multiply(a, b):
    return Multiply(a, b)

def divide(a, b):
    return Divide(a, b)

def tanh(a):
    return Tanh(a)

# Simple Tests
x = Value(2.0)
y = Value(3.0)
z = add(x, y)
z.grad = 1
z.backward()
print("Addition:", x.grad, y.grad)  # Check gradients for addition

x = Value(5.0)
y = Value(3.0)
z = subtract(x, y)
z.grad = 1
z.backward()
print("Subtraction:", x.grad, y.grad)  # Verify subtraction gradients

x = Value(2.0)
y = Value(3.0)
z = multiply(x, y)
z.grad = 1
z.backward()
print("Multiplication:", x.grad, y.grad)  # Ensure multiplication gradients

x = Value(6.0)
y = Value(3.0)
z = divide(x, y)
z.grad = 1
z.backward()
print("Division:", x.grad, y.grad)  # Assess division gradients

x = Value(1.0)
z = tanh(x)
z.grad = 1
z.backward()
print("Tanh:", x.grad)  # Examine tanh gradient
