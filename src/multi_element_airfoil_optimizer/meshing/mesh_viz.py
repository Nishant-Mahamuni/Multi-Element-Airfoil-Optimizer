from __future__ import annotations

__all__ = [
    "mesh_plot_subparser_function",
]

import meshio
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_MSH = ROOT_DIR / "meshing" / "outputs" / "mesh.msh"


def mesh_plot_subparser_function(args):
    mesh_file = OUTPUT_MSH
    print(f"Reading {mesh_file}...")
    try:
        mesh = meshio.read(mesh_file)
    except FileNotFoundError:
        print(f"Error: Mesh file not found at {mesh_file}")
        return

    points = mesh.points[:, :2]

    print("Extracting edges from elements...")
    edges = set()

    for cell_block in mesh.cells:
        if cell_block.type == "triangle":
            for tri in cell_block.data:
                edges.add(tuple(sorted((tri[0], tri[1]))))
                edges.add(tuple(sorted((tri[1], tri[2]))))
                edges.add(tuple(sorted((tri[2], tri[0]))))

        elif cell_block.type == "quad":
            for q in cell_block.data:
                edges.add(tuple(sorted((q[0], q[1]))))
                edges.add(tuple(sorted((q[1], q[2]))))
                edges.add(tuple(sorted((q[2], q[3]))))
                edges.add(tuple(sorted((q[3], q[0]))))

    edge_coords = [(points[i], points[j]) for i, j in edges]

    print("Plotting mesh...")
    fig, ax = plt.subplots(figsize=(12, 8))

    lc = LineCollection(edge_coords, colors="black", linewidths=0.2, alpha=0.7)
    ax.add_collection(lc)

    ax.autoscale()
    ax.set_aspect("equal")

    ax.set_title(f"Mesh Visualization: {mesh_file.name}")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")

    plt.tight_layout()
    plt.show()
