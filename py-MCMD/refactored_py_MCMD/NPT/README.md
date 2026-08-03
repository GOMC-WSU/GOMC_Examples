# py-MCMD NPT Simulation Example

Hybrid NAMD/GOMC simulation of liquid OPC water in the Isobaric-Isothermal (NPT) ensemble.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```text
NPT/
├── user_input_NAMD_GOMC.json    # Main JSON input configuration file
├── README.md                    # Example documentation
└── required_data/               # Force fields, template files, and coordinate/topology inputs
    ├── config_files/            # NAMD (.conf) and GOMC (.conf) template scripts
    ├── input/                   # Force fields and PDB/PSF files for 1K, 10K, and 100K systems
    └── bin/                     # Trajectory processing utilities (catdcd)
```

## Simulation Overview

This example simulates a single-box liquid OPC water system at constant pressure (1.0 bar) and temperature (300 K):
- **GOMC** handles Monte Carlo volume perturbations to sample density fluctuations and maintain pressure, alongside translation/rotation moves.
- **NAMD** performs Molecular Dynamics integration to equilibrate atomic positions and velocities under constant pressure and temperature.

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

Since NPT is a single-box simulation, `starting_pdb_box_1_file` and `starting_psf_box_1_file` are set to `null`.

The default `user_input_NAMD_GOMC.json` file is configured for 1,000 molecules at 300 K. To run a different system size, change the input file paths in `user_input_NAMD_GOMC.json`:

### 1,000 Molecules (`N_1000` @ 300 K) — Default
```json
"starting_pdb_box_0_file": "required_data/input/N_1000/NPT_inputs/300K/NPT_OPC_T300_N1000.pdb",
"starting_psf_box_0_file": "required_data/input/N_1000/NPT_inputs/300K/NPT_OPC_T300_N1000.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

### 10,000 Molecules (`N_10000` @ 300 K)
```json
"starting_pdb_box_0_file": "required_data/input/N_10000/NPT_inputs/300K/NPT_OPC_T300_N10000.pdb",
"starting_psf_box_0_file": "required_data/input/N_10000/NPT_inputs/300K/NPT_OPC_T300_N10000.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

### 100,000 Molecules (`N_100000` @ 300 K)
```json
"starting_pdb_box_0_file": "required_data/input/N_100000/NPT_inputs/300K/NPT_opc_N100000_box0.pdb",
"starting_psf_box_0_file": "required_data/input/N_100000/NPT_inputs/300K/NPT_opc_N100000_box0.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"NPT"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `300`).
- `simulation_pressure_bar`: Target pressure in bar (default: `1.0`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `200`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to NAMD for Box 0 (default: `4`).
- `no_core_box_1`: Set to `0` for single-box NPT simulations.
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/OPC_FF_GOMC.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/OPC_FF_NAMD.inp"]`).
- `namd2_bin_directory`: Path to directory containing the `namd2` executable.
- `gomc_bin_directory`: Path to directory containing the `GOMC_CPU_NPT` executable.
