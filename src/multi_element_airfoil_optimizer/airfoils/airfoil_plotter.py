import sys

import matplotlib.pyplot as plt
from pathlib import Path

from multi_element_airfoil_optimizer.helpers import read_dat

HERE = Path(__file__).parent

def plot_airfoil(filepath):
    name, coords = read_dat(filepath)
    x, y = coords[:, 0], coords[:, 1]

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.grid(True, linestyle='--', alpha=0.5)
    ax.axhline(0, color='k', linewidth=0.5, linestyle='--')

    ax.plot(x, y, 'b-', linewidth=1.5, label=name or "Airfoil")
    ax.fill(x, y, alpha=0.1, color='steelblue')

    ax.set_aspect('equal')

    ax.set_xlabel("x/c", fontsize=12)
    ax.set_ylabel("y/c", fontsize=12)

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.6, 0.6)

    ax.set_title(f"Airfoil: {name}", fontsize=14)
    plt.tight_layout()
    plt.show()

def handle_plot(args):
    filename = args.airfoil.strip()

    if not filename.endswith(".dat"):
        filename += ".dat"

    filepath = HERE / "airfoil_files" / filename

    if not filepath.exists():
        print(f"Error: File not found at {filepath}")
        sys.exit(1)
    else:
        print(f"Plotting {filename}...")
        plot_airfoil(filepath)