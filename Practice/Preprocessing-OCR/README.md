# Preprocessing-OCR - Open Text Recognition Image Preprocessor

A Python project for image preprocessing in OCR (Optical Character Recognition) applications.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Required packages:
- pillow (PIL) for image processing
- numpy for numerical operations
- matplotlib for visualization

## Project Structure

```
Preprocessing-OCR/
├── src/                          # Source code files
│   ├── algorithms.py            # Image processing algorithms
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # Configuration settings
│   ├── constants.py             # Application constants
│   ├── convertion.py            # Format conversion utilities
│   ├── gui.py                   # GUI implementation
│   ├── image.py                 # Core image processing
│   ├── utility.py               # Utility functions
│   └── uzbek_language.py        # Uzbek language-specific preprocessing
├── dataset/                      # Training datasets
└── example/                     # Example scripts
```

## Usage

### Running via Command Line

Process an image using the CLI:

```bash
python src/cli.py --input input.jpg --output output.jpg --mode denoise
```

Available modes:
- `denoise` - Remove noise from images
- `enhance` - Enhance image contrast
- `binarize` - Convert to binary for OCR
- `threshold` - Apply threshold filtering

### Programmatic Usage

Import and use the image processing utilities:

```python
from src.image import ImageProcessor
from src.algorithms import Denoise, Enhance, Binarize

processor = ImageProcessor()

# Process images with multiple steps
denoised = Denoise().process('image.jpg')
enhanced = Enhance().process(denoised)
binary = Binarize().process(enhanced)

# Save processed image
binary.save('output.jpg')
```

### GUI Application

Run the graphical interface:

```bash
python src/gui.py
```

## Features

- Multi-resolution support
- Automatic contrast enhancement
- Noise reduction filters (median, Gaussian, bilateral)
- Binarization for OCR optimization
- Uzbek language specific preprocessing algorithms
- Batch image processing
- Image format conversion (JPEG, PNG, TIFF, BMP)

## Development Notes

- Optimized for high-resolution documents
- Supports grayscale and color image input
- Customizable threshold values for binarization
- Compatible with standard OCR pipelines

## License

This project is part of academic coursework.
