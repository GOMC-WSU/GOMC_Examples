# Ethane (TraPPE-UA) Simulation Example (GCMC)

Hybrid NAMD/GOMC simulation of an ethane adsorption/chemical potential system using the TraPPE United-Atom force field in the Grand Canonical (GCMC) ensemble.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```
GCMC/ethane_trappe/
├── user_input_NAMD_GOMC.json    # Main JSON input configuration file
├── README.md                    # Example documentation
└── required_data/               # Force fields and coordinate/topology inputs
    ├── config_files/            # NAMD (.conf) and GOMC (.conf) template scripts
    ├── input/                   # Force field (.inp) and PDB/PSF files
    └── bin/                     # Trajectory processing utilities (catdcd)
```

## Simulation Overview

In this GCMC simulation, ethane molecules (TraPPE-UA model) are inserted and deleted in Box 0 at a fixed chemical potential (`{"NDE": -3500.0}`) and temperature (280.0 K):

1. **NAMD Execution**: Computes molecular dynamics integration steps in Box 0.
2. **GOMC Execution**: Performs Grand Canonical Monte Carlo insertion and deletion moves.
3. **Orchestrator Control**: Coordinates data transfer between engines across simulation cycles.

## How to Run

Execute the refactored CLI script from the main `py-MCMD` directory:

```bash
python py_mcmd_refactored/cli/main.py -f GCMC/ethane_trappe/user_input_NAMD_GOMC.json
```

### Command Line Options

- `-f`, `--file`: Path to JSON input file (default: `user_input_NAMD_GOMC.json`).
- `-r`, `--restart`: Resume from a specific cycle index.
- `-t`, `--test`: Run in dry-run/validation mode.

## System Setup

The `required_data/input/` directory provides pre-configured coordinate (`.pdb`) and topology (`.psf`) files for both system and reservoir:
- Box 0 (System): `required_data/input/ethane_liq.pdb` & `required_data/input/ethane_liq.psf`
- Box 1 (Reservoir): `required_data/input/ethane_vap.pdb` & `required_data/input/ethane_vap.psf`

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GCMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `280.0`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `500`).

### Ensemble Parameters
- `GCMC_ChemPot_or_Fugacity`: Control mode for molecule transfers (`"ChemPot"`).
- `GCMC_ChemPot_or_Fugacity_dict`: Chemical potential value per residue type (default: `{"NDE": -3500.0}`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to NAMD for Box 0 (default: `4`).
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/ethane_FF_trappe_gomc.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/ethane_FF_trappe_namd.inp"]`).
- `starting_pdb_box_0_file`: Box 0 initial coordinates (`"required_data/input/ethane_liq.pdb"`).
- `starting_psf_box_0_file`: Box 0 initial topology (`"required_data/input/ethane_liq.psf"`).
- `starting_pdb_box_1_file`: Box 1 initial coordinates (`"required_data/input/ethane_vap.pdb"`).
- `starting_psf_box_1_file`: Box 1 initial topology (`"required_data/input/ethane_vap.psf"`).
- `namd2_bin_directory`: Path to directory containing the `namd2` executable.
- `gomc_bin_directory`: Path to directory containing the `GOMC_CPU_GCMC` executable.

## Simulation Results

When the simulation converges, the expected density results are as follows:
- **Expected Liquid Density**: TBD
- **Expected Gas Density**: TBD
