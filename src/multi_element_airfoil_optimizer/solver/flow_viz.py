from __future__ import annotations

__all__ = [
    "flow_viz_subparser_function",
]

import argparse
from pathlib import Path

import pyvista as pv

from multi_element_airfoil_optimizer import ROOT_DIR

SOLVER_MAP = {
    "inc_rans": "su2_runners",
}


def plot_flow_contour(file_path: Path, field: str = "Velocity"):
    if not file_path.exists():
        raise FileNotFoundError(
            f"Cannot find {file_path}. Run the solver first!")

    print(f"Loading mesh: {file_path}")
    mesh = pv.read(file_path)

    z_min, z_max = mesh.bounds[4], mesh.bounds[5]
    if z_min == z_max:
        plot_mesh = mesh
    else:
        z_mid = (z_min + z_max) / 2.0
        print(f"Mesh is 3D extruded. Slicing at Z = {z_mid}")
        plot_mesh = mesh.slice(normal='z', origin=(0, 0, z_mid))

    plotter = pv.Plotter()
    plotter.add_mesh(
        plot_mesh,
        scalars=field,
        cmap="jet",
        show_edges=False,
        lighting=False,
    )
    plotter.view_xy()
    plotter.add_text(f"{field} Contour", font_size=14)
    plotter.show()


def flow_viz_subparser_function(args: argparse.Namespace) -> None:
    solver = args.solver.strip()
    feature = args.feature.strip().capitalize()

    filepath = (
        ROOT_DIR / "solver" / SOLVER_MAP[solver] /
        solver / "outputs" / "flow.vtu"
    )
    plot_flow_contour(filepath, field=feature)
