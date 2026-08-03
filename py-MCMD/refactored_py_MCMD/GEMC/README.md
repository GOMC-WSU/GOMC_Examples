# py-MCMD GEMC Simulation Example

Hybrid NAMD/GOMC simulation of vapor-liquid phase equilibrium for OPC water in the Gibbs (GEMC) ensemble.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```text
GEMC/
├── user_input_NAMD_GOMC.json    # Main JSON input configuration file
├── README.md                    # Example documentation
└── required_data/               # Force fields, template files, and coordinate/topology inputs
    ├── config_files/            # NAMD (.conf) and GOMC (.conf) template scripts
    ├── input/                   # Force fields and PDB/PSF files for 1K, 10K, and 100K systems
    └── bin/                     # Trajectory processing utilities (catdcd)
```

## Simulation Overview

This example simulates vapor-liquid phase coexistence of an OPC water system using two simulation boxes:
- **Box 0**: Liquid phase.
- **Box 1**: Vapor phase.

In this hybrid setup:
- **GOMC** handles molecule transfers between boxes, volume exchanges between boxes to maintain pressure equilibrium, and translation/rotation moves.
- **NAMD** performs Molecular Dynamics relaxation steps on Box 0 between Monte Carlo cycles to efficiently sample dense liquid configurations.

One cycle (`total_cycles_namd_gomc_sims`) consists of one NAMD run followed by one GOMC run.

## How to Run

Run the simulation from this directory using:

```bash
python ~/py-MCMD/py_mcmd_refactored/cli/main.py -f user_input_NAMD_GOMC.json
```

Or using the installed package module:

```bash
python -m py_mcmd_refactored.cli.main -f user_input_NAMD_GOMC.json
```

### Command Line Options
- `-f`, `--file`: Path to JSON input file (default: `user_input_NAMD_GOMC.json`).
- `--dry_run`: Validates input settings and generates configuration files without launching NAMD/GOMC binaries.
- `-v`, `--verbose`: Enables debug logging.

## System Size Setup

The `required_data/input/` directory provides pre-configured coordinate (`.pdb`) and topology (`.psf`) files for three system sizes:
- **1,000 Molecules (`N_1000`)** — Default
- **10,000 Molecules (`N_10000`)**
- **100,000 Molecules (`N_100000`)**

The default `user_input_NAMD_GOMC.json` file is configured for 1,000 molecules at 350 K. To run a different system size, change the input file paths in `user_input_NAMD_GOMC.json`:

### 1,000 Molecules (`N_1000` @ 350 K) — Default
```json
"simulation_temp_k": 350,
"starting_pdb_box_0_file": "required_data/input/N_1000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_0.pdb",
"starting_psf_box_0_file": "required_data/input/N_1000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_0.psf",
"starting_pdb_box_1_file": "required_data/input/N_1000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_1.pdb",
"starting_psf_box_1_file": "required_data/input/N_1000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_1.psf"
```

### 10,000 Molecules (`N_10000` @ 350 K)
```json
"simulation_temp_k": 350,
"starting_pdb_box_0_file": "required_data/input/N_10000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_0.pdb",
"starting_psf_box_0_file": "required_data/input/N_10000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_0.psf",
"starting_pdb_box_1_file": "required_data/input/N_10000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_1.pdb",
"starting_psf_box_1_file": "required_data/input/N_10000/GEMC_inputs/350K/GEMC_OPC_T350_N1000_BOX_1.psf"
```

### 100,000 Molecules (`N_100000` @ 350 K)
```json
"simulation_temp_k": 350,
"starting_pdb_box_0_file": "required_data/input/N_100000/GEMC_inputs/350K/GEMC_opc_N100000_T350_box0.pdb",
"starting_psf_box_0_file": "required_data/input/N_100000/GEMC_inputs/350K/GEMC_opc_N100000_T350_box0.psf",
"starting_pdb_box_1_file": "required_data/input/N_100000/GEMC_inputs/350K/GEMC_opc_N100000_T350_box1.pdb",
"starting_psf_box_1_file": "required_data/input/N_100000/GEMC_inputs/350K/GEMC_opc_N100000_T350_box1.psf"
```

*(Note: Input files for 500 K are also provided in the `500K/` subfolders. To run at 500 K, set `"simulation_temp_k": 500` and use the 500K file paths).*

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GEMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `350`).
- `only_use_box_0_for_namd_for_gemc`: Set to `true` to run NAMD on Box 0 only, or `false` for both boxes.
- `namd_simulation_order`: Execution order when running two NAMD boxes (`"series"` or `"parallel"`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `200`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to NAMD for Box 0 (default: `4`).
- `no_core_box_1`: CPU cores allocated to NAMD for Box 1 (`0` when Box 0 only).
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/OPC_FF_GOMC.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/OPC_FF_NAMD.inp"]`).
- `namd2_bin_directory`: Path to directory containing the `namd2` executable.
- `gomc_bin_directory`: Path to directory containing the `GOMC_CPU_GEMC` executable.
