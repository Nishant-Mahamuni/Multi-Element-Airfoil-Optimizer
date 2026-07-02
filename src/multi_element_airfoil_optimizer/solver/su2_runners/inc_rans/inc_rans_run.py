from __future__ import annotations

__all__ = [
    "su2_inc_rans_run",
    "su2_inc_rans_run_subparser_function",
]

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from multi_element_airfoil_optimizer import ROOT_DIR

TEMPLATE = Path(__file__).parent / "inc_rans_config.cfg"
MESH = ROOT_DIR / "meshing" / "outputs" / "mesh.su2"
OUTPUT_DIR = Path(__file__).parent / "outputs"

_SU2_OUTPUTS = [
    "flow.vtu",
    "flow.vtk",             # — full volume field (velocity, pressure, Mach, …)
    "surface_flow.csv",     # — boundary quantities (Cp, Cf, …) on the airfoil
    "history.csv",          # — per-iteration residuals, CL, CD
    "restart_flow.dat",
]


def su2_inc_rans_run(args: argparse.Namespace) -> None:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Config template not found: {TEMPLATE}")
    if not MESH.exists():
        raise FileNotFoundError(
            f"Mesh file not found: {MESH}\n"
            "Run  meaow mesh-init  first to generate the mesh.",
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="su2_run_") as tmp_str:
        tmp = Path(tmp_str)
        cfg_path = tmp / "su2_run.cfg"
        local_mesh_path = tmp / "mesh.su2"
        shutil.copy2(MESH, local_mesh_path)
        cfg_text = TEMPLATE.read_text()

        cfg_text = re.sub(r"^\s*MESH_FILENAME\s*=.*$", "", cfg_text,
                          flags=re.MULTILINE)

        cfg_text += "\nMESH_FILENAME= mesh.su2\n"

        cfg_path.write_text(cfg_text)

        print(
            f"[su2-run] Template : {TEMPLATE}\n"
            f"[su2-run] Mesh     : {MESH}\n"
            f"[su2-run] Output   : {OUTPUT_DIR}\n",
            flush=True,
        )

        result = subprocess.run(["SU2_CFD", str(cfg_path)], cwd=tmp)

        if result.returncode != 0:
            raise RuntimeError(f"SU2_CFD exited with code {result.returncode}.")

        collected: list[Path] = []
        for filename in _SU2_OUTPUTS:
            src = tmp / filename
            if src.exists():
                dst = OUTPUT_DIR / filename
                shutil.copy2(src, dst)
                collected.append(dst)
                print(f"[su2-run] Saved  : {dst}")

        shutil.copy2(cfg_path, OUTPUT_DIR / "su2_run.cfg")

        if not collected:
            print(
                "[su2-run] Warning: no recognised output files were found.\n"
                "Check that OUTPUT_FILES in your template matches your SU2"
                "version.",
                file=sys.stderr,
            )

    print(f"[su2-run] Done. Results in {OUTPUT_DIR}")


def su2_inc_rans_run_subparser_function(args: argparse.Namespace) -> None:
    try:
        su2_inc_rans_run(args)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"[su2-run] Error: {exc}", file=sys.stderr)
        sys.exit(1)
