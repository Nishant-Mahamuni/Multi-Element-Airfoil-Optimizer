import argparse
import sys

from multi_element_airfoil_optimizer.airfoils import plot_subparser_function
from multi_element_airfoil_optimizer.meshing import (
    mesh_plot_subparser_function,
    build_mesh,
)


def setup_plot_parser(subparsers):
    plot_parser = subparsers.add_parser("plot", help="Plot an airfoil")
    plot_parser.add_argument(
        "-a",
        "--airfoil",
        type=str,
        required=True,
        help="Name of the airfoil file to plot (e.g., NACA0009.dat)",
    )
    plot_parser.set_defaults(func=plot_subparser_function)
    
    
def setup_mesh_plot_parser(subparsers):
    mesh_plot_parser = subparsers.add_parser(
        "mesh-viz",
        help="Visualise the mesh",
    )
    mesh_plot_parser.set_defaults(func=mesh_plot_subparser_function)
    
    
def setup_meshing_parser(subparsers):
    mesh_plot_parser = subparsers.add_parser(
        "mesh-init",
        help="Generate an Initial mesh",
    )
    mesh_plot_parser.set_defaults(func=build_mesh)


def main():
    parser = argparse.ArgumentParser(
        description="MEAOW: Multi-Element Airfoil Optimizer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    setup_plot_parser(subparsers)
    setup_mesh_plot_parser(subparsers)
    setup_meshing_parser(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
