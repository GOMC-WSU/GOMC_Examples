# F1A-C1A GEMC Example

Hybrid MD/MC simulation of the F1A-C1A binary mixture (methanol and n-hexane,
TraPPE force field) in the Gibbs ensemble at a temperature of 500 K, giving the
coexisting vapor and liquid compositions and densities.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```text
GEMC/F1A-C1A/
├── user_input_NAMD_GOMC.json    # JSON input for this example
├── README.md
└── required_data/
    ├── config_files/            # NAMD and GOMC control-file templates
    ├── input/                   # Force field (.inp) and coordinate/topology (.pdb/.psf) files
    └── bin/                     # catdcd trajectory utility
```

## Simulation Overview

The simulation proceeds through a series of alternating molecular dynamics time
steps and Monte Carlo moves.

Molecular dynamics is performed in the canonical (NVT) ensemble on the liquid box
(Box 0) and is used to sample configurational and conformational degrees of
freedom.

Monte Carlo molecule transfers between the two boxes and volume-exchange moves are
performed at constant temperature. The two boxes come to the same temperature,
pressure, and component chemical potentials, so Box 0 settles at the liquid
density and composition and Box 1 at the vapor density and composition along the
saturation curve.

One cycle is one molecular dynamics run followed by one Monte Carlo run, and
`total_cycles_namd_gomc_sims` sets the number of cycles.

## How to Run

Run the py-MCMD program from this example directory:

```bash
python <path-to-py-MCMD>/py_mcmd_refactored/cli/main.py -f user_input_NAMD_GOMC.json
```

Replace `<path-to-py-MCMD>` with the location of your py-MCMD checkout (for
example, `~/py-MCMD`).

### Command Line Options
- `-f`, `--file`: Path to the JSON input file (default: `user_input_NAMD_GOMC.json`).
- `-namd_sims_order`, `--namd_simulation_order`: Override the JSON `namd_simulation_order` (`series` or `parallel`); only relevant when molecular dynamics is run on both boxes.
- `--dry_run`: Write the NAMD and GOMC control files and run the orchestration logic without executing the NAMD or GOMC binaries.
- `-v`, `--verbose`: Enable debug logging.

## System Setup

The `required_data/input/` directory provides the coordinate (`.pdb`) and
topology (`.psf`) files for both boxes:
- Box 0 (liquid): `required_data/input/C4A-C1OH_nvt_BOX_0_restart.pdb` and `.psf`
- Box 1 (vapor): `required_data/input/C4A-C1OH_nvt_BOX_1_restart.pdb` and `.psf`

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GEMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin; this example runs at `500`.
- `only_use_box_0_for_namd_for_gemc`: Run molecular dynamics on Box 0 only (`true`) or on both boxes (`false`).
- `namd_simulation_order`: Order for the two NAMD runs when both boxes use molecular dynamics (`"series"` or `"parallel"`).
- `total_cycles_namd_gomc_sims`: Number of MD/MC cycles to run (`10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of molecular dynamics timesteps performed in each cycle (default: `1000`).
- `gomc_run_steps`: Number of Monte Carlo moves performed in each cycle (default: `200`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to the Box 0 NAMD run (`4`).
- `no_core_box_1`: CPU cores allocated to the Box 1 NAMD run (`0` when Box 0 only).
- `starting_ff_file_list_gomc`: GOMC force field parameter files (`["required_data/input/TraPPE_FF.inp"]`).
- `starting_ff_file_list_namd`: NAMD force field parameter files (`["required_data/input/TraPPE_FF.inp"]`).
- `namd2_bin_directory`: Directory containing the `namd2` executable.
- `gomc_bin_directory`: Directory containing the `GOMC_CPU_GEMC` executable.

## Simulation Results

- **Expected liquid density**: TBD
- **Expected gas density**: TBD
