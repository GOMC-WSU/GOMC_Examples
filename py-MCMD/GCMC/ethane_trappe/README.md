# Ethane (TraPPE-UA) GCMC Example

Hybrid MD/MC simulation of ethane using the TraPPE united-atom force field in the
grand canonical ensemble with a chemical potential of -3500 K and a temperature of
220 K.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```text
GCMC/ethane_trappe/
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

Molecular dynamics is performed in the canonical (NVT) ensemble and is used to
sample configurational and conformational degrees of freedom.

Monte Carlo insertion and deletion moves are performed at constant chemical
potential and temperature.

Box 0 holds the ethane system; Box 1 is the ideal-gas reservoir that supplies and
accepts molecules during the insertion and deletion moves. One cycle is one
molecular dynamics run followed by one Monte Carlo run, and
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
- `--dry_run`: Write the NAMD and GOMC control files and run the orchestration logic without executing the NAMD or GOMC binaries.
- `-v`, `--verbose`: Enable debug logging.

## System Setup

The `required_data/input/` directory provides the coordinate (`.pdb`) and
topology (`.psf`) files for the system and the reservoir:
- Box 0 (system): `required_data/input/ethane_liq.pdb` and `ethane_liq.psf`
- Box 1 (reservoir): `required_data/input/ethane_vap.pdb` and `ethane_vap.psf`

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"GCMC"`).
- `simulation_temp_k`: Simulation temperature in Kelvin; this example runs at `220.0`.
- `total_cycles_namd_gomc_sims`: Number of MD/MC cycles to run (`10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of molecular dynamics timesteps performed in each cycle (default: `1000`).
- `gomc_run_steps`: Number of Monte Carlo moves performed in each cycle (default: `500`).

### Ensemble Parameters
- `GCMC_ChemPot_or_Fugacity`: Defines whether GOMC uses chemical potential or fugacity as input (`"ChemPot"`).
- `GCMC_ChemPot_or_Fugacity_dict`: Chemical potential (K) or fugacity (bar) per residue type; this example uses `{"NDE": -3500.0}`.

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to the Box 0 NAMD run (`4`).
- `starting_ff_file_list_gomc`: GOMC force field parameter files (`["required_data/input/ethane_FF_trappe_gomc.inp"]`).
- `starting_ff_file_list_namd`: NAMD force field parameter files (`["required_data/input/ethane_FF_trappe_namd.inp"]`).
- `starting_pdb_box_0_file` / `starting_psf_box_0_file`: Box 0 coordinates and topology.
- `starting_pdb_box_1_file` / `starting_psf_box_1_file`: Box 1 coordinates and topology.
- `namd2_bin_directory`: Directory containing the `namd2` executable.
- `gomc_bin_directory`: Directory containing the `GOMC_CPU_GCMC` executable.

## Simulation Results

- **Expected liquid density**: 507.5901 kg/m³ (220 K)
