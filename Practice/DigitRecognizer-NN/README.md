# DigitRecognizer-NN - Neural Network-Based Digit Recognizer

A Python project for recognizing digits using neural networks (MNIST dataset).

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Required packages:
- numpy (neural network computations)
- pillow (PIL) for image processing
- tkinter for GUI development

## Project Structure

```
DigitRecognizer-NN/
├── src/                    # Source code files
│   ├── adu_main_form.py   # GUI main form
│   ├── chatgpt.py         # ChatGPT API integration
│   ├── grok.py            # Grok API integration
│   ├── image_processing.py# Image processing utilities
│   ├── mnist_loader.py    # MNIST dataset loader
│   ├── network.py         # Neural network definitions
│   ├── main.py            # Main entry point
│   └── main_form.py       # GUI implementation
├── data/                   # Training and test datasets
├── images/                 # Sample images for testing
├── models/                # Saved neural network models
├── plots/                 # Generated visualization plots
├── raw-images/            # Raw image files
└── example/               # Example scripts and code
```

## Usage

### Running the Main Application

Start the digit recognition application:

```bash
python src/adu_main_form.py
```

### Training a New Model

Train a neural network on the MNIST dataset:

```bash
python src/train_model.py --dataset mnist --epochs 10 --save-model
```

### Image Recognition

Use the image processing module to recognize digits in images:

```python
from image_processing import DigitRecognizer

recognizer = DigitRecognizer()
digit = recognizer.recognize_image('image.jpg')
print(f"Recognized digit: {digit}")
```

## Development Notes

- The project uses MNIST (Modified National Institute of Standards and Technology) dataset for training
- Neural networks are built using TensorFlow/PyTorch
- Images are preprocessed using Pillow before recognition

## License

This project is part of academic coursework (M.N. Mahmudov - Seminar).
