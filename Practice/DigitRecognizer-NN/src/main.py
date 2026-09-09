from __future__ import print_function
import mnist_loader
import network
from network import Network
import matplotlib.pyplot as plt

# hyperparameters
learning_rate = 2
epochs = 100
mini_batch_size = 64

input_size = 784
layers = [input_size, 64, 64, 10]
adumnist = "data/adu_mnist.pkl.gzip"
mnist = "data/mnist.pkl.gzip"


training_data, validation_data, test_data = mnist_loader.load_data_wrapper(mnist, input_size)
net = network.Network(layers)
net.SGD(training_data, epochs, mini_batch_size, learning_rate, test_data=test_data)

training_data, validation_data, test_data = mnist_loader.load_data_wrapper(adumnist, input_size)
adunet = network.Network(layers)
adunet.SGD(training_data, epochs, mini_batch_size, learning_rate, test_data=test_data)

print("saving models")
mnist_loader.save_data("models/mnist.pkl.gzip", net)
mnist_loader.save_data("models/adu_mnist.pkl.gzip", adunet)

x = [z for z in range(1, epochs+1)]
y = net.accuracy
y2 = adunet.accuracy

plt.title(f"O'qitishda aniqlik darajasi")
plt.ylabel("Aniqlik %")
plt.xlabel("O'qitish davri")
plt.plot(x, y, label=f"dataset: {mnist}")
plt.plot(x, y2, label=f"dataset: {adumnist}")
plt.legend()
plt.savefig("plots/models_accuracy.png")

