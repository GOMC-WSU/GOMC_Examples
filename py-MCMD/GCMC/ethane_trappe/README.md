# Ethane (TraPPE-UA) Simulation Example (GCMC)

Hybrid NAMD/GOMC simulation of an ethane system using the TraPPE United-Atom force field in the GCMC ensemble.

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

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GCMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin (default: `280.0`).
- `total_cycles_namd_gomc_sims`: Total number of coupled NAMD and GOMC cycles (default: `10`).
- `namd_run_steps`: Number of MD integration steps NAMD runs per cycle (default: `1000`).
- `gomc_run_steps`: Number of MC moves GOMC runs per cycle (default: `500`).

### Compute & Binary Paths
- `starting_ff_file_list_gomc`: Force field parameter files for GOMC (`["required_data/input/ethane_FF_trappua_gomc.inp"]`).
- `starting_ff_file_list_namd`: Force field parameter files for NAMD (`["required_data/input/ethane_FF_trappua_namd.inp"]`).
- `starting_pdb_box_0_file`: Box 0 initial coordinates (`"required_data/input/ethane_liq.pdb"`).
- `starting_psf_box_0_file`: Box 0 initial topology (`"required_data/input/ethane_liq.psf"`).

## Simulation Results

When the simulation converges, the expected density results are as follows:
- **Expected Liquid Density**: TBD
- **Expected Gas Density**: TBD
