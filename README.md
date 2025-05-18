# Code 39 Barcode Parser

A Python-based tool to decode Code 39 (Code 3 of 9) barcodes from images. Code 39 is a discrete, variable-length symbology that supports alphanumeric characters.

## Features

- Image preprocessing and binarization
- Automatic barcode region detection and cropping
- Bar width analysis and pattern recognition
- Full Code 39 character set support

## How It Works

1. **Image Preprocessing**: Converts the input image to grayscale and applies thresholding to binarize.
2. **Region Detection**: Identifies and crops the barcode-containing area.
3. **Bar Analysis**: Measures bar and space widths to determine patterns.
4. **Pattern Recognition**: Matches extracted patterns to the Code 39 specification.
5. **Decoding**: Translates the sequence into readable characters.

## Requirements

- Python 3.x
- NumPy
- Pillow (PIL)

## Installation

```bash
pip install numpy pillow
```
## Usage

Run the script and input the path to an image file containing a Code 39 barcode when prompted.

```bash
python main.py
```

#Code 39 Specification
- Each character is encoded using 9 elements: 5 bars and 4 spaces
- Elements are either narrow (n) or wide (w)
- A start/stop character (*) is required for decoding

#Technical Components
- read_and_binarize: Converts the image to binary (black and white)
- crop_barcode_region: Detects and crops the barcode region
- trim_to_bars: Further isolates the barcode area
- compute_run_widths: Measures widths of alternating bars and spaces
- classify_runs: Classifies runs as 'n' (narrow) or 'w' (wide)
- chunk_pattern: Segments the pattern into character-sized chunks
- decode_chunks: Maps patterns to characters using the Code 39 table



