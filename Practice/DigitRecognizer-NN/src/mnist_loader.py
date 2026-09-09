"""
File directly sourced from @mnielsen -- Github
"""
import pickle, gzip
import numpy as np

def load_data(path="data/adu_mnist.pkl.gzip"):
    with gzip.open(path, 'rb') as f:
        return pickle.load(f)

def save_data(path, data):
    with gzip.open(path, 'wb') as f:
        pickle.dump(data, f)

def load_data_wrapper(path, input_size):
    tr_d, va_d, te_d = load_data(path)
    training_inputs = [np.reshape(x, (input_size, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))
    validation_inputs = [np.reshape(x, (input_size, 1)) for x in va_d[0]]
    validation_data = list(zip(validation_inputs, va_d[1]))
    test_inputs = [np.reshape(x, (input_size, 1)) for x in te_d[0]]
    test_data = list(zip(test_inputs, te_d[1]))
    return (training_data, validation_data, test_data)

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

if __name__ == "__main__":
    training_data, validation_data, test_data = load_data(path='data/adu_mnist.pkl.gzip')
    print("images: ", str(training_data[0]))
    
