from PIL import Image
import numpy as np
import sys
import os

CODE39_PATTERNS = {
    '0': 'nnnwwnwnn', '1': 'wnnwnnnnw', '2': 'nnwwnnnnw', '3': 'wnwwnnnnn',
    '4': 'nnnwwnnnw', '5': 'wnnwwnnnn', '6': 'nnwwwnnnn', '7': 'nnnwnnwnw',
    '8': 'wnnwnnwnn', '9': 'nnwwnnwnn', 'A': 'wnnnnwnnw', 'B': 'nnwnnwnnw',
    'C': 'wnwnnwnnn', 'D': 'nnnnwwnnw', 'E': 'wnnnwwnnn', 'F': 'nnwnwwnnn',
    'G': 'nnnnnwwnw', 'H': 'wnnnnwwnn', 'I': 'nnwnnwwnn', 'J': 'nnnnwwwnn',
    'K': 'wnnnnnnww', 'L': 'nnwnnnnww', 'M': 'wnwnnnnwn', 'N': 'nnnnwnnww',
    'O': 'wnnnwnnwn', 'P': 'nnwnwnnwn', 'Q': 'nnnnnnwww', 'R': 'wnnnnnwwn',
    'S': 'nnwnnnwwn', 'T': 'nnnnwnwwn', 'U': 'wwnnnnnnw', 'V': 'nwwnnnnnw',
    'W': 'wwwnnnnnn', 'X': 'nwnnwnnwn', 'Y': 'wwnnwnnnn', 'Z': 'nwwnwnnnn',
    '-': 'nwnnnnwnw', '.': 'wwnnnnwnn', ' ': 'nwwnnnwnn', '$': 'nwnwnwnnn',
    '/': 'nwnwnnnwn', '+': 'nwnnnwnwn', '%': 'nnnwnwnwn', '*': 'nwnnwnwnn'
}

def crop_barcode_region(binary_img):
    h, w = binary_img.shape
    row_sums = np.sum(binary_img == 255, axis=1) 
    threshold = 0.3 * w  

    start, end = None, None
    for i, val in enumerate(row_sums):
        if val > threshold and start is None:
            start = i
        elif start is not None and val < threshold:
            end = i
            break

    if start is None or end is None:
        start = h // 3
        end = 2 * h // 3
    return binary_img[start:end, :]



def read_and_binarize(path, threshold=150):
    try:
        img = Image.open(path).convert('L')
    except Exception as e:
        return None, None
    arr = np.array(img)
    binary = (arr < threshold).astype(np.uint8) * 255
    return img.size, binary


def trim_to_bars(slice_img):
    h, _ = slice_img.shape
    black_counts = np.count_nonzero(slice_img == 255, axis=0)
    threshold = h // 4
    cols = np.where(black_counts > threshold)[0]
    if cols.size == 0:
        return slice_img
    start, end = cols[0], cols[-1]
    return slice_img[:, start:end+1]


def compute_run_widths(slice_img):
    h, w = slice_img.shape
    threshold = h // 2
    runs = []
    curr_color = None
    curr_width = 0
    for x in range(w):
        black_count = np.count_nonzero(slice_img[:, x] == 255)
        color = 'black' if black_count > threshold else 'white'
        if color == curr_color:
            curr_width += 1
        else:
            if curr_color is not None:
                runs.append((curr_color, curr_width))
            curr_color = color
            curr_width = 1
    if curr_color:
        runs.append((curr_color, curr_width))
    return runs


def classify_runs(runs):
    widths = [w for _, w in runs if w > 0]
    minn = min(widths)
    maxx = max(widths)
    thresh = (minn+maxx)/2
    pattern = ''.join('n' if w <= thresh else 'w' for _, w in runs)
    return pattern


def chunk_pattern(pattern):
    chunks = [pattern[i:i+10] for i in range(0, len(pattern), 10)]
    chunks = [chunk[0:9] for chunk in chunks]
    return chunks


def decode_chunks(chunks):
    inv_map = {v: k for k, v in CODE39_PATTERNS.items()}
    decoded = ''.join(inv_map.get(chunk, '?') for chunk in chunks)
    return decoded


if __name__ == '__main__':
    path = input()
    if not os.path.isfile(path):
        sys.exit(1)

    size, binary = read_and_binarize(path)
    if binary is None:
        sys.exit(1)

    cropped = crop_barcode_region(binary)
    trimmed = trim_to_bars(cropped)
    runs = compute_run_widths(trimmed)
    pattern = classify_runs(runs)
    chunks = chunk_pattern(pattern)
    result = decode_chunks(chunks)
    
    print(result[1:-1])