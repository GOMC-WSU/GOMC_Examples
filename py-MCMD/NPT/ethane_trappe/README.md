# Ethane (TraPPE-UA) Simulation Example (NPT)

Hybrid NAMD/GOMC simulation of a liquid ethane system using the TraPPE United-Atom force field in the Isobaric-Isothermal (NPT) ensemble.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```
NPT/ethane_trappe/
├── user_input_NAMD_GOMC.json    # Main JSON input configuration file
├── README.md                    # Example documentation
└── required_data/               # Force fields and coordinate/topology inputs
    ├── config_files/            # NAMD (.conf) and GOMC (.conf) template scripts
    ├── input/                   # Force field (.inp) and PDB/PSF files
    └── bin/                     # Trajectory processing utilities (catdcd)
```

## Simulation Overview

In this NPT simulation, liquid ethane (TraPPE-UA model) is simulated at a constant temperature (280.0 K) and pressure (5.0 bar) to compute liquid-phase properties:

1. **NAMD Execution**: Computes molecular dynamics integration steps in Box 0.
2. **GOMC Execution**: Performs Monte Carlo volume changes to maintain constant pressure.
3. **Orchestrator Control**: Coordinates data transfer between engines across simulation cycles.

## How to Run

Execute the refactored CLI script from the main `py-MCMD` directory:

```bash
python py_mcmd_refactored/cli/main.py -f NPT/ethane_trappe/user_input_NAMD_GOMC.json
```

### Command Line Options

- `-f`, `--file`: Path to JSON input file (default: `user_input_NAMD_GOMC.json`).
- `-r`, `--restart`: Resume from a specific cycle index.
- `-t`, `--test`: Run in dry-run/validation mode.

## System Setup

The `required_data/input/` directory provides pre-configured coordinate (`.pdb`) and topology (`.psf`) files for the system:
- Box 0 (Liquid): `required_data/input/ethane_liq.pdb` & `required_data/input/ethane_liq.psf`

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"NPT"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `280.0`).
- `simulation_pressure_bar`: Simulation pressure in bar (default: `5.0`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `20`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to NAMD for Box 0 (default: `4`).
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/ethane_FF_trappe_gomc.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/ethane_FF_trappe_namd.inp"]`).
- `starting_pdb_box_0_file`: Box 0 initial coordinates (`"required_data/input/ethane_liq.pdb"`).
- `starting_psf_box_0_file`: Box 0 initial topology (`"required_data/input/ethane_liq.psf"`).
- `namd2_bin_directory`: Path to directory containing the `namd2` executable.
- `gomc_bin_directory`: Path to directory containing the `GOMC_CPU_NPT` executable.

## Simulation Results

When the simulation converges, the expected density results are as follows:
- **Expected Liquid Density**: TBD
- **Expected Gas Density**: —
