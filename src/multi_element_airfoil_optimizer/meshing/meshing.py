from __future__ import annotations

__all__ = [
    "build_mesh",
]

import argparse
from pathlib import Path

import gmsh
import numpy as np
from numpy.typing import NDArray

ROOT_DIR = Path(__file__).resolve().parents[1]
ELEMENTS_DIR = ROOT_DIR / "geometry" / "elements"
OUTPUT_SU2 = ROOT_DIR / "meshing" / "outputs" / "mesh.su2"


def load_airfoil_dat(filepath: str | Path) -> tuple[NDArray, NDArray]:
    data = np.loadtxt(filepath, skiprows=1)
    x, y = data[:, 0], data[:, 1]
    return x, y


def deduplicate_endpoints(
    x: NDArray,
    y: NDArray,
    tol: float = 1e-6,
) -> tuple[NDArray, NDArray]:
    if np.hypot(x[-1] - x[0], y[-1] - y[0]) < tol:
        return x[:-1], y[:-1]
    return x, y


def create_airfoil_geometry(
    x_coords: NDArray,
    y_coords: NDArray,
    mesh_size: float = 0.01,
) -> tuple[int, list[int]]:
    x_coords, y_coords = deduplicate_endpoints(x_coords, y_coords)
    points = [
        gmsh.model.geo.addPoint(x, y, 0, mesh_size)
        for x, y in zip(x_coords, y_coords, strict=False)
    ]
    lines = [
        gmsh.model.geo.addLine(points[i], points[(i + 1) % len(points)])
        for i in range(len(points))
    ]
    return gmsh.model.geo.addCurveLoop(lines), lines


def build_mesh(args: argparse.Namespace) -> None:
    gmsh.initialize()

    gmsh.option.setNumber("Geometry.Tolerance", 1e-9)
    gmsh.option.setNumber("Geometry.ToleranceBoolean", 1e-9)
    gmsh.model.add("multi_element_airfoil")
    gmsh.option.setNumber("Mesh.Algorithm", 6)

    center = gmsh.model.geo.addPoint(0.5, 0, 0, 1.0)
    p_top = gmsh.model.geo.addPoint(0.5, 15, 0, 1.0)
    p_bot = gmsh.model.geo.addPoint(0.5, -15, 0, 1.0)
    p_left = gmsh.model.geo.addPoint(-14.5, 0, 0, 1.0)
    p_right = gmsh.model.geo.addPoint(15.5, 0, 0, 1.0)

    arc1 = gmsh.model.geo.addCircleArc(p_right, center, p_top)
    arc2 = gmsh.model.geo.addCircleArc(p_top, center, p_left)
    arc3 = gmsh.model.geo.addCircleArc(p_left, center, p_bot)
    arc4 = gmsh.model.geo.addCircleArc(p_bot, center, p_right)

    farfield_loop = gmsh.model.geo.addCurveLoop([arc1, arc2, arc3, arc4])
    farfield_arcs = [arc1, arc2, arc3, arc4]

    all_airfoil_loops = []
    all_airfoil_lines = []

    for dat_file in ELEMENTS_DIR.glob("*.dat"):
        x, y = load_airfoil_dat(dat_file)
        loop, lines = create_airfoil_geometry(x, y)
        all_airfoil_loops.append(loop)
        all_airfoil_lines.extend(lines)

    fluid_surface = gmsh.model.geo.addPlaneSurface(
        [farfield_loop, *all_airfoil_loops],
    )

    gmsh.model.geo.synchronize()

    bl_field = gmsh.model.mesh.field.add("BoundaryLayer")
    gmsh.model.mesh.field.setNumbers(bl_field, "CurvesList", all_airfoil_lines)
    gmsh.model.mesh.field.setNumber(bl_field, "Size", 0.005)
    gmsh.model.mesh.field.setNumber(bl_field, "Ratio", 1.2)
    gmsh.model.mesh.field.setNumber(bl_field, "Thickness", 0.03)
    gmsh.model.mesh.field.setNumber(bl_field, "Quads", 1)
    gmsh.model.mesh.field.setAsBackgroundMesh(bl_field)

    gmsh.model.addPhysicalGroup(1, all_airfoil_lines, name="airfoils")
    gmsh.model.addPhysicalGroup(1, farfield_arcs, name="farfield")
    gmsh.model.addPhysicalGroup(2, [fluid_surface], name="fluid")

    gmsh.model.mesh.generate(2)

    OUTPUT_SU2.parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(str(OUTPUT_SU2))

    output_msh = OUTPUT_SU2.with_suffix(".msh")
    gmsh.write(str(output_msh))
    gmsh.finalize()
