# Ethane (TraPPE-UA) Simulation Example (GEMC)

Hybrid NAMD/GOMC simulation of an ethane vapor-liquid phase coexistence system using the TraPPE United-Atom force field in the Gibbs Ensemble Monte Carlo (GEMC) ensemble.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```
GEMC/ethane_trappe/
├── user_input_NAMD_GOMC.json    # Main JSON input configuration file
├── README.md                    # Example documentation
└── required_data/               # Force fields and coordinate/topology inputs
    ├── config_files/            # NAMD (.conf) and GOMC (.conf) template scripts
    ├── input/                   # Force field (.inp) and PDB/PSF files
    └── bin/                     # Trajectory processing utilities (catdcd)
```

## Simulation Overview

In this GEMC simulation, liquid ethane (Box 0) and vapor ethane (Box 1) undergo coupled Monte Carlo molecule transfers, volume exchanges, and MD integration steps at constant temperature (280.0 K):

1. **NAMD Execution**: Computes molecular dynamics integration steps in Box 0.
2. **GOMC Execution**: Performs Monte Carlo molecule swap and volume exchange moves between Box 0 and Box 1.
3. **Orchestrator Control**: Coordinates state transfer between engines across simulation cycles.

## How to Run

Execute the refactored CLI script from the main `py-MCMD` directory:

```bash
python py_mcmd_refactored/cli/main.py -f GEMC/ethane_trappe/user_input_NAMD_GOMC.json
```

### Command Line Options

- `-f`, `--file`: Path to JSON input file (default: `user_input_NAMD_GOMC.json`).
- `-r`, `--restart`: Resume from a specific cycle index.
- `-t`, `--test`: Run in dry-run/validation mode.

## System Setup

The `required_data/input/` directory provides pre-configured coordinate (`.pdb`) and topology (`.psf`) files for both phases:
- Box 0 (Liquid): `required_data/input/ethane_liq.pdb` & `required_data/input/ethane_liq.psf`
- Box 1 (Vapor): `required_data/input/ethane_vap.pdb` & `required_data/input/ethane_vap.psf`

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GEMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `280.0`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `200`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to NAMD for Box 0 (default: `4`).
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/ethane_FF_trappe_gomc.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/ethane_FF_trappe_namd.inp"]`).
- `starting_pdb_box_0_file`: Box 0 initial coordinates (`"required_data/input/ethane_liq.pdb"`).
- `starting_psf_box_0_file`: Box 0 initial topology (`"required_data/input/ethane_liq.psf"`).
- `starting_pdb_box_1_file`: Box 1 initial coordinates (`"required_data/input/ethane_vap.pdb"`).
- `starting_psf_box_1_file`: Box 1 initial topology (`"required_data/input/ethane_vap.psf"`).
- `namd2_bin_directory`: Path to directory containing the `namd2` executable.
- `gomc_bin_directory`: Path to directory containing the `GOMC_CPU_GEMC` executable.

## Simulation Results

When the simulation converges, the expected density results are as follows:
- **Expected Liquid Density**: TBD
- **Expected Gas Density**: TBD
