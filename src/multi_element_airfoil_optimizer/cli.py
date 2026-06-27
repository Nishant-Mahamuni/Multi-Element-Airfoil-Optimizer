import argparse
import sys

from multi_element_airfoil_optimizer.airfoils.airfoil_plotter import handle_plot

def setup_plot_parser(subparsers):
    plot_parser = subparsers.add_parser("plot", help="Plot an airfoil")
    plot_parser.add_argument(
        "-a",
        "--airfoil",
        type=str,
        required=True,
        help="Name of the airfoil file to plot (e.g., NACA0009.dat)",
    )
    plot_parser.set_defaults(func=handle_plot)


def main():
    parser = argparse.ArgumentParser(
        description="MEAOW: Multi-Element Airfoil Optimizer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    setup_plot_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        # Show help if no command was provided (e.g., just running `meaow`)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
