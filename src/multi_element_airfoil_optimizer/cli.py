from __future__ import annotations

import argparse
import sys

from multi_element_airfoil_optimizer.airfoils import plot_subparser_function
from multi_element_airfoil_optimizer.meshing import (
    build_mesh,
    mesh_plot_subparser_function,
)
from multi_element_airfoil_optimizer.solver import (
    su2_rans_direct_run_subparser_function,
)


def setup_plot_parser(subparsers: argparse._SubParsersAction) -> None:
    plot_parser = subparsers.add_parser("plot", help="Plot an airfoil")
    plot_parser.add_argument(
        "-a",
        "--airfoil",
        type=str,
        required=True,
        help="Name of the airfoil file to plot (e.g., NACA0009.dat)",
    )
    plot_parser.set_defaults(func=plot_subparser_function)


def setup_mesh_plot_parser(subparsers: argparse._SubParsersAction) -> None:
    mesh_plot_parser = subparsers.add_parser(
        "mesh-viz",
        help="Visualise the mesh",
    )
    mesh_plot_parser.set_defaults(func=mesh_plot_subparser_function)


def setup_meshing_parser(subparsers: argparse._SubParsersAction) -> None:
    mesh_plot_parser = subparsers.add_parser(
        "mesh-init",
        help="Generate an Initial mesh",
    )
    mesh_plot_parser.set_defaults(func=build_mesh)


def setup_su2_rans_direct_parser(
        subparsers: argparse._SubParsersAction,
) -> None:
    su2_rans_direct = subparsers.add_parser(
        "su2-rans-direct",
        help="Run SU2_CFD using a config template and save the solution",
    )
    su2_rans_direct.set_defaults(func=su2_rans_direct_run_subparser_function)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MEAOW: Multi-Element Airfoil Optimizer",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )

    setup_plot_parser(subparsers)
    setup_mesh_plot_parser(subparsers)
    setup_meshing_parser(subparsers)
    setup_su2_rans_direct_parser(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
