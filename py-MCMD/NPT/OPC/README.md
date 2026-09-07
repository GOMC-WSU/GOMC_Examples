# OPC Water NPT Example

Hybrid MD/MC simulation of liquid OPC water in the isothermal-isobaric (NPT)
ensemble at a temperature of 300 K and a pressure of 1 bar, giving the equilibrium
liquid density.

Repository: https://github.com/GOMC-WSU/py-MCMD.git

## Directory Structure

```text
NPT/OPC/
├── user_input_NAMD_GOMC.json    # JSON input for this example
├── README.md
└── required_data/
    ├── config_files/            # NAMD and GOMC control-file templates
    ├── input/                   # Force fields and coordinate/topology files for the 1K, 10K, and 100K systems
    └── bin/                     # catdcd trajectory utility
```

## Simulation Overview

The simulation proceeds through a series of alternating molecular dynamics time
steps and Monte Carlo moves.

Molecular dynamics is performed in the canonical (NVT) ensemble and is used to
sample configurational and conformational degrees of freedom.

Monte Carlo volume moves are performed at constant pressure and temperature, so
the single box relaxes to its equilibrium density.

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
- `--dry_run`: Write the NAMD and GOMC control files and run the orchestration logic without executing the NAMD or GOMC binaries.
- `-v`, `--verbose`: Enable debug logging.

## System Size Setup

The `required_data/input/` directory provides coordinate (`.pdb`) and topology
(`.psf`) files for three system sizes, all at 300 K:
- **1,000 molecules (`N_1000`)** — used by `user_input_NAMD_GOMC.json`
- **10,000 molecules (`N_10000`)**
- **100,000 molecules (`N_100000`)**

NPT is a single-box simulation, so `starting_pdb_box_1_file` and
`starting_psf_box_1_file` are set to `null`. To run a different system size,
change the input file paths in `user_input_NAMD_GOMC.json`:

### 1,000 molecules (`N_1000`)
```json
"starting_pdb_box_0_file": "required_data/input/N_1000/NPT_OPC_T300_N1000.pdb",
"starting_psf_box_0_file": "required_data/input/N_1000/NPT_OPC_T300_N1000.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

### 10,000 molecules (`N_10000`)
```json
"starting_pdb_box_0_file": "required_data/input/N_10000/NPT_OPC_T300_N10000.pdb",
"starting_psf_box_0_file": "required_data/input/N_10000/NPT_OPC_T300_N10000.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

### 100,000 molecules (`N_100000`)
```json
"starting_pdb_box_0_file": "required_data/input/N_100000/NPT_opc_N100000_box0.pdb",
"starting_psf_box_0_file": "required_data/input/N_100000/NPT_opc_N100000_box0.psf",
"starting_pdb_box_1_file": null,
"starting_psf_box_1_file": null
```

## Input Parameters (`user_input_NAMD_GOMC.json`)

### Simulation Controls
- `simulation_type`: Ensemble type (`"NPT"`).
- `simulation_temp_k`: Simulation temperature in Kelvin; this example runs at `300`.
- `simulation_pressure_bar`: Simulation pressure in bar; this example runs at `1.0`.
- `total_cycles_namd_gomc_sims`: Number of MD/MC cycles to run (`10`).
- `starting_at_cycle_namd_gomc_sims`: Starting cycle index (`0` for a new run, `>0` to resume).
- `namd_run_steps`: Number of molecular dynamics timesteps performed in each cycle (default: `1000`).
- `gomc_run_steps`: Number of Monte Carlo moves performed in each cycle (default: `20`).

### Compute & Binary Paths
- `no_core_box_0`: CPU cores allocated to the Box 0 NAMD run (`4`).
- `no_core_box_1`: Set to `0` for single-box NPT simulations.
- `starting_ff_file_list_gomc`: GOMC force field parameter files (`["required_data/input/OPC_FF_GOMC.inp"]`).
- `starting_ff_file_list_namd`: NAMD force field parameter files (`["required_data/input/OPC_FF_NAMD.inp"]`).
- `namd2_bin_directory`: Directory containing the `namd2` executable.
- `gomc_bin_directory`: Directory containing the `GOMC_CPU_NPT` executable.

## Simulation Results

- **Expected liquid density**: 996.28 kg/m³
