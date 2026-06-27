import numpy as np

__all__ = [
    'read_dat',
]

def read_dat(filepath):
    coords = []
    name = ""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        try:
            x, y = float(parts[0]), float(parts[1])
            coords.append((x, y))
        except (ValueError, IndexError):
            if i == 0:
                name = line
    return name, np.array(coords)