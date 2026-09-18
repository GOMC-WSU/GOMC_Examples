"""GOMC's setup for signac, signac-flow, signac-dashboard for this study."""
# project.py

import os
import subprocess

import flow

import mbuild as mb
import mosdef_gomc.formats.gmso_charmm_writer as mf_charmm
import mosdef_gomc.formats.gmso_gomc_conf_writer as gomc_control
import numpy as np
import signac
import unyt as u
import pandas as pd
import math
import shutil
from scipy import stats
from flow import FlowProject, aggregator
from flow.environment import DefaultSlurmEnvironment


class Project(FlowProject):
    """Subclass of FlowProject to provide custom methods and attributes."""

    def __init__(self):
     	super().__init__()

class Grid(DefaultSlurmEnvironment):  # Grid(StandardEnvironment):
    """Subclass of DefaultSlurmEnvironment for WSU's Grid cluster."""
    
    #uncomment for Grid
    #hostname_pattern = r".*\.grid\.wayne\.edu"
    #template = "grid.sh"
    template = "local.sh"




# ******************************************************
# users typical variables, but not all (start)
# ******************************************************
# set binary path to gomc binary files (the bin folder).
# If the gomc binary files are callable directly from the terminal without a path,
# please just enter and empty string (i.e., "" or '')

# Enter the GOMC binary path here (MANDATORY INFORMAION)
gomc_binary_path = "~/GOMC/tabulated/GOMC/bin"


# number of simulation steps
gomc_steps_nvt_equilibration =10000000 # pre-equilibrate system without swap moves.
gomc_steps_equilibration = 50000000 #  set value for paper = 60 * 10**6
gomc_steps_production = 50000000 # set value for paper = 60 * 10**6
console_output_freq = 100000 # Monte Carlo Steps between console output
pressure_calc_freq = 1000 # Monte Carlo Steps for pressure calculation
block_ave_output_freq = 10000000 # Monte Carlo Steps between console output
coordinate_output_freq = 10000000 # # set value for paper = 50 * 10**3
EqSteps = 1000000 # MCS for equilibration
AdjSteps = 1000 #MCS for adjusting max displacement, rotation, volume, etc.

# number of simulation steps
#gomc_steps_equilb_design_ensemble = 60 * 10**6 #  set value for paper = 60 * 10**6
#gomc_steps_production = 60 * 10**6 # set value for paper = 60 * 10**6

gomc_output_data_every_X_steps = 50 * 10**3 # # set value for paper = 50 * 10**3

# force field (FF) file for all simulations in that job
# Note: do not add extensions
gomc_ff_filename_str = "TRAPPE_FF"
gomc_tabulated_ff_filename="alkane_table_01.inp"

# initial mosdef structure and coordinates
# Note: do not add extensions
mosdef_structure_box_0_name_str = "initial_box_0"
mosdef_structure_box_1_name_str = "initial_box_1"

# NVT preequilibration to help stabilize GEMC simulations
gomc_nvt_equilb_control_file_name_str = "GEMC_nvt"
gomc_nvt_equilb_output_name_str="C2A_nvt"

# The equilb using the ensemble used for the simulation design, which
# includes the simulation runs GOMC control file input and simulation outputs
# Note: do not add extensions
gomc_equilb_control_file_name_str = "GEMC_equil"
gomc_equilb_output_name_str="C2A_equil"

# The production run using the ensemble used for the simulation design, which
# includes the simulation runs GOMC control file input and simulation outputs
# Note: do not add extensions
gomc_production_control_file_name_str = "GEMC_prod"
gomc_production_output_name_str="C2A_prod"

# The equilb using the ensemble used for the simulation design, which
# includes the simulation runs GOMC control file input and simulation outputs
# Note: do not add extensions
#gomc_equilb_design_ensemble_control_file_name_str = "gomc_equilb_design_ensemble"

# The production run using the ensemble used for the simulation design, which
# includes the simulation runs GOMC control file input and simulation outputs
# Note: do not add extensions
#gomc_production_control_file_name_str = "gomc_production_run"

# Analysis (each replicates averages):
# Output text (txt) file names for each replicates averages
# directly put in each replicate folder (.txt, .dat, etc)
output_replicate_txt_file_name_liq = "avg_data_box_liq.txt"
output_replicate_txt_file_name_vap = "avg_data_box_vap.txt"

# Analysis (averages and std. devs. of  # all the replcates): 
# Output text (txt) file names for the averages and std. devs. of all the replcates, 
# including the extention (.txt, .dat, etc)
output_avg_std_of_replicates_txt_file_name_liq = "avg_over_replicates_box_liq.txt"
output_avg_std_of_replicates_txt_file_name_vap = "avg_over_replicates_box_vap.txt"

# Analysis (Critical and boiling point values):
# Output text (txt) file name for the Critical and Boiling point values of the system using the averages
# and std. devs. all the replcates, including the extention (.txt, .dat, etc)
output_critical_data_replicate_txt_file_name = "critical_points_all_replicates.txt"
output_critical_data_avg_std_of_replicates_txt_file_name = "critical_point_avg_over_replicates.txt"

output_boiling_data_replicate_txt_file_name = "boiling_point_all_replicates.txt"
output_boiling_data_avg_std_of_replicates_txt_file_name = "boiling_point_avg_over_replicates.txt"


walltime_mosdef_hr = 24
walltime_gomc_equilbrium_hr = 168
walltime_gomc_production_hr = 168
walltime_gomc_analysis_hr = 4
memory_needed = 1

# ******************************************************
# users typical variables, but not all (end)
# ******************************************************


# ******************************************************
# signac and GOMC-MOSDEF code (start)
# ******************************************************

# ******************************************************
# ******************************************************
# create some initial variable to be store in each jobs
# directory in an additional json file, and test
# to see if they are written (start).
# ******************************************************
# ******************************************************

# set the default directory
project_directory_path = str(os.getcwd())
print("project_directory_path = " +str(project_directory_path))


@Project.label
def part_1a_initial_data_input_to_json(job):
    """Check that the initial job data is written to the json files."""
    data_written_bool = False
    if job.isfile(f"{'signac_job_document.json'}"):
     	data_written_bool = True

    return data_written_bool


@Project.post(part_1a_initial_data_input_to_json)
@Project.operation(directives=
    {
     	"np": 1,
     	"ngpu": 0,
     	"memory": memory_needed,
     	"walltime": walltime_mosdef_hr,
    }, with_job=True
)
def initial_parameters(job):
    """Set the initial job parameters into the jobs doc json file."""
    # select

    # set free energy data in doc
    # Free energy calcs
    # lamda generator

    # list replica seed numbers
    replica_no_to_seed_dict = {
     	0: 0,
     	1: 1,
     	2: 2,
     	3: 3,
     	4: 4,
     	5: 5,
     	6: 6,
     	7: 7,
     	8: 8,
     	9: 9,
     	10: 10,
     	11: 11,
     	12: 12,
     	13: 13,
     	14: 14,
     	15: 15,
     	16: 16,
     	17: 17,
     	18: 18,
     	19: 19,
     	20: 20,
    }

    job.doc.replica_number_int = replica_no_to_seed_dict.get(
     	int(job.sp.replica_number_int)
    )

    # gomc core and CPU or GPU
    job.doc.gomc_ncpu = 4  # 4 is optimal for water
    job.doc.gomc_ngpu = 0

    # get the gomc binary paths
    if job.doc.gomc_ngpu == 0:
     	job.doc.gomc_cpu_or_gpu = "CPU"

    elif job.doc.gomc_ngpu == 1:
     	job.doc.gomc_cpu_or_gpu = "GPU"

    else:
     	raise ValueError(
     	    "The GOMC CPU and GPU can not be determined as force field (FF) is not available in the selection, "
     	    "or GPU selection is is not 0 or 1."
     	)

    # only for GEMC-NVT
    job.doc.gomc_equilb_design_ensemble_gomc_binary_file = f"GOMC_{job.doc.gomc_cpu_or_gpu}_GEMC"
    job.doc.gomc_production_ensemble_gomc_binary_file = f"GOMC_{job.doc.gomc_cpu_or_gpu}_GEMC"


# ******************************************************
# ******************************************************
# create some initial variable to be store in each jobs
# directory in an additional json file, and test
# to see if they are written (end).
# ******************************************************
# ******************************************************


# ******************************************************
# ******************************************************
# functions for selecting/grouping/aggregating in different ways (start)
# ******************************************************
# ******************************************************

def statepoint_without_replica(job):
    keys = sorted(tuple(i for i in job.sp.keys() if i not in {"replica_number_int"}))
    return [(key, job.sp[key]) for key in keys]

def statepoint_without_temperature(job):
    keys = sorted(tuple(i for i in job.sp.keys() if i not in {"production_temperature_K"}))
    return [(key, job.sp[key]) for key in keys]

# ******************************************************
# ******************************************************
# functions for selecting/grouping/aggregating in different ways (end)
# ******************************************************
# ******************************************************

# ******************************************************
# ******************************************************
# check if GOMC psf, pdb, and force field (FF) files were written (start)
# ******************************************************
# ******************************************************

# check if GOMC-MOSDEF wrote the gomc files
@Project.label
def mosdef_input_written(job):
    """Check that the mosdef files (psf, pdb, and force field (FF) files) are written ."""
    file_written_bool = False
    if (
     	job.isfile(f"{gomc_ff_filename_str}.inp")
     	and job.isfile(
     	    f"{mosdef_structure_box_0_name_str}.psf"
     	)
     	and job.isfile(
     	    f"{mosdef_structure_box_0_name_str}.pdb"
     	)
    ):
     	file_written_bool = True

    return file_written_bool

@Project.label
def tabulated_file_copied(job):
    """Check if tabulated potential file exists"""
    file_written_bool = False
    if job.isfile(f"{gomc_tabulated_ff_filename}"):
        file_written_bool = True
    else:
        file_written_bool = False
       
    return file_written_bool

# ******************************************************
# ******************************************************
# check if GOMC psf, pdb, and FF files were written (end)
# ******************************************************
# ******************************************************

# ******************************************************
# ******************************************************
# check if GOMC control file was written (start)
# ******************************************************
# ******************************************************
# function for checking if the GOMC control file is written
def gomc_control_file_written(job, control_filename_str):
    """General check that the gomc control files are written."""
    file_written_bool = False
    control_file = f"{control_filename_str}.conf"

    if job.isfile(control_file):
        with open(job.fn(control_file), "r") as fp:
            out_gomc = fp.readlines()
            for i, line in enumerate(out_gomc):
                if "OutputName" in line:
                    split_move_line = line.split()
                    if split_move_line[0] == "OutputName":
                        file_written_bool = True

    return file_written_bool

# checking if the GOMC control file is written for the nvt equilb run with the selected ensemble
@Project.label
def part_2a_gomc_nvt_equilb_design_ensemble_control_file_written(job):
    """General check that the gomc_equilb_design_ensemble (run temperature) gomc control file is written."""
    return gomc_control_file_written(job, gomc_nvt_equilb_control_file_name_str)

# checking if the GOMC control file is written for the equilb run with the selected ensemble
@Project.label
def part_2b_gomc_equilb_design_ensemble_control_file_written(job):
    """General check that the gomc_equilb_design_ensemble (run temperature) gomc control file is written."""
    return gomc_control_file_written(job, gomc_equilb_control_file_name_str)


# checking if the GOMC control file is written for the production run
@Project.label
def part_2c_gomc_production_control_file_written(job):
    """General check that the gomc_production_control_file (run temperature) is written."""
    return gomc_control_file_written(job, gomc_production_control_file_name_str)

# ******************************************************
# ******************************************************
# check if GOMC control file was written (end)
# ******************************************************
# ******************************************************

# ******************************************************
# ******************************************************
# check if GOMC simulations started (start)
# ******************************************************
# ******************************************************
# function for checking if GOMC simulations are started
def gomc_simulation_started(job, control_filename_str):
    """General check to see if the gomc simulation is started."""
    output_started_bool = False
    if job.isfile("out_{}.dat".format(control_filename_str)):
     	output_started_bool = True

    return output_started_bool

@Project.label
def part_3a_output_gomc_nvt_equilb_design_ensemble_started(job):
    """Check to see if the gomc_equilb_design_ensemble (set temperature) simulation is started."""
    return gomc_simulation_started(job, gomc_nvt_equilb_control_file_name_str)

# check if equilb_with design ensemble GOMC run is started by seeing if the GOMC consol file and the merged psf exist
@Project.label
def part_3b_output_gomc_equilb_design_ensemble_started(job):
    """Check to see if the gomc_equilb_design_ensemble (set temperature) simulation is started."""
    return gomc_simulation_started(job, gomc_equilb_control_file_name_str)

# check if production GOMC run is started by seeing if the GOMC consol file and the merged psf exist
@Project.label
def part_3c_output_gomc_production_run_started(job):
    """Check to see if the gomc production run (set temperature) simulation is started."""
    return gomc_simulation_started(job, gomc_production_control_file_name_str)

# ******************************************************
# ******************************************************
# check if GOMC simulations started (end)
# ******************************************************
# ******************************************************

# ******************************************************
# ******************************************************
# check if GOMC simulation are completed properly (start)
# ******************************************************
# ******************************************************
# function for checking if GOMC simulations are completed properly
def gomc_sim_completed_properly(job, control_filename_str):
    """General check to see if the gomc simulation was completed properly."""
    job_run_properly_bool = False
    output_log_file = "out_{}.dat".format(control_filename_str)
    if job.isfile(output_log_file):
     	# with open(f"workspace/{job.id}/{output_log_file}", "r") as fp:
     	#print(f"job.id = {job.id}")
     	with open(job.fn(output_log_file), "r") as fp:
     	    out_gomc = fp.readlines()
     	    for i, line in enumerate(out_gomc):
     		    if "Completed" in line:
     		        job_run_properly_bool = True
     	      #  if "Move" in line:
     	      #      split_move_line = line.split()
     	      #      if (
     	      # 	 split_move_line[0] == "Move"
     	      # 	 and split_move_line[1] == "Type"
     	      # 	 and split_move_line[2] == "Mol."
     	      # 	 and split_move_line[3] == "Kind"
     	      #      ):
     	      # 	 job_run_properly_bool = True
    else:
     	job_run_properly_bool = False

    return job_run_properly_bool

# check if equilb selected ensemble GOMC run completed by checking the end of the GOMC consol file
@Project.label
def part_4a_job_gomc_nvt_equilb_design_ensemble_completed_properly(job):
    """Check to see if the gomc_equilb_design_ensemble (set temperature) simulation was completed properly."""
    return gomc_sim_completed_properly(job, gomc_nvt_equilb_control_file_name_str)

@Project.label
def part_4b_job_gomc_equilb_design_ensemble_completed_properly(job):
    """Check to see if the gomc_equilb_design_ensemble (set temperature) simulation was completed properly."""
    return gomc_sim_completed_properly(job, gomc_equilb_control_file_name_str)

# check if production GOMC run completed by checking the end of the GOMC consol file
@Project.label
def part_4c_job_production_run_completed_properly(job):
    """Check to see if the gomc production run (set temperature) simulation was completed properly."""
    return gomc_sim_completed_properly(job, gomc_production_control_file_name_str)

# check if analysis is done for the individual replicates wrote the gomc files
@Project.label
def part_5a_analysis_individual_simulation_averages_completed(job):
    """Check that the individual simulation averages files are written ."""
    file_written_bool = False
    if (
     	job.isfile(
     	    f"{output_replicate_txt_file_name_liq}"
     	)
     	and job.isfile(
     	    f"{output_replicate_txt_file_name_vap}"
     	)
    ):
     	file_written_bool = True

    return file_written_bool


# check if analysis for averages of all the replicates is completed
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
@Project.label
def part_5b_analysis_replica_averages_completed(*jobs):
    """Check that the individual simulation averages files are written ."""
    file_written_bool_list = []
    all_file_written_bool_pass = False
    for job in jobs:
     	file_written_bool = False

     	if (
     	    job.isfile(
     		f"../../analysis/{output_avg_std_of_replicates_txt_file_name_liq}"
     	    )
     	    and job.isfile(
     		f"../../analysis/{output_avg_std_of_replicates_txt_file_name_vap}"
     	    )
     	):
     	    file_written_bool = True

     	file_written_bool_list.append(file_written_bool)

    if False not in file_written_bool_list:
     	all_file_written_bool_pass = True

    return all_file_written_bool_pass

# check if analysis for critical points is completed
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
#@Project.pre(part_5b_analysis_replica_averages_completed)
@Project.label
def part_5c_analysis_critical_and_boiling_points_replicate_data_completed(*jobs):
    """Check that the critical and boiling point replicate file is written ."""
    file_written_bool_list = []
    all_file_written_bool_pass = False
    for job in jobs:
     	file_written_bool = False

     	if (
     	    job.isfile(
     		f"../../analysis/{output_critical_data_replicate_txt_file_name}"
     	    ) \
     		and
     	    job.isfile(
     		f"../../analysis/{output_boiling_data_replicate_txt_file_name}"
     	    )
     	):
     	    file_written_bool = True

     	file_written_bool_list.append(file_written_bool)

    if False not in file_written_bool_list:
     	all_file_written_bool_pass = True

    return file_written_bool

# check if analysis for critical points is completed
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
#@Project.pre(part_5b_analysis_replica_averages_completed)
@Project.label
def part_5d_analysis_critical_and_boiling_points_avg_std_data_completed(*jobs):
    """Check that the avg and std dev critical and boiling point data file is written ."""
    file_written_bool_list = []
    all_file_written_bool_pass = False
    for job in jobs:
     	file_written_bool = False

     	if (
     	    job.isfile(
     		f"../../analysis/{output_critical_data_avg_std_of_replicates_txt_file_name}"
     	    ) \
     		and
     		job.isfile(
     		    f"../../analysis/{output_boiling_data_avg_std_of_replicates_txt_file_name}"
     		)
     	):
     	    file_written_bool = True

     	file_written_bool_list.append(file_written_bool)

    if False not in file_written_bool_list:
     	all_file_written_bool_pass = True

    return file_written_bool


# ******************************************************
# ******************************************************
# check if GOMC simulation are completed properly (end)
# ******************************************************
# ******************************************************

### Copy tabulated potential file
#gomc_tabulated_ff_filename
#@Project.pre(mosdef_input_written)
@Project.post(tabulated_file_copied)
@Project.operation(directives=
    {
        "np": lambda job: 1,
        "ngpu": lambda job: 0,
        "memory": memory_needed,
        "walltime": walltime_gomc_analysis_hr,
    }, with_job=True, cmd=True
)
def copy_tabulated_potential(job):
    """copy tabulated potential."""

    project_root = os.path.abspath(os.path.join(job.path, "../.."))
    source_path = os.path.join(project_root, gomc_tabulated_ff_filename)

    if os.path.exists(source_path):
        shutil.copy(source_path, job.path)
    else:
        # This will show up in your logs so you know why it failed
        print(f"Source file not found: {source_path}")
    return ":"

# ******************************************************
# ******************************************************
# build system, with option to write the force field (force field (FF)), pdb, psf files.
# Note: this is needed to write GOMC control file, even if a restart (start)
# ******************************************************
# build system
def build_charmm(job, write_files=True):
    """Build the Charmm object and potentially write the pdb, psd, and force field (FF) files."""
    print("#**********************")
    print("Started: GOMC Charmm Object")
    print("#**********************")

    box_0_temp_to_length_ang_dict = {290: 50,
                                     270: 48,
                                     250: 46,
                                     242: 46,
                                     240: 46,
                                     220: 45,
                                     200: 45,
                                     180: 44,
                                     }

    box_1_temp_to_length_ang_dict = {290: 40,
                                     270: 49,
                                     250: 59,
                                     242: 64,
                                     240: 65,
                                     220: 80,
                                     200: 105,
                                     180: 140,
                                     }

    box_0_temp_to_molecules_dict = {290: 900,
                                     270: 900,
                                     250: 900,
                                     242: 900,
                                     240: 900,
                                     220: 900,
                                     200: 900,
                                     180: 900,
                                     }

    box_1_temp_to_molecules_dict = { 290: 100,
                                     270: 100,
                                     250: 100,
                                     242: 100,
                                     240: 100,
                                     220: 100,
                                     200: 100,
                                     180: 100,
                                     }
    
    #total_molecules_liquid = 970
    #total_molecules_vapor = 30

    forcefield_files = '../../trappe-tabulated.xml'
    molecule_A = mb.load('../../C2A.mol2')
    molecule_A.name = 'C2A'

    molecule_type_list = [molecule_A]
    mol_fraction_molecule_A = 1.0
    molecule_mol_fraction_list = [mol_fraction_molecule_A]
    fixed_bonds_angles_list = [molecule_A.name]
    residues_list = [molecule_A.name]

    bead_to_atom_name_dict = {'_CH4': 'C', '_CH3': 'C', '_CH2': 'C', '_CH': 'C', '_HC': 'C','_CF4':'C', '_CF3':'C','_CF2':'C'}

    #print('total_molecules_liquid = ' + str(total_molecules_liquid))
    #print('total_molecules_vapor = ' + str(total_molecules_vapor))

    box_0_box_size_ang = box_0_temp_to_length_ang_dict[job.sp.production_temperature_K]
    box_1_box_size_ang = box_1_temp_to_length_ang_dict[job.sp.production_temperature_K]
    box_0_molecules = box_0_temp_to_molecules_dict[job.sp.production_temperature_K]
    box_1_molecules = box_1_temp_to_molecules_dict[job.sp.production_temperature_K]

    print('Running: liquid phase box packing')
    box_liq = mb.fill_box(compound=molecule_type_list,
     			  n_compounds=box_0_molecules,
     			  box=[box_0_box_size_ang/10, box_0_box_size_ang/10, box_0_box_size_ang/10]
     			  )
    #box_liq.energy_minimize(forcefield=forcefield_files,
    #			     steps=10 ** 5
    #			     )
    print('Completed: liquid phase box packing')

    print('Running: vapor phase box packing')
    box_vap = mb.fill_box(compound=molecule_type_list,
     			  n_compounds=box_1_molecules,
     			  box=[box_1_box_size_ang/10, box_1_box_size_ang/10, box_1_box_size_ang/10]
     			  )
    #box_vap.energy_minimize(forcefield=forcefield_files,
    #			     steps=10 ** 5
    #			     )
    print('Completed: vapor phase box packing')

    # calculate the actual molecular packing data
    print('molecule_mol_fraction_list =  ' + str(molecule_mol_fraction_list))

    print('Running: GOMC FF file, and the psf and pdb files')
    gomc_charmm = mf_charmm.Charmm(
     	box_liq,
     	mosdef_structure_box_0_name_str,
     	structure_box_1=box_vap,
     	filename_box_1=mosdef_structure_box_1_name_str,
     	ff_filename=gomc_ff_filename_str,
     	forcefield_selection=forcefield_files,
     	residues=residues_list,
     	bead_to_atom_name_dict=bead_to_atom_name_dict,
     	gomc_fix_bonds_angles=fixed_bonds_angles_list,
    )

    if write_files == True:
     	gomc_charmm.write_inp()

     	gomc_charmm.write_psf()

     	gomc_charmm.write_pdb()

    print('Completed: GOMC FF file, and the psf and pdb files')

    return gomc_charmm


# ******************************************************
# ******************************************************
# build system, with option to write the force field (FF), pdb, psf files.
# Note: this is needed to write GOMC control file, even if a restart (end)
# ******************************************************


# ******************************************************
# ******************************************************
# Creating GOMC files (pdb, psf, force field (FF), and gomc control files (start)
# ******************************************************
# ******************************************************
@Project.pre(part_1a_initial_data_input_to_json)
@Project.post(part_2a_gomc_nvt_equilb_design_ensemble_control_file_written)
@Project.post(part_2b_gomc_equilb_design_ensemble_control_file_written)
@Project.post(part_2c_gomc_production_control_file_written)
@Project.post(mosdef_input_written)
@Project.operation(directives=
    {
     	"np": 1,
     	"ngpu": 0,
     	"memory": memory_needed,
     	"walltime": walltime_mosdef_hr,
    }, with_job=True
)
def build_psf_pdb_ff_gomc_conf(job):
    """Build the Charmm object and write the pdb, psd, and force field (FF) files for all the simulations in the workspace."""
    gomc_charmm_object_with_files = build_charmm(job, write_files=True)

    # ******************************************************
    # common variables (start)
    # ******************************************************
    # variables from signac workspace
    box_0_temp_to_rcutcoulomb_dict = {300:12,
     				     350: 12,
     				     400: 12,
     				     450: 12,
     				     500: 12,
     				     550: 12,
     				     575: 12,
     				     600: 12,
     				     625: 10,
     				     650: 10,
     				     675: 10,
     				     }
    
    box_1_temp_to_rcutcoulomb_dict = {300:100,
     				     350: 50,
     				     400: 30,
     				     450: 20,
     				     500: 20,
     				     550: 14,
     				     575: 12,
     				     600: 10,
     				     625: 10,
     				     650: 10,
     				     675: 10,
     				     }
    
    production_temperature_K = job.sp.production_temperature_K * u.K
    seed_no = job.doc.replica_number_int

    # cutoff and tail correction
    Rcut_ang = 10 * u.angstrom
    Rcut_low_ang = 1.0 * u.angstrom
    Electrostatic_bool = False
    Ewald_bool=False
    LRC = False
    Ewald_tol=0.00001
    RcutCoulomb_box_0=10.0 * u.angstrom
    RcutCoulomb_box_1=10.0 * u.angstrom
    Exclude = "1-4"
    #RcutCoulomb_box_0 = box_0_temp_to_rcutcoulomb_dict[job.sp.production_temperature_K]*u.angstrom
    #RcutCoulomb_box_1 = box_1_temp_to_rcutcoulomb_dict[job.sp.production_temperature_K]*u.angstrom
    #RcutCoulomb_box_0=14.0 * u.angstrom
    #RcutCoulomb_box_1=17.0 * u.angstrom

    # output all data and calc frequecy
    output_true_list_input = [
     	True,
     	int(gomc_output_data_every_X_steps),
    ]
    output_false_list_input = [
     	False,
     	int(gomc_output_data_every_X_steps),
    ]

    print("#**********************")
    print("Started: NVT Pre-equilibration GEMC-NVT GOMC control file writing")
    print("#**********************")
    output_file_prefix = gomc_nvt_equilb_output_name_str
    starting_control_file_name_str = gomc_charmm_object_with_files

# calc MC steps for gomc equilb
    MC_steps = int(gomc_steps_nvt_equilibration)
    Expert_bool = True
    table_interpolation="cubic"
    # MC move ratios
    DisFreq = 0.40
    RotFreq = 0.40
    VolFreq = 0.00
    MultiParticleFreq=0.00
    RegrowthFreq = 0.10
    IntraSwapFreq = 0.00
    IntraMEMC_2Freq = 0.00
    MEMC_2LiqFreq = 0.0
    CrankShaftFreq = 0.10
    SwapFreq = 0.0
    MEMC_2Freq = 0.0
    #memc_move_data = [1, "F4A", ["C2","C3"], "C4A", ["C2","C3"]]
    #Exchange_volume = [3.0, 3.0, 5.0]

    gomc_control.write_gomc_control_file(
     	starting_control_file_name_str,
     	gomc_nvt_equilb_control_file_name_str,
     	'GEMC_NVT',
     	MC_steps,
     	production_temperature_K,
     	ff_psf_pdb_file_directory=None,
     	check_input_files_exist=False,
     	Parameters=None,
     	Restart=False,
     	Checkpoint=False,
     	ExpertMode=Expert_bool,
     	Coordinates_box_0=None,
     	Structure_box_0=None,
     	binCoordinates_box_0=None,
     	extendedSystem_box_0=None,
     	binVelocities_box_0=None,
     	Coordinates_box_1=None,
     	Structure_box_1=None,
     	binCoordinates_box_1=None,
     	extendedSystem_box_1=None,
     	binVelocities_box_1=None,
     	input_variables_dict={
     	    "PRNG": seed_no,
     	    "Pressure": None,
     	    "Potential": "TABULATED",
            "TabulatedEnergiesFile":gomc_tabulated_ff_filename,
            "TableInterpType":table_interpolation,
     	    "LRC": LRC,
     	    "Rcut": Rcut_ang,
     	    "RcutLow": Rcut_low_ang,
     	    "RcutCoulomb_box_0":RcutCoulomb_box_0,
     	    "RcutCoulomb_box_1":RcutCoulomb_box_1,
     	    "Ewald": Ewald_bool,
     	    "ElectroStatic": Electrostatic_bool,
     	    "Tolerance": Ewald_tol,
     	    "VDWGeometricSigma": False,
     	    "Exclude": Exclude,
     	    "DisFreq": DisFreq,
     	    "VolFreq": VolFreq,
     	    "RotFreq": RotFreq,
     	    "MultiParticleFreq": MultiParticleFreq,
     	    "RegrowthFreq": RegrowthFreq,
     	    "IntraSwapFreq": IntraSwapFreq,
     	    "IntraMEMC-2Freq": IntraMEMC_2Freq,
     	    "CrankShaftFreq": CrankShaftFreq,
     	    "SwapFreq": SwapFreq,
     	    "MEMC-2Freq": MEMC_2Freq,
     	    "MEMC-2-LiqFreq": MEMC_2LiqFreq,
     	    "ExchangeVolumeDim": [3.0, 3.0, 5.0],
     	    #"MEMC_DataInput": [memc_move_data],
     	    "OutputName": output_file_prefix,
     	    "EqSteps": EqSteps,
     	    "AdjSteps":AdjSteps,
     	    "PressureCalc": [True, pressure_calc_freq],
     	    "RestartFreq": [True, coordinate_output_freq],
     	    "CheckpointFreq": [True, coordinate_output_freq],
     	    "DCDFreq": [True, coordinate_output_freq],
     	    "ConsoleFreq": [True, console_output_freq],
     	    "BlockAverageFreq":[True, block_ave_output_freq],
     	    "HistogramFreq": output_false_list_input,
     	    "CoordinatesFreq": output_false_list_input,
     	    "CBMC_First": 12,
     	    "CBMC_Nth": 10,
     	    "CBMC_Ang": 50,
     	    "CBMC_Dih": 50,
     	},
    )
    print("#**********************")
    print("Completed: pre-equilb GEMC-NVT GOMC control file writing")
    print("#**********************")

    # ******************************************************
    # common variables (end))
    # ******************************************************


    # ******************************************************
    # equilb selected_ensemble, if NVT -> NPT - GOMC control file writing  (start)
    # Note: the control files are written for the max number of gomc_equilb_design_ensemble runs
    # so the Charmm object only needs created 1 time.
    # ******************************************************
    
    print("#**********************")
    print("Started: equilb GEMC-NVT GOMC control file writing")
    print("#**********************")
      # Set Monte Carlo steps for equilibration MC steps for gomc
    MC_steps = int(gomc_steps_equilibration)
    
    # MC move ratios
    DisFreq = 0.30
    RotFreq = 0.29
    VolFreq = 0.01
    MultiParticleFreq=0.00
    RegrowthFreq = 0.10
    IntraSwapFreq = 0.00
    IntraMEMC_2Freq = 0.00
    MEMC_2LiqFreq = 0.00
    CrankShaftFreq = 0.10
    SwapFreq = 0.20
    MEMC_2Freq = 0.0
    memc_move_data = [1, "F4A", ["C2","C3"], "C4A", ["C2","C3"]]
    Exchange_volume = [6.0, 6.0, 9.0]

    output_file_prefix = gomc_equilb_output_name_str
    starting_control_file_name_str = gomc_charmm_object_with_files
    restart_control_file_name_str = gomc_nvt_equilb_output_name_str
# setup file names for the second stage of the equilibration
    Coordinates_box_0 = "{}_BOX_0_restart.pdb".format(
     	restart_control_file_name_str
    )	
    Structure_box_0 = "{}_BOX_0_restart.psf".format(
     	restart_control_file_name_str
    )
    binCoordinates_box_0 = "{}_BOX_0_restart.coor".format(
     	restart_control_file_name_str
    )
    extendedSystem_box_0 = "{}_BOX_0_restart.xsc".format(
     	restart_control_file_name_str
    )
    Coordinates_box_1 = "{}_BOX_1_restart.pdb".format(
     	restart_control_file_name_str
    )
    Structure_box_1 = "{}_BOX_1_restart.psf".format(
     	restart_control_file_name_str
    )
    binCoordinates_box_1 = "{}_BOX_1_restart.coor".format(
     	restart_control_file_name_str
    )
    extendedSystem_box_1 = "{}_BOX_1_restart.xsc".format(
     	restart_control_file_name_str
    )
   
    gomc_control.write_gomc_control_file(
     	starting_control_file_name_str,
     	gomc_equilb_control_file_name_str,
     	'GEMC_NVT',
     	MC_steps,
     	production_temperature_K,
     	ff_psf_pdb_file_directory=None,
     	check_input_files_exist=False,
     	Parameters=None,
     	Restart=True,
     	Checkpoint=False,
     	ExpertMode=False,
     	Coordinates_box_0=Coordinates_box_0,
     	Structure_box_0=Structure_box_0,
     	binCoordinates_box_0=binCoordinates_box_0,
     	extendedSystem_box_0=extendedSystem_box_0,
     	Coordinates_box_1=Coordinates_box_1,
     	Structure_box_1=Structure_box_1,
     	binCoordinates_box_1=binCoordinates_box_1,
     	extendedSystem_box_1=extendedSystem_box_1,
     	binVelocities_box_0=None,
     	binVelocities_box_1=None,
     	input_variables_dict={
     	    "PRNG": seed_no,
     	   "Pressure": None,
           "Potential": "TABULATED",
           "TabulatedEnergiesFile":gomc_tabulated_ff_filename,
           "TableInterpType":table_interpolation,
     	   "LRC": LRC,
     	   "Rcut": Rcut_ang,
     	   "RcutLow": Rcut_low_ang,
     	   "RcutCoulomb_box_0":RcutCoulomb_box_0,
     	   "RcutCoulomb_box_1":RcutCoulomb_box_1,
     	   "Ewald": Ewald_bool,
     	   "ElectroStatic": Electrostatic_bool,
     	   "Tolerance": Ewald_tol,
     	   "VDWGeometricSigma": False,
     	   "Exclude": Exclude,
     	   "DisFreq": DisFreq,
     	   "VolFreq": VolFreq,
     	   "RotFreq": RotFreq,
     	   "MultiParticleFreq": MultiParticleFreq,
     	   "RegrowthFreq": RegrowthFreq,
     	   "IntraSwapFreq": IntraSwapFreq,
     	   "IntraMEMC-2Freq": IntraMEMC_2Freq,
     	   "CrankShaftFreq": CrankShaftFreq,
     	   "SwapFreq": SwapFreq,
     	   "MEMC-2Freq": MEMC_2Freq,
     	   "MEMC-2-LiqFreq": MEMC_2LiqFreq,
     	   "ExchangeVolumeDim": [3.0, 3.0, 5.0],
     	  # "MEMC_DataInput": [memc_move_data],
     	   "OutputName": output_file_prefix,
     	   "EqSteps": EqSteps,
     	   "AdjSteps":AdjSteps,
     	   "PressureCalc": [True, pressure_calc_freq],
     	   "RestartFreq": [True, coordinate_output_freq],
     	   "CheckpointFreq": [True, coordinate_output_freq],
     	   "DCDFreq": [True, coordinate_output_freq],
     	   "ConsoleFreq": [True, console_output_freq],
     	   "BlockAverageFreq":[True, block_ave_output_freq],
     	   "HistogramFreq": output_false_list_input,
     	   "CoordinatesFreq": output_false_list_input,
     	   "CBMC_First": 12,
     	   "CBMC_Nth": 10,
     	   "CBMC_Ang": 50,
     	   "CBMC_Dih": 50,
       },
   )
    print("#**********************")
    print("Completed: equilb GEMC-NPT GOMC control file written")
    print("#**********************")

   # ******************************************************
   # equilb selected_ensemble, if NVT -> NPT - GOMC control file writing  (end)
   # Note: the control files are written for the max number of gomc_equilb_design_ensemble runs
   # so the Charmm object only needs created 1 time.
   # ******************************************************

   # ******************************************************
   # production NPT or GEMC-NVT - GOMC control file writing  (start)
   # ******************************************************

    print("#**********************")
    print("Started: production NPT or GEMC-NVT GOMC control file writing")
    print("#**********************")

    output_file_prefix = gomc_production_output_name_str
    restart_control_file_name_str = gomc_equilb_output_name_str

   # calc MC steps
    MC_steps = int(gomc_steps_production)

    Coordinates_box_0 = "{}_BOX_0_restart.pdb".format(
       restart_control_file_name_str
    )
    Structure_box_0 = "{}_BOX_0_restart.psf".format(
       restart_control_file_name_str
    )
    binCoordinates_box_0 = "{}_BOX_0_restart.coor".format(
       restart_control_file_name_str
    )
    extendedSystem_box_0 = "{}_BOX_0_restart.xsc".format(
       restart_control_file_name_str
    )

    Coordinates_box_1 = "{}_BOX_1_restart.pdb".format(
       restart_control_file_name_str
    )
    Structure_box_1 = "{}_BOX_1_restart.psf".format(
       restart_control_file_name_str
    )
    binCoordinates_box_1 = "{}_BOX_1_restart.coor".format(
       restart_control_file_name_str
    )
    extendedSystem_box_1 = "{}_BOX_1_restart.xsc".format(
       restart_control_file_name_str
    )

    gomc_control.write_gomc_control_file(
       gomc_charmm_object_with_files,
       gomc_production_control_file_name_str,
       "GEMC_NVT",
       MC_steps,
       production_temperature_K,
       ff_psf_pdb_file_directory=None,
       check_input_files_exist=False,
       Parameters=None,
       Restart=True,
       Checkpoint=False,
       ExpertMode=False,
       Coordinates_box_0=Coordinates_box_0,
       Structure_box_0=Structure_box_0,
       binCoordinates_box_0=binCoordinates_box_0,
       extendedSystem_box_0=extendedSystem_box_0,
       Coordinates_box_1=Coordinates_box_1,
       Structure_box_1=Structure_box_1,
       binCoordinates_box_1=binCoordinates_box_1,
       extendedSystem_box_1=extendedSystem_box_1,
       binVelocities_box_1=None,
       input_variables_dict={
     	   "PRNG": seed_no,
     	   "Pressure": None,
           "Potential": "TABULATED",
           "TabulatedEnergiesFile":gomc_tabulated_ff_filename,
           "TableInterpType":table_interpolation,
     	   "LRC": LRC,
     	   "Rcut": Rcut_ang,
     	   "RcutLow": Rcut_low_ang,
     	  # "RcutCoulomb_box_0":RcutCoulomb_box_0,
     	  # "RcutCoulomb_box_1":RcutCoulomb_box_1,
     	   "Ewald": Ewald_bool,
     	   "ElectroStatic": Ewald_bool,
     	   "Tolerance": Ewald_tol,
     	   "VDWGeometricSigma": False,
     	   "Exclude": Exclude,
     	   "DisFreq": DisFreq,
     	   "VolFreq": VolFreq,
     	   "RotFreq": RotFreq,
     	   "MultiParticleFreq": MultiParticleFreq,
     	   "RegrowthFreq": RegrowthFreq,
     	   "IntraSwapFreq": IntraSwapFreq,
     	   "IntraMEMC-2Freq": IntraMEMC_2Freq,
     	   "CrankShaftFreq": CrankShaftFreq,
     	   "SwapFreq": SwapFreq,
     	   "MEMC-2Freq": MEMC_2Freq,
     	   "OutputName": output_file_prefix,
     	   "EqSteps": EqSteps,
     	   "AdjSteps":AdjSteps,
     	   "PressureCalc": [True, pressure_calc_freq],
     	   "RestartFreq": [True, coordinate_output_freq],
     	   "CheckpointFreq": [True, coordinate_output_freq],
     	   "DCDFreq": [True, coordinate_output_freq],
     	   "ConsoleFreq": [True, console_output_freq],
     	   "BlockAverageFreq":[True, block_ave_output_freq],
     	   "HistogramFreq": output_false_list_input,
     	   "CoordinatesFreq": output_false_list_input,  	  
     	   "CBMC_First": 12,
     	   "CBMC_Nth": 10,
     	   "CBMC_Ang": 50,
     	   "CBMC_Dih": 50,
       },
   )
    print("#**********************")
    print("Completed: production NPT or GEMC-NVT GOMC control file writing")
    print("#**********************")
   
# ******************************************************
# production NPT or GEMC-NVT - GOMC control file writing  (end)
# ******************************************************


# ******************************************************
# ******************************************************
# Creating GOMC files (pdb, psf, force field (FF), and gomc control files (end)
# ******************************************************
# ******************************************************


# ******************************************************
# ******************************************************
# equilb NPT or GEMC-NVT - starting the GOMC simulation (start)
# ******************************************************
# ******************************************************


@Project.pre(mosdef_input_written)
@Project.pre(part_2a_gomc_nvt_equilb_design_ensemble_control_file_written)
@Project.post(part_4a_job_gomc_nvt_equilb_design_ensemble_completed_properly)
@Project.operation(directives=
    {
        "np": lambda job: job.doc.gomc_ncpu,
        "ngpu": lambda job: job.doc.gomc_ngpu,
        "memory": memory_needed,
        "walltime": walltime_gomc_equilbrium_hr,
    }, with_job=True, cmd=True
)
def run_nvt_equilb_ensemble_gomc_command(job):
    """Run the gomc equilb_ensemble simulation."""
    control_file_name_str = gomc_nvt_equilb_control_file_name_str

    print(f"Running simulation job id {job}")
    run_command = "{}/{} +p{} {}.conf > out_{}.dat".format(
        str(gomc_binary_path),
        str(job.doc.gomc_equilb_design_ensemble_gomc_binary_file),
        str(job.doc.gomc_ncpu),
        str(control_file_name_str),
        str(control_file_name_str),
    )

    print('gomc equilb run_command = ' + str(run_command))

    return run_command


# ******************************************************
# ******************************************************
# equilb NPT or GEMC-NVT - starting the GOMC simulation (end)
# ******************************************************
# ******************************************************

@Project.pre(mosdef_input_written)
@Project.pre(part_2b_gomc_equilb_design_ensemble_control_file_written)
@Project.pre(part_4a_job_gomc_nvt_equilb_design_ensemble_completed_properly)
@Project.post(part_4b_job_gomc_equilb_design_ensemble_completed_properly)
@Project.operation(directives=
    {
        "np": lambda job: job.doc.gomc_ncpu,
        "ngpu": lambda job: job.doc.gomc_ngpu,
        "memory": memory_needed,
        "walltime": walltime_gomc_equilbrium_hr,
    }, with_job=True, cmd=True
)
def run_equilb_ensemble_gomc_command(job):
    """Run the gomc equilb_ensemble simulation."""
    control_file_name_str = gomc_equilb_control_file_name_str

    print(f"Running simulation job id {job}")
    run_command = "{}/{} +p{} {}.conf > out_{}.dat".format(
        str(gomc_binary_path),
        str(job.doc.gomc_equilb_design_ensemble_gomc_binary_file),
        str(job.doc.gomc_ncpu),
        str(control_file_name_str),
        str(control_file_name_str),
    )

    print('gomc equilb run_command = ' + str(run_command))

    return run_command



# ******************************************************
# ******************************************************
# production run - starting the GOMC simulation (start)
# ******************************************************
# ******************************************************


@Project.pre(part_2c_gomc_production_control_file_written)
@Project.pre(part_4b_job_gomc_equilb_design_ensemble_completed_properly)
#@Project.post(part_3b_output_gomc_production_run_started)
@Project.post(part_4c_job_production_run_completed_properly)
@Project.operation(directives=
    {
        "np": lambda job: job.doc.gomc_ncpu,
        "ngpu": lambda job: job.doc.gomc_ngpu,
        "memory": memory_needed,
        "walltime": walltime_gomc_production_hr,
    }, with_job=True, cmd=True
)
def run_production_run_gomc_command(job):
    """Run the gomc_production_ensemble simulation."""

    control_file_name_str = gomc_production_control_file_name_str

    print(f"Running simulation job id {job}")
    run_command = "{}/{} +p{} {}.conf > out_{}.dat".format(
        str(gomc_binary_path),
        str(job.doc.gomc_production_ensemble_gomc_binary_file),
        str(job.doc.gomc_ncpu),
        str(control_file_name_str),
        str(control_file_name_str),
    )

    print('gomc production run_command = ' + str(run_command))

    return run_command
# ******************************************************
# ******************************************************
# production run - starting the GOMC simulation (end)
# ******************************************************
# ******************************************************



# ******************************************************
# ******************************************************
# data analysis - get the average data from each replicate (start)
# ******************************************************
# ******************************************************
  
@Project.pre(part_4c_job_production_run_completed_properly)
@Project.post(part_5a_analysis_individual_simulation_averages_completed)
@Project.operation(directives=
     {
         "np": 1,
         "ngpu": 0,
         "memory": memory_needed,
         "walltime": walltime_gomc_analysis_hr,
     }, with_job=True
)
def part_5a_analysis_individual_simulation_averages(job):
    # remove the total averged replicate data and all analysis data after this,
    # as it is no longer valid when adding more simulations
    if os.path.isfile(f'../../analysis/{output_avg_std_of_replicates_txt_file_name_liq}'):
        os.remove(f'../../analysis/{output_avg_std_of_replicates_txt_file_name_liq}')
    if os.path.isfile(f'../../analysis/{output_avg_std_of_replicates_txt_file_name_vap}'):
        os.remove(f'../../analysis/{output_avg_std_of_replicates_txt_file_name_vap}')
    if os.path.isfile(f'../../analysis/{output_critical_data_replicate_txt_file_name}'):
        os.remove(f'../../analysis/{output_critical_data_replicate_txt_file_name}')
    if os.path.isfile(f'../../analysis/{output_critical_data_avg_std_of_replicates_txt_file_name}'):
        os.remove(f'../../analysis/{output_critical_data_avg_std_of_replicates_txt_file_name}')
    if os.path.isfile(f'../../analysis/{output_boiling_data_replicate_txt_file_name}'):
        os.remove(f'../../analysis/{output_boiling_data_replicate_txt_file_name}')
    if os.path.isfile(f'../../analysis/{output_boiling_data_avg_std_of_replicates_txt_file_name}'):
        os.remove(f'../../analysis/{output_boiling_data_avg_std_of_replicates_txt_file_name}')


    # this is set to basically use all values.  However, allows the ability to set if needed
    step_start = 0 * 10 ** 6
    step_finish = 1 * 10 ** 12

    # get the averages from each individual simulation and write the csv's.

    reading_file_box_0 = job.fn(f'Blk_{gomc_production_output_name_str}_BOX_0.dat')
    reading_file_box_1 = job.fn(f'Blk_{gomc_production_output_name_str}_BOX_1.dat')

    output_column_temp_title = 'temp_K'  # column title title for temp
    output_column_no_step_title = 'Step'  # column title title for iter value
    output_column_no_pressure_title = 'P_bar'  # column title title for PRESSURE
    output_column_total_molecules_title = "No_mol"  # column title title for TOT_MOL
    output_column_Rho_title = 'Rho_kg_per_m_cubed'  # column title title for TOT_DENS
    output_column_box_volume_title = 'V_ang_cubed'  # column title title for VOLUME
    output_column_box_length_if_cubed_title = 'L_m_if_cubed'  # column title title for VOLUME
    output_column_box_Hv_title = 'Hv_kJ_per_mol'  # column title title for HEAT_VAP
    output_column_box_Z_title = 'Z'  # column title title for  compressiblity (Z)

    blk_file_reading_column_no_step_title = '#STEP'  # column title title for iter value
    blk_file_reading_column_no_pressure_title = 'PRESSURE'  # column title title for PRESSURE
    blk_file_reading_column_total_molecules_title = "TOT_MOL"  # column title title for TOT_MOL
    blk_file_reading_column_Rho_title = 'TOT_DENS'  # column title title for TOT_DENS
    blk_file_reading_column_box_volume_title = 'VOLUME'  # column title title for VOLUME
    blk_file_reading_column_box_Hv_title = 'HEAT_VAP'  # column title title for HEAT_VAP
    blk_file_reading_column_box_Z_title = 'COMPRESSIBILITY'  # column title title for compressiblity (Z)

    # Programmed data
    step_start_string = str(int(step_start))
    step_finish_string = str(int(step_finish))

    # *************************
    # drawing in data from single file and extracting specific rows for the liquid box (start)
    # *************************
    data_box_0 = pd.read_csv(reading_file_box_0, sep='\s+', header=0, na_values='NaN', index_col=False)

    data_box_0 = pd.DataFrame(data_box_0)
    step_no_title_mod = blk_file_reading_column_no_step_title[1:]
    header_list = list(data_box_0.columns)
    header_list[0] = step_no_title_mod
    data_box_0.columns = header_list

    data_box_0 = data_box_0.query(step_start_string + ' <= ' + step_no_title_mod + ' <= ' + step_finish_string)

    iter_no_box_0 = data_box_0.loc[:, step_no_title_mod]
    iter_no_box_0 = list(iter_no_box_0)
    iter_no_box_0 = np.transpose(iter_no_box_0)

    pressure_box_0 = data_box_0.loc[:, blk_file_reading_column_no_pressure_title]
    pressure_box_0 = list(pressure_box_0)
    pressure_box_0 = np.transpose(pressure_box_0)
    pressure_box_0_mean = np.nanmean(pressure_box_0)

    total_molecules_box_0 = data_box_0.loc[:, blk_file_reading_column_total_molecules_title]
    total_molecules_box_0 = list(total_molecules_box_0)
    total_molecules_box_0 = np.transpose(total_molecules_box_0)
    total_molecules_box_0_mean = np.nanmean(total_molecules_box_0)

    Rho_box_0 = data_box_0.loc[:, blk_file_reading_column_Rho_title]
    Rho_box_0 = list(Rho_box_0)
    Rho_box_0 = np.transpose(Rho_box_0)
    Rho_box_0_mean = np.nanmean(Rho_box_0)

    volume_box_0 = data_box_0.loc[:, blk_file_reading_column_box_volume_title]
    volume_box_0 = list(volume_box_0)
    volume_box_0 = np.transpose(volume_box_0)
    volume_box_0_mean = np.nanmean(volume_box_0)
    length_if_cube_box_0_mean = (volume_box_0_mean) ** (1 / 3)

    Hv_box_0 = data_box_0.loc[:, blk_file_reading_column_box_Hv_title]
    Hv_box_0 = list(Hv_box_0)
    Hv_box_0 = np.transpose(Hv_box_0)
    Hv_box_0_mean = np.nanmean(Hv_box_0)

    Z_box_0 = data_box_0.loc[:, blk_file_reading_column_box_Z_title]
    Z_box_0 = list(Z_box_0)
    Z_box_0 = np.transpose(Z_box_0)
    Z_box_0_mean = np.nanmean(Z_box_0)

    # *************************
    # drawing in data from single file and extracting specific rows for the liquid box (end)
    # *************************

    # *************************
    # drawing in data from single file and extracting specific rows for the vapor box (start)
    # *************************
    data_box_1 = pd.read_csv(reading_file_box_1, sep='\s+', header=0, na_values='NaN', index_col=False)
    data_box_1 = pd.DataFrame(data_box_1)

    step_no_title_mod = blk_file_reading_column_no_step_title[1:]
    header_list = list(data_box_1.columns)
    header_list[0] = step_no_title_mod
    data_box_1.columns = header_list

    data_box_1 = data_box_1.query(step_start_string + ' <= ' + step_no_title_mod + ' <= ' + step_finish_string)

    iter_no_box_1 = data_box_1.loc[:, step_no_title_mod]
    iter_no_box_1 = list(iter_no_box_1)
    iter_no_box_1 = np.nanmean(iter_no_box_1)

    pressure_box_1 = data_box_1.loc[:, blk_file_reading_column_no_pressure_title]
    pressure_box_1 = list(pressure_box_1)
    pressure_box_1 = np.transpose(pressure_box_1)
    pressure_box_1_mean = np.nanmean(pressure_box_1)

    total_molecules_box_1 = data_box_1.loc[:, blk_file_reading_column_total_molecules_title]
    total_molecules_box_1 = list(total_molecules_box_1)
    total_molecules_box_1 = np.transpose(total_molecules_box_1)
    total_molecules_box_1_mean = np.nanmean(total_molecules_box_1)

    Rho_box_1 = data_box_1.loc[:, blk_file_reading_column_Rho_title]
    Rho_box_1 = list(Rho_box_1)
    Rho_box_1 = np.transpose(Rho_box_1)
    Rho_box_1_mean = np.nanmean(Rho_box_1)

    volume_box_1 = data_box_1.loc[:, blk_file_reading_column_box_volume_title]
    volume_box_1 = list(volume_box_1)
    volume_box_1 = np.transpose(volume_box_1)
    volume_box_1_mean = np.nanmean(volume_box_1)
    length_if_cube_box_1_mean = (volume_box_1_mean) ** (1 / 3)

    Hv_box_1 = data_box_1.loc[:, blk_file_reading_column_box_Hv_title]
    Hv_box_1 = list(Hv_box_1)
    Hv_box_1 = np.transpose(Hv_box_1)
    Hv_box_1_mean = np.nanmean(Hv_box_1)

    Z_box_1 = data_box_1.loc[:, blk_file_reading_column_box_Z_title]
    Z_box_1 = list(Z_box_1)
    Z_box_1 = np.transpose(Z_box_1)
    Z_box_1_mean = np.nanmean(Z_box_1)

    # sort boxes based on density to liquid or vapor
    if (Rho_box_0_mean > Rho_box_1_mean) or (Rho_box_0_mean == Rho_box_1_mean):
        pressure_box_liq_mean = pressure_box_0_mean
        total_molecules_box_liq_mean = total_molecules_box_0_mean
        Rho_box_liq_mean = Rho_box_0_mean
        volume_box_liq_mean = volume_box_0_mean
        length_if_cube_box_liq_mean = length_if_cube_box_0_mean
        Hv_box_liq_mean = Hv_box_0_mean
        Z_box_liq_mean = Z_box_0_mean

        pressure_box_vap_mean = pressure_box_1_mean
        total_molecules_box_vap_mean = total_molecules_box_1_mean
        Rho_box_vap_mean = Rho_box_1_mean
        volume_box_vap_mean = volume_box_1_mean
        length_if_cube_box_vap_mean = length_if_cube_box_1_mean
        Hv_box_vap_mean = Hv_box_1_mean
        Z_box_vap_mean = Z_box_1_mean

    elif Rho_box_0_mean < Rho_box_1_mean:
        pressure_box_liq_mean = pressure_box_1_mean
        total_molecules_box_liq_mean = total_molecules_box_1_mean
        Rho_box_liq_mean = Rho_box_1_mean
        volume_box_liq_mean = volume_box_1_mean
        length_if_cube_box_liq_mean = length_if_cube_box_1_mean
        Hv_box_liq_mean = Hv_box_1_mean
        Z_box_liq_mean = Z_box_1_mean

        pressure_box_vap_mean = pressure_box_0_mean
        total_molecules_box_vap_mean = total_molecules_box_0_mean
        Rho_box_vap_mean = Rho_box_0_mean
        volume_box_vap_mean = volume_box_0_mean
        length_if_cube_box_vap_mean = length_if_cube_box_0_mean
        Hv_box_vap_mean = Hv_box_0_mean
        Z_box_vap_mean = Z_box_0_mean

    # *************************
    # drawing in data from single file and extracting specific rows for the vapor box (end)
    # *************************

    box_liq_replicate_data_txt_file = open(output_replicate_txt_file_name_liq, "w")
    box_liq_replicate_data_txt_file.write(
        f"{output_column_temp_title: <30} "
        f"{output_column_no_pressure_title: <30} "
        f"{output_column_total_molecules_title: <30} "
        f"{output_column_Rho_title: <30} "
        f"{output_column_box_volume_title: <30} "
        f"{output_column_box_length_if_cubed_title: <30} "
        f"{output_column_box_Hv_title: <30} "
        f"{output_column_box_Z_title: <30} "
        f" \n"
    )
    box_liq_replicate_data_txt_file.write(
        f"{job.sp.production_temperature_K: <30} "
        f"{pressure_box_liq_mean: <30} "
        f"{total_molecules_box_liq_mean: <30} "
        f"{Rho_box_liq_mean: <30} "
        f"{volume_box_liq_mean: <30} "
        f"{length_if_cube_box_liq_mean: <30} "
        f"{Hv_box_liq_mean: <30} "
        f"{Z_box_liq_mean: <30} "
        f" \n"
    )

    box_vap_replicate_data_txt_file = open(output_replicate_txt_file_name_vap, "w")
    box_vap_replicate_data_txt_file.write(
        f"{output_column_temp_title: <30} "
        f"{output_column_no_pressure_title: <30} "
        f"{output_column_total_molecules_title: <30} "
        f"{output_column_Rho_title: <30} "
        f"{output_column_box_volume_title: <30} "
        f"{output_column_box_length_if_cubed_title: <30} "
        f"{output_column_box_Hv_title: <30} "
        f"{output_column_box_Z_title: <30} "
        f" \n"
    )
    box_vap_replicate_data_txt_file.write(
        f"{job.sp.production_temperature_K: <30} "
        f"{pressure_box_vap_mean: <30} "
        f"{total_molecules_box_vap_mean: <30} "
        f"{Rho_box_vap_mean: <30} "
        f"{volume_box_vap_mean: <30} "
        f"{length_if_cube_box_vap_mean: <30} "
        f"{Hv_box_vap_mean: <30} "
        f"{Z_box_vap_mean: <30} "
        f" \n"
    )

    box_liq_replicate_data_txt_file.close()
    box_vap_replicate_data_txt_file.close()


    # ***********************
    # calc the avg data from the liq and vap boxes (end)
    # ***********************

# ******************************************************
# ******************************************************
# data analysis - get the average data from each replicate (end)
# ******************************************************
# ******************************************************


# ******************************************************
# ******************************************************
# data analysis - get the average and std. dev. from/across all the replicate (start)
# ******************************************************
# ******************************************************

@Project.pre(lambda *jobs: all(part_5a_analysis_individual_simulation_averages_completed(j)
        		       for j in jobs[0]._project))
@Project.post(part_5b_analysis_replica_averages_completed)
@Project.operation(directives=
   {
       "np": 1,
       "ngpu": 0,
       "memory": memory_needed,
       "walltime": walltime_gomc_analysis_hr,
     }, aggregator=aggregator.groupby(key=statepoint_without_replica, sort_by="production_temperature_K", sort_ascending=False)
)
def part_5b_analysis_replica_averages(*jobs):
    # ***************************************************
    #  create the required lists and file labels total averages across the replicates (start)
    # ***************************************************
    # get the list used in this function
    temp_repilcate_list = []

    pressure_repilcate_box_liq_list = []
    total_molecules_repilcate_box_liq_list = []
    Rho_repilcate_box_liq_list = []
    volume_repilcate_box_liq_list = []
    length_if_cube_repilcate_box_liq_list = []
    Hv_repilcate_box_liq_list = []
    Z_repilcate_box_liq_list = []

    pressure_repilcate_box_vap_list = []
    total_molecules_repilcate_box_vap_list = []
    Rho_repilcate_box_vap_list = []
    volume_repilcate_box_vap_list = []
    length_if_cube_repilcate_box_vap_list = []
    Hv_repilcate_box_vap_list = []
    Z_repilcate_box_vap_list = []

    output_column_temp_title = 'temp_K'  # column title title for temp
    output_column_no_pressure_title = 'P_bar'  # column title title for PRESSURE
    output_column_total_molecules_title = "No_mol"  # column title title for TOT_MOL
    output_column_Rho_title = 'Rho_kg_per_m_cubed'  # column title title for TOT_DENS
    output_column_box_volume_title = 'V_ang_cubed'  # column title title for VOLUME
    output_column_box_length_if_cubed_title = 'L_m_if_cubed'  # column title title for VOLUME
    output_column_box_Hv_title = 'Hv_kJ_per_mol'  # column title title for HEAT_VAP
    output_column_box_Z_title = 'Z'  # column title title for compressiblity (Z)

    output_column_temp_std_title = 'temp_std_K'  # column title title for temp
    output_column_no_pressure_std_title = 'P_std_bar'  # column title title for PRESSURE
    output_column_total_molecules_std_title = "No_mol_std"  # column title title for TOT_MOL
    output_column_Rho_std_title = 'Rho_std_kg_per_m_cubed'  # column title title for TOT_DENS
    output_column_box_volume_std_title = 'V_std_ang_cubed'  # column title title for VOLUME
    output_column_box_length_if_cubed_std_title = 'L_std_m_if_cubed'  # column title title for VOLUME
    output_column_box_Hv_std_title = 'Hv_std_kJ_per_mol'  # column title title for HEAT_VAP
    output_column_box_Z_std_title = 'Z_std'  # column title title for compressiblity (Z)

    output_txt_file_header = f"{output_column_temp_title: <30} "\
        		     f"{output_column_temp_std_title: <30} "\
        		     f"{output_column_no_pressure_title: <30} "\
        		     f"{output_column_no_pressure_std_title: <30} "\
        		     f"{output_column_total_molecules_title: <30} "\
        		     f"{output_column_total_molecules_std_title: <30} "\
        		     f"{output_column_Rho_title: <30} "\
        		     f"{output_column_Rho_std_title: <30} "\
        		     f"{output_column_box_volume_title: <30} "\
        		     f"{output_column_box_volume_std_title: <30} "\
        		     f"{output_column_box_length_if_cubed_title: <30} "\
        		     f"{output_column_box_length_if_cubed_std_title: <30} "\
        		     f"{output_column_box_Hv_title: <30} "\
        		     f"{output_column_box_Hv_std_title: <30} " \
        		     f"{output_column_box_Z_title: <30} " \
        		     f"{output_column_box_Z_std_title: <30} " \
        		     f"\n"


    write_file_path_and_name_liq = f'analysis/{output_avg_std_of_replicates_txt_file_name_liq}'
    write_file_path_and_name_vap = f'analysis/{output_avg_std_of_replicates_txt_file_name_vap}'
    if os.path.isfile(write_file_path_and_name_liq):
        box_liq_data_txt_file = open(write_file_path_and_name_liq, "a")
    else:
        box_liq_data_txt_file = open(write_file_path_and_name_liq, "w")
        box_liq_data_txt_file.write(output_txt_file_header)

    if os.path.isfile(write_file_path_and_name_vap):
        box_vap_data_txt_file = open(write_file_path_and_name_vap, "a")
    else:
        box_vap_data_txt_file = open(write_file_path_and_name_vap, "w")
        box_vap_data_txt_file.write(output_txt_file_header)

    # ***************************************************
    # create the required lists and file labels total averages across the replicates (end)
    # ***************************************************

    for job in jobs:

        # *************************
        # drawing in data from single simulation file and extracting specific
        # *************************
        reading_file_box_liq = job.fn(output_replicate_txt_file_name_liq)
        reading_file_box_vap = job.fn(output_replicate_txt_file_name_vap)

        data_box_liq = pd.read_csv(reading_file_box_liq, sep='\s+', header=0, na_values='NaN', index_col=False)
        data_box_liq = pd.DataFrame(data_box_liq)

        pressure_repilcate_box_liq = data_box_liq.loc[:, output_column_no_pressure_title][0]
        total_molecules_repilcate_box_liq = data_box_liq.loc[:, output_column_total_molecules_title][0]
        Rho_repilcate_box_liq = data_box_liq.loc[:, output_column_Rho_title][0]
        volume_repilcate_box_liq = data_box_liq.loc[:, output_column_box_volume_title][0]
        length_if_cube_repilcate_box_liq = (volume_repilcate_box_liq) ** (1 / 3)
        Hv_repilcate_box_liq = data_box_liq.loc[:, output_column_box_Hv_title][0]
        Z_repilcate_box_liq = data_box_liq.loc[:, output_column_box_Z_title][0]

        # *************************
        # drawing in data from single file and extracting specific rows for the liquid box (end)
        # *************************

        # *************************
        # drawing in data from single file and extracting specific rows for the vapor box (start)
        # *************************
        data_box_vap = pd.read_csv(reading_file_box_vap, sep='\s+', header=0, na_values='NaN', index_col=False)
        data_box_vap = pd.DataFrame(data_box_vap)

        pressure_repilcate_box_vap = data_box_vap.loc[:, output_column_no_pressure_title][0]
        total_molecules_repilcate_box_vap = data_box_vap.loc[:, output_column_total_molecules_title][0]
        Rho_repilcate_box_vap = data_box_vap.loc[:, output_column_Rho_title][0]
        volume_repilcate_box_vap = data_box_vap.loc[:, output_column_box_volume_title][0]
        length_if_cube_repilcate_box_vap = (volume_repilcate_box_vap) ** (1 / 3)
        Hv_repilcate_box_vap = data_box_vap.loc[:, output_column_box_Hv_title][0]
        Z_repilcate_box_vap = data_box_vap.loc[:, output_column_box_Z_title][0]

        temp_repilcate_list.append(job.sp.production_temperature_K)

        pressure_repilcate_box_liq_list.append(pressure_repilcate_box_liq)
        total_molecules_repilcate_box_liq_list.append(total_molecules_repilcate_box_liq)
        Rho_repilcate_box_liq_list.append(Rho_repilcate_box_liq)
        volume_repilcate_box_liq_list.append(volume_repilcate_box_liq)
        length_if_cube_repilcate_box_liq_list.append(length_if_cube_repilcate_box_liq)
        Hv_repilcate_box_liq_list.append(Hv_repilcate_box_liq)
        Z_repilcate_box_liq_list.append(Z_repilcate_box_liq)

        pressure_repilcate_box_vap_list.append(pressure_repilcate_box_vap)
        total_molecules_repilcate_box_vap_list.append(total_molecules_repilcate_box_vap)
        Rho_repilcate_box_vap_list.append(Rho_repilcate_box_vap)
        volume_repilcate_box_vap_list.append(volume_repilcate_box_vap)
        length_if_cube_repilcate_box_vap_list.append(length_if_cube_repilcate_box_vap)
        Hv_repilcate_box_vap_list.append(Hv_repilcate_box_vap)
        Z_repilcate_box_vap_list.append(Z_repilcate_box_vap)

        # *************************
        # drawing in data from single file and extracting specific rows for the vapor box (end)
        # *************************

    # *************************
    # get the replica means and std.devs (start)
    # *************************
    temp_mean = np.mean(temp_repilcate_list)
    temp_std = np.std(temp_repilcate_list, ddof=1)

    pressure_mean_box_liq = np.mean(pressure_repilcate_box_liq_list)
    total_molecules_mean_box_liq = np.mean(total_molecules_repilcate_box_liq_list)
    Rho_mean_box_liq = np.mean(Rho_repilcate_box_liq_list)
    volume_mean_box_liq = np.mean(volume_repilcate_box_liq_list)
    length_if_cube_mean_box_liq = np.mean(length_if_cube_repilcate_box_liq_list)
    Hv_mean_box_liq = np.mean(Hv_repilcate_box_liq_list)
    Z_mean_box_liq = np.mean(Z_repilcate_box_liq_list)

    pressure_std_box_liq = np.std(pressure_repilcate_box_liq_list, ddof=1)
    total_molecules_std_box_liq = np.std(total_molecules_repilcate_box_liq_list, ddof=1)
    Rho_std_box_liq= np.std(Rho_repilcate_box_liq_list, ddof=1)
    volume_std_box_liq = np.std(volume_repilcate_box_liq_list, ddof=1)
    length_if_cube_std_box_liq = np.std(length_if_cube_repilcate_box_liq_list, ddof=1)
    Hv_std_box_liq = np.std(Hv_repilcate_box_liq_list, ddof=1)
    Z_std_box_liq = np.std(Z_repilcate_box_liq_list, ddof=1)

    pressure_mean_box_vap = np.mean(pressure_repilcate_box_vap_list)
    total_molecules_mean_box_vap = np.mean(total_molecules_repilcate_box_vap_list)
    Rho_mean_box_vap = np.mean(Rho_repilcate_box_vap_list)
    volume_mean_box_vap = np.mean(volume_repilcate_box_vap_list)
    length_if_cube_mean_box_vap = np.mean(length_if_cube_repilcate_box_vap_list)
    Hv_mean_box_vap = np.mean(Hv_repilcate_box_vap_list)
    Z_mean_box_vap = np.mean(Z_repilcate_box_vap_list)

    pressure_std_box_vap = np.std(pressure_repilcate_box_vap_list, ddof=1)
    total_molecules_std_box_vap = np.std(total_molecules_repilcate_box_vap_list, ddof=1)
    Rho_std_box_vap = np.std(Rho_repilcate_box_vap_list, ddof=1)
    volume_std_box_vap = np.std(volume_repilcate_box_vap_list, ddof=1)
    length_if_cube_std_box_vap = np.std(length_if_cube_repilcate_box_vap_list, ddof=1)
    Hv_std_box_vap = np.std(Hv_repilcate_box_vap_list, ddof=1)
    Z_std_box_vap = np.std(Z_repilcate_box_vap_list, ddof=1)

    # *************************
    # get the replica means and std.devs (end)
    # *************************


    # ************************************
    # write the analysis data files for the liquid and vapor boxes (start)
    # ************************************

    box_liq_data_txt_file.write(
        f"{temp_mean: <30} "
        f"{temp_std: <30} "
        f"{pressure_mean_box_liq: <30} "
        f"{pressure_std_box_liq: <30} "
        f"{total_molecules_mean_box_liq: <30} "
        f"{total_molecules_std_box_liq: <30} "
        f"{Rho_mean_box_liq: <30} "
        f"{Rho_std_box_liq: <30} "
        f"{volume_mean_box_liq: <30} "
        f"{volume_std_box_liq: <30} "
        f"{length_if_cube_mean_box_liq: <30} "
        f"{length_if_cube_std_box_liq: <30} "
        f"{Hv_mean_box_liq: <30} "
        f"{Hv_std_box_liq: <30} "
        f"{Z_mean_box_liq: <30} "
        f"{Z_std_box_liq: <30} "
        f" \n"
    )

    box_vap_data_txt_file.write(
        f"{temp_mean: <30} "
        f"{temp_std: <30} "
        f"{pressure_mean_box_vap: <30} "
        f"{pressure_std_box_vap: <30} "
        f"{total_molecules_mean_box_vap: <30} "
        f"{total_molecules_std_box_vap: <30} "
        f"{Rho_mean_box_vap: <30} "
        f"{Rho_std_box_vap: <30} "
        f"{volume_mean_box_vap: <30} "
        f"{volume_std_box_vap: <30} "
        f"{length_if_cube_mean_box_vap: <30} "
        f"{length_if_cube_std_box_vap: <30} "
        f"{Hv_mean_box_vap: <30} "
        f"{Hv_std_box_vap: <30} "
        f"{Z_mean_box_vap: <30} "
        f"{Z_std_box_vap: <30} "
        f" \n"
    )
    # ************************************
    # write the analysis data files for the liquid and vapor boxes (end)
    # ************************************


# ******************************************************
# ******************************************************
# data analysis - get the average and std. dev. from/across all the replicate (end)
# ******************************************************
# ******************************************************

# ******************************************************
# ******************************************************
# data analysis - get the critical and boiling point data for each set of replicates (start)
# ******************************************************
# ******************************************************

@Project.pre(
     lambda * jobs: all(
         gomc_sim_completed_properly(job, gomc_production_control_file_name_str)
         for job in jobs
     )
)
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
@Project.pre(part_5b_analysis_replica_averages_completed)
@Project.post(part_5c_analysis_critical_and_boiling_points_replicate_data_completed)
@Project.operation( directives=
     {
         "np": 1,
         "ngpu": 0,
         "memory": memory_needed,
         "walltime": walltime_gomc_analysis_hr,
     }, aggregator=aggregator.groupby(key=statepoint_without_temperature, sort_by="production_temperature_K", sort_ascending=True)
)
def part_5c_analysis_critical_and_boiling__points_replicate_data(*jobs):
    # ***************************************************
    #  user changable variables (start)
    # ***************************************************
    #changed to 0.7 was 0.8
    lowest_Tr_for_critical_calcs = 0.7

    Beta_for_critical_points = 0.325

    # ***************************************************
    #  user changable variables (end)
    # ***************************************************

    # ***************************************************
    #  create the required lists and file labels for the replicates (start)
    # ***************************************************
    input_column_temp_title = 'temp_K'  # column title title for temp
    input_column_no_pressure_title = 'P_bar'  # column title title for PRESSURE
    input_column_Rho_title = 'Rho_kg_per_m_cubed'  # column title title for TOT_DENS
    input_column_box_Hv_kJ_per_mol_title = 'Hv_kJ_per_mol'  # column title title for HEAT_VAP

    output_column_Tc_K_title = 'Tc_K'
    output_column_Rho_c_kg_per_m_cubed_title = 'Rho_c_kg_per_m_cubed'
    output_column_Pc_bar_title = 'Pc_bar'
    output_column_lowest_T_K_for_Tc = "lowest_T_K_for_Tc"
    output_column_highest_T_K_for_Tc = "highest_T_K_for_Tc"
    output_column_lowest_Tr_K_for_Tc = "lowest_Tr_K_for_Tc"
    output_column_highest_Tr_K_for_Tc = "highest_Tr_K_for_Tc"
    output_column_No_T_K_for_Tc = "No_T_K_for_Tc"

    # write the critical data file
    output_critical_data_replicate_txt_file_header = f"{output_column_Tc_K_title: <30} " \
        					     f"{output_column_Rho_c_kg_per_m_cubed_title: <30} " \
        					     f"{output_column_Pc_bar_title: <30} " \
        					     f"{output_column_lowest_T_K_for_Tc: <30} " \
        					     f"{output_column_highest_T_K_for_Tc: <30} " \
        					     f"{output_column_lowest_Tr_K_for_Tc: <30} " \
        					     f"{output_column_highest_Tr_K_for_Tc: <30} " \
        					     f"{output_column_No_T_K_for_Tc: <30} " \
        					     f"\n"


    write_critial_file_path_and_name = f'analysis/{output_critical_data_replicate_txt_file_name}'
    if os.path.isfile(write_critial_file_path_and_name):
        critial_data_replicate_txt_file = open(write_critial_file_path_and_name, "a")
    else:
        critial_data_replicate_txt_file = open(write_critial_file_path_and_name, "w")
        critial_data_replicate_txt_file.write(output_critical_data_replicate_txt_file_header)

    # ***************************************************
    #  create the required lists and file labels for the replicates (end)
    # ***************************************************

    # *************************
    # drawing in data from the avg and std dev data file (start)
    # *************************
    temp_avg_box_liq_list = []
    Rho_avg_box_liq_list = []

    temp_K_avg_box_vap_list = []
    pressure_bar_avg_box_vap_list = []
    Rho_avg_box_vap_list = []
    Hv_kJ_per_mol_avg_box_vap_list = []
    for job in jobs:


        reading_file_avg_std_liq = job.fn(f'{output_replicate_txt_file_name_liq}')
        data_avg_std_liq = pd.read_csv(reading_file_avg_std_liq, sep='\s+', header=0, na_values='NaN', index_col=False)

        temp_avg_box_liq_list.append(data_avg_std_liq.loc[:, input_column_temp_title][0])
        Rho_avg_box_liq_list.append( data_avg_std_liq.loc[:, input_column_Rho_title][0])


        reading_file_avg_std_vap = job.fn(f'{output_replicate_txt_file_name_vap}')
        data_avg_std_vap = pd.read_csv(reading_file_avg_std_vap, sep='\s+', header=0, na_values='NaN', index_col=False)

        temp_K_avg_box_vap_list.append(data_avg_std_vap.loc[:, input_column_temp_title][0])
        pressure_bar_avg_box_vap_list.append(data_avg_std_vap.loc[:, input_column_no_pressure_title][0])
        Rho_avg_box_vap_list.append(data_avg_std_vap.loc[:, input_column_Rho_title][0])
        Hv_kJ_per_mol_avg_box_vap_list.append(data_avg_std_vap.loc[:, input_column_box_Hv_kJ_per_mol_title][0])


    # *************************
    # drawing in data from the avg and std dev data file (end)
    # *************************

    Tc_K_replicate_list = []
    Rho_c_kg_per_m_cubed_replicate_list = []
    Pc_bar_replicate_list = []

    lowest_T_K_for_Tc_replicate_list  = []
    highest_T_K_for_Tc_replicate_list  = []
    No_T_K_for_Tc_replicate_list  = []
    lowest_Tr_K_for_Tc_replicate_list  = []
    highest_Tr_K_for_Tc_replicate_list = []

    # check and make sure the liq and vap temps are in order for comparison
    for t_i in range(0, len(temp_avg_box_liq_list)):
        if temp_avg_box_liq_list[t_i] != temp_K_avg_box_vap_list[t_i]:
            raise ValueError("ERROR: the temperatures in the vapor and liquid average "
        		     "and std. dev. data do not match in order.")

    # get the full list of temps for the critical point calcs
    starting_temps_K_for_critical_point_list = temp_avg_box_liq_list


    Rho_avg_box_liq_and_1_list = []
    for Rho_i in range(0, len(Rho_avg_box_liq_list)):
        Rho_avg_box_liq_and_1_list.append(
            (Rho_avg_box_liq_list[Rho_i] + Rho_avg_box_vap_list[Rho_i]) / 2
        )



    # ***************************************************
    #  create t
    #  he required lists and file labels for the replicates (end)
    # ***************************************************

    # ***********************
    # calc the Critical points (start)
    # ***********************
    # loop thru to find lowers temps to use for critical calcs
    # set use_last_no_temps_for_critical_calcs to 1 as adding 1 on first for loop
    use_last_no_temps_for_critical_calcs = 1
    for temp_i in range(0, len(starting_temps_K_for_critical_point_list)):
        use_last_no_temps_for_critical_calcs += 1

        if len(starting_temps_K_for_critical_point_list) >= use_last_no_temps_for_critical_calcs:

            # (Rho_box_liq + Rho_box_liq)/2 = (Rho_critical) + A *(T -Tc)
            # (Rho_box_liq - Rho_box_liq) = B * |T -Tc |^(beta)
            # eq1 : Yr = ar + br * Xr = (Rho_box_liq + Rho_box_liq)/2 = (Rho_critical - A Tc) + A * T
            # eq2 : Ys =  as +bs *Xs = (Rho_box_liq - Rho_box_liq) = B^(1/beta) * Tc + (-B^(1/beta)) * T
            # Yr = (Rho_box_liq + Rho_box_liq)/2
            # Xr = T
            # ar = Rho_critical - A * Tc
            # br = A
            # Ys = (Rho_box_liq - Rho_box_liq) = B^(1/beta)
            # Xs = T
            # as = B^(1/beta)
            # bs = -B^(1/beta)

            temp_for_critical_list = []
            Rho_0_minus_Rho_1_for_critical_list = []
            Rho_0_plus_Rho_1_for_critical_list = []
            Rho_0_plus_Rho_1_div2_for_critical_list = []
            Rho_0_minus_Rho_1_power_1_div_Beta_for_critical_list = []

            ln_P_per_bar_for_critical_list = []
            T_power_neg1_for_critical_list = []

            if use_last_no_temps_for_critical_calcs > len(starting_temps_K_for_critical_point_list):
        	    print('Error: Larger number of temperatures for the critical '
        	      'point calculations than are available.'
        	      )
                  
            elif use_last_no_temps_for_critical_calcs <= 0:
        	    print('Error: The number of temperatures for the critical point '
        	      'calculations negative or zero.'
        	      )

            else:
                for k in range(len(starting_temps_K_for_critical_point_list) - use_last_no_temps_for_critical_calcs,
        		       len(starting_temps_K_for_critical_point_list)
                    ):
        	    # concentration 1 files and inputs
                    temp_value_iter = starting_temps_K_for_critical_point_list[k]
                    Rho_avg_box_liq_list_iter = Rho_avg_box_liq_list[k]
                    Rho_avg_box_vap_list_iter = Rho_avg_box_vap_list[k]
                    Rho_0_minus_Rho_1_iter = Rho_avg_box_liq_list_iter - Rho_avg_box_vap_list_iter
                    Rho_0_plus_Rho_1_iter = Rho_avg_box_liq_list_iter + Rho_avg_box_vap_list_iter
                    Rho_0_plus_Rho_1_div2_iter = \
                    (Rho_avg_box_liq_list_iter + Rho_avg_box_vap_list_iter) / 2

                    temp_for_critical_list.append(temp_value_iter)
                    Rho_0_minus_Rho_1_for_critical_list.append(Rho_0_minus_Rho_1_iter)
                    Rho_0_minus_Rho_1_power_1_div_Beta_for_critical_list.append(
                    Rho_0_minus_Rho_1_iter ** (1 / Beta_for_critical_points)
                    )
                    Rho_0_plus_Rho_1_for_critical_list.append(Rho_0_plus_Rho_1_iter)
                    Rho_0_plus_Rho_1_div2_for_critical_list.append(Rho_0_plus_Rho_1_div2_iter)

                    pressure_box_vap_iter = pressure_bar_avg_box_vap_list[k]
                    ln_P_per_bar_for_critical_list.append(np.log(pressure_box_vap_iter))
                    T_power_neg1_for_critical_list.append(1 / (starting_temps_K_for_critical_point_list[k]))

                    Rho_avg_box_liq_and_1_iter = \
                    (Rho_avg_box_liq_list_iter + Rho_avg_box_vap_list_iter) / 2
                    Rho_avg_box_liq_and_1_list.append(Rho_avg_box_liq_and_1_iter)

                eq1_slope, eq1_intercept, eq1_r_value, eq1_p_value, eq1_std_err = \
        	    stats.linregress(temp_for_critical_list, Rho_0_plus_Rho_1_div2_for_critical_list)
                eq2_slope, eq2_intercept, eq2_r_value, eq2_p_value, eq2_std_err = \
        	    stats.linregress(temp_for_critical_list, Rho_0_minus_Rho_1_power_1_div_Beta_for_critical_list)

                eq3_slope, eq3_intercept, eq3_r_value, eq3_p_value, eq3_std_err = \
        	    stats.linregress(T_power_neg1_for_critical_list, ln_P_per_bar_for_critical_list)
        	
                Tc_K_eval = -eq2_intercept / eq2_slope
                if np.isnan(Tc_K_eval) == True:
                    Tc_K = 'NA'
                else:
                    Tc_K = Tc_K_eval

                Rho_c_kg_per_m_cubed_eval = eq1_intercept + eq1_slope * Tc_K
                if np.isnan(Rho_c_kg_per_m_cubed_eval) == True:
                    Rho_c_kg_per_m_cubed = 'NA'
                else:
                    Rho_c_kg_per_m_cubed = Rho_c_kg_per_m_cubed_eval

                Pc_bar_eval = np.exp(eq3_intercept + eq3_slope * (1 / Tc_K))
                if np.isnan(Pc_bar_eval) == True:
                    Pc_bar = 'NA'
                else:
                    Pc_bar = Pc_bar_eval


                # check if passes the lowest_Tr_for_critical_calcs before writing
                lowest_T_K_for_Tc_iter = temp_for_critical_list[0]
                highest_T_K_for_Tc_iter = temp_for_critical_list[-1]
                No_T_K_for_Tc_iter = len(temp_for_critical_list)
                lowest_Tr_K_for_Tc_iter = float(lowest_T_K_for_Tc_iter / Tc_K)
                highest_Tr_K_for_Tc_iter = float(highest_T_K_for_Tc_iter / Tc_K)


                if lowest_Tr_K_for_Tc_iter >= lowest_Tr_for_critical_calcs:
                    print('utilized temperatures used for critical calcs = ' + str(temp_for_critical_list))
                    Tc_K_replicate_list.append(Tc_K)
                    Rho_c_kg_per_m_cubed_replicate_list.append(Rho_c_kg_per_m_cubed)
                    Pc_bar_replicate_list.append(Pc_bar)

                    lowest_T_K_for_Tc_replicate_list.append(lowest_T_K_for_Tc_iter)
                    highest_T_K_for_Tc_replicate_list.append(highest_T_K_for_Tc_iter)
                    No_T_K_for_Tc_replicate_list.append(No_T_K_for_Tc_iter)
                    lowest_Tr_K_for_Tc_replicate_list.append(lowest_Tr_K_for_Tc_iter)
                    highest_Tr_K_for_Tc_replicate_list.append(highest_Tr_K_for_Tc_iter)

    # write the critical data
    critial_data_replicate_txt_file.write(
        f"{Tc_K_replicate_list[-1]: <30} "
        f"{Rho_c_kg_per_m_cubed_replicate_list[-1]: <30} "
        f"{Pc_bar_replicate_list[-1]: <30} "
        f"{lowest_T_K_for_Tc_replicate_list[-1]: <30} "
        f"{highest_T_K_for_Tc_replicate_list[-1]: <30} "
        f"{lowest_Tr_K_for_Tc_replicate_list[-1]: <30} "
        f"{highest_Tr_K_for_Tc_replicate_list[-1]: <30} "
        f"{No_T_K_for_Tc_replicate_list[-1]: <30} "
        f" \n"
    )
    # ***********************
    # calc the Critical points (end)
    # ***********************

    # ***********************
    # calc the Boiling points (end)
    # ***********************

    # set the standard pressure for the boiling point (bp) via the standard temperature and pressure (STP)
    Pbp_STP_bar = 1.01325
    ln_Pbp_STP_bar = np.log(Pbp_STP_bar)

    R_kJ_per_mol_K = 0.008134
    T_298_15K = 298.15

    # ***************************************************
    #  create the required lists and file labels for the replicates (start)
    # ***************************************************
    output_column_Tbp_K_title = 'Tbp_K'
    output_column_Pbp_bar_title = 'Pbp_bar' # this is atom pressure (1.01325 bar)
    output_column_Hv_kJ_per_mol_Claus_Clap_title = 'Hv_kJ_per_mol_Claus_Clap'
    output_column_lowest_T_K_for_Tbp = "lowest_T_K_for_Tbp"
    output_column_highest_T_K_for_Tbp = "highest_T_K_for_Tbp"
    output_column_lowest_Tr_K_for_Tbp = "lowest_Tr_K_for_Tbp"
    output_column_highest_Tr_K_for_Tbp = "highest_Tr_K_for_Tbp"
    output_column_No_T_K_for_Tbp = "No_T_K_for_Tbp"

    # write the boiling data file
    output_boiling_data_replicate_txt_file_header = f"{output_column_Tbp_K_title: <30} " \
        					     f"{output_column_Pbp_bar_title: <30} " \
        					     f"{output_column_Hv_kJ_per_mol_Claus_Clap_title: <30} " \
        					     f"{output_column_lowest_T_K_for_Tbp: <30} " \
        					     f"{output_column_highest_T_K_for_Tbp: <30} " \
        					     f"{output_column_lowest_Tr_K_for_Tbp: <30} " \
        					     f"{output_column_highest_Tr_K_for_Tbp: <30} " \
        					     f"{output_column_No_T_K_for_Tbp: <30} " \
        					     f"\n"

    write_boiling_file_path_and_name = f'analysis/{output_boiling_data_replicate_txt_file_name}'
    if os.path.isfile(write_boiling_file_path_and_name):
        boiling_data_replicate_txt_file = open(write_boiling_file_path_and_name, "a")
    else:
        boiling_data_replicate_txt_file = open(write_boiling_file_path_and_name, "w")
        boiling_data_replicate_txt_file.write(output_boiling_data_replicate_txt_file_header)
    # ***************************************************
    #  create the required lists and file labels for the replicates (end)
    # ***************************************************
    # get the full list of temps, pressure, and ln(pressure) for the critical point calcs
    temps_K_for_boiling_point_list = temp_K_avg_box_vap_list
    inverse_temps_K_for_boiling_point_list = [1/ temp_bp_i for temp_bp_i in temps_K_for_boiling_point_list]
    ln_pressures_bar_for_boiling_point_list = [np.log(press_bp_i) for press_bp_i in pressure_bar_avg_box_vap_list]

    lowest_T_K_for_Tbp_replicate = temps_K_for_boiling_point_list[0]
    highest_T_K_for_Tbp_replicate = temps_K_for_boiling_point_list[-1]
    No_T_K_for_Tbp_replicate = len(temps_K_for_boiling_point_list)
    lowest_Tr_K_for_Tbp_replicate = float(temps_K_for_boiling_point_list[0] / Tc_K_replicate_list[-1])
    highest_Tr_K_for_Tbp_replicate = float(temps_K_for_boiling_point_list[-1] / Tc_K_replicate_list[-1])

    # Boilin point fit
    eq_bp_slope, eq_bp_intercept, eq_bp_r_value, eq_bp_p_value, eq_bp_std_err = \
        stats.linregress(inverse_temps_K_for_boiling_point_list, ln_pressures_bar_for_boiling_point_list)
    Tbp_iter = eq_bp_slope / ( ln_Pbp_STP_bar - eq_bp_intercept)

    Delta_Hv_kJ_per_mol_at_Claus_Clap_eval = - eq_bp_slope * R_kJ_per_mol_K

    # write the critical data
    boiling_data_replicate_txt_file.write(
        f"{Tbp_iter: <30} "
        f"{Pbp_STP_bar: <30} "
        f"{Delta_Hv_kJ_per_mol_at_Claus_Clap_eval: <30} " 
        f"{lowest_T_K_for_Tbp_replicate: <30} "
        f"{highest_T_K_for_Tbp_replicate: <30} "
        f"{lowest_Tr_K_for_Tbp_replicate: <30} "
        f"{highest_Tr_K_for_Tbp_replicate: <30} "
        f"{No_T_K_for_Tbp_replicate: <30} "
        f" \n"
    )

    # ***********************
    # calc the Boiling points (end)
    # ***********************


# ******************************************************
# ******************************************************
# data analysis - get the critical and boilin point data for each set of replicates (end)
# ******************************************************
# ******************************************************


# ******************************************************
# ******************************************************
# data analysis - get the critical and boilin point data avg and std. dev across the replicates (start)
# ******************************************************
# ******************************************************

#@Project.pre(
#     lambda * jobs: all(
#	  gomc_sim_completed_properly(job, gomc_production_control_file_name_str)
#	  for job in jobs
#     )
#)
#@Project.pre(part_5a_analysis_individual_simulation_averages_completed)
@Project.pre(part_5b_analysis_replica_averages_completed)
@Project.pre(part_5c_analysis_critical_and_boiling_points_replicate_data_completed)
@Project.post(part_5d_analysis_critical_and_boiling_points_avg_std_data_completed)
@Project.operation(directives=
     {
         "np": 1,
         "ngpu": 0,
         "memory": memory_needed,
         "walltime": walltime_gomc_analysis_hr,
     }, aggregator=aggregator.groupby(key=statepoint_without_temperature, sort_by="production_temperature_K", sort_ascending=True)
)

def part_5d_analysis_critical_and_boiling_points_avg_std_data(*jobs):
    # ***********************
    # calc the Critical points (start)
    # ***********************

    output_column_Tc_K_title = 'Tc_K'
    output_column_Rho_c_kg_per_m_cubed_title = 'Rho_c_kg_per_m_cubed'
    output_column_Pc_bar_title = 'Pc_bar'
    output_column_lowest_T_K_for_Tc = "lowest_T_K_for_Tc"
    output_column_highest_T_K_for_Tc = "highest_T_K_for_Tc"
    output_column_lowest_Tr_K_for_Tc = "lowest_Tr_K_for_Tc"
    output_column_highest_Tr_K_for_Tc = "highest_Tr_K_for_Tc"
    output_column_No_T_K_for_Tc = "No_T_K_for_Tc"

    output_column_Tc_K_std_title = 'Tc_std_K'
    output_column_Rho_c_kg_per_m_cubed_std_title = 'Rho_c_std_kg_per_m_cubed'
    output_column_Pc_bar_std_title = 'Pc_std_bar'

    output_critical_data_avg_std_txt_file_header = f"{output_column_Tc_K_title: <30} " \
        					   f"{output_column_Tc_K_std_title: <30} " \
        					   f"{output_column_Rho_c_kg_per_m_cubed_title: <30} " \
        					   f"{output_column_Rho_c_kg_per_m_cubed_std_title: <30} " \
        					   f"{output_column_Pc_bar_title: <30} " \
        					   f"{output_column_Pc_bar_std_title: <30} " \
        					   f"{output_column_lowest_T_K_for_Tc: <30} " \
        					   f"{output_column_highest_T_K_for_Tc: <30} " \
        					   f"{output_column_lowest_Tr_K_for_Tc: <30} " \
        					   f"{output_column_highest_Tr_K_for_Tc: <30} " \
        					   f"{output_column_No_T_K_for_Tc: <30} " \
        					   f"\n"

    for job in jobs:
        if job.isfile(f'../../analysis/{output_critical_data_replicate_txt_file_name}'):
            reading_file_final_critical_replicate_data = job.fn(
        	    f'../../analysis/{output_critical_data_replicate_txt_file_name}')
            data_final_critical_replicate = pd.read_csv(reading_file_final_critical_replicate_data,
        						    sep='\s+',
        						    header=0,
        						    na_values='NaN',
        						    index_col=False
        						    )

            Tc_K_final_replicate_data_list = \
        	    data_final_critical_replicate.loc[:, output_column_Tc_K_title]
            Rho_avg_box_vap_final_replicate_list = \
        	    data_final_critical_replicate.loc[:, output_column_Rho_c_kg_per_m_cubed_title]
            Pc_bar_final_replicate_data_list = \
        	    data_final_critical_replicate.loc[:, output_column_Pc_bar_title]

            lowest_T_K_for_Tc_final_replicate_data_list = \
        	    data_final_critical_replicate.loc[:, output_column_lowest_T_K_for_Tc]
            highest_T_K_for_Tc_final_replicate_data_list = \
        	    data_final_critical_replicate.loc[:, output_column_highest_T_K_for_Tc]
            lowest_Tr_K_for_Tc_final_replicate_list = \
        	    data_final_critical_replicate.loc[:, output_column_lowest_Tr_K_for_Tc]
            highest_Tr_K_for_Tc_final_replicate_list = \
        	    data_final_critical_replicate.loc[:, output_column_highest_Tr_K_for_Tc]
            No_T_K_for_Tc_final_replicate_list = \
        	    data_final_critical_replicate.loc[:, output_column_No_T_K_for_Tc]

        	# check that all replicates have same Temps used for the analysis:
            for temp_iter_k in range(0, len(lowest_T_K_for_Tc_final_replicate_data_list)):
                if len(lowest_T_K_for_Tc_final_replicate_data_list) >= 1 \
                    and len(highest_T_K_for_Tc_final_replicate_data_list) >= 1 \
                    and len(lowest_Tr_K_for_Tc_final_replicate_list) >= 1 \
                    and len(highest_Tr_K_for_Tc_final_replicate_list) >= 1 \
                    and len(No_T_K_for_Tc_final_replicate_list) >= 1:

                    if not math.isclose(lowest_T_K_for_Tc_final_replicate_data_list[0],
        				    lowest_T_K_for_Tc_final_replicate_data_list[temp_iter_k],
        				    rel_tol=0, abs_tol=1e-9
        				    ) \
        			and not math.isclose(highest_T_K_for_Tc_final_replicate_data_list[0],
        					     highest_T_K_for_Tc_final_replicate_data_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			and not math.isclose(lowest_Tr_K_for_Tc_final_replicate_list[0],
        					     lowest_Tr_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			and not math.isclose(highest_Tr_K_for_Tc_final_replicate_list[0],
        					     highest_Tr_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			and not math.isclose(No_T_K_for_Tc_final_replicate_list[0],
        					     No_T_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ):                          
                        raise ValueError("ERROR: In the critical point data, "
        				     "the replicate data temperatures or number of points used is "
        				     "different for the replicates, and they need to be the same.  ")

                else:
                    raise ValueError("ERROR: There is not 1 or any replicate data for the critical point analysis.")

            critial_data_avg_std_txt_file = open(
        	    f'analysis/{output_critical_data_avg_std_of_replicates_txt_file_name}', "w"
        	)
            critial_data_avg_std_txt_file.write(output_critical_data_avg_std_txt_file_header)

            Tc_K_mean = np.mean(Tc_K_final_replicate_data_list)
            Rho_c_kg_per_m_cubed_mean = np.mean(Rho_avg_box_vap_final_replicate_list)
            Pc_bar_mean = np.mean(Pc_bar_final_replicate_data_list)

            Tc_K_std = np.std(Tc_K_final_replicate_data_list, ddof=1)
            Rho_c_kg_per_m_cubed_std = np.std(Rho_avg_box_vap_final_replicate_list, ddof=1)
            Pc_bar_std = np.std(Pc_bar_final_replicate_data_list, ddof=1)

            lowest_T_K_for_Tc = lowest_T_K_for_Tc_final_replicate_data_list[0]
            highest_T_K_for_Tc = highest_T_K_for_Tc_final_replicate_data_list[0]
            lowest_Tr_K_for_Tc = lowest_Tr_K_for_Tc_final_replicate_list[0]
            highest_Tr_K_for_Tc = highest_Tr_K_for_Tc_final_replicate_list[0]
            No_T_K_for_Tc = No_T_K_for_Tc_final_replicate_list[0]

            critial_data_avg_std_txt_file.write(
        	    f"{Tc_K_mean: <30} "
        	    f"{Tc_K_std: <30} "
        	    f"{Rho_c_kg_per_m_cubed_mean: <30} "
        	    f"{Rho_c_kg_per_m_cubed_std: <30} "
        	    f"{Pc_bar_mean: <30} "
        	    f"{Pc_bar_std: <30} "
        	    f"{lowest_T_K_for_Tc: <30} "
        	    f"{highest_T_K_for_Tc: <30} "
        	    f"{lowest_Tr_K_for_Tc: <30} "
        	    f"{highest_Tr_K_for_Tc: <30} "
        	    f"{No_T_K_for_Tc: <30} "
        	    f" \n"
        	)
    # ***********************
    # calc the Critical points (end)
    # ***********************

    # ***********************
    # calc the Boiling points (start)
    # ***********************
    output_column_Tbp_K_title = 'Tbp_K'
    output_column_Tbp_K_std_title = 'Tbp_std_K'
    output_column_Pbp_bar_title = 'Pbp_bar'  # this is atom pressure (1.01325 bar)
    output_column_Hv_kJ_per_mol_Claus_Clap_title = 'Hv_kJ_per_mol_Claus_Clap'
    output_column_Hv_kJ_per_mol_Claus_Clap_std_title = 'Hv_std_kJ_per_mol_Claus_Clap'
    output_column_lowest_T_K_for_Tbp = "lowest_T_K_for_Tbp"
    output_column_highest_T_K_for_Tbp = "highest_T_K_for_Tbp"
    output_column_lowest_Tr_K_for_Tbp = "lowest_Tr_K_for_Tbp"
    output_column_highest_Tr_K_for_Tbp = "highest_Tr_K_for_Tbp"
    output_column_No_T_K_for_Tbp = "No_T_K_for_Tbp"

    # write the boiling data file
    output_boiling_data_avg_std_txt_file_header = f"{output_column_Tbp_K_title: <30} " \
        					  f"{output_column_Tbp_K_std_title : <30} " \
        					  f"{output_column_Pbp_bar_title: <30} " \
        					  f"{output_column_Hv_kJ_per_mol_Claus_Clap_title: <30} " \
        					  f"{output_column_Hv_kJ_per_mol_Claus_Clap_std_title: <30} " \
        					  f"{output_column_lowest_T_K_for_Tbp: <30} " \
        					  f"{output_column_highest_T_K_for_Tbp: <30} " \
        					  f"{output_column_lowest_Tr_K_for_Tbp: <30} " \
        					  f"{output_column_highest_Tr_K_for_Tbp: <30} " \
        					  f"{output_column_No_T_K_for_Tbp: <30} " \
        					  f"\n"

    for job in jobs:
        if job.isfile(f'../../analysis/{output_boiling_data_replicate_txt_file_name}'):
            reading_file_final_boiling_replicate_data = job.fn(
        	    f'../../analysis/{output_boiling_data_replicate_txt_file_name}')
            data_final_boiling_replicate = pd.read_csv(reading_file_final_boiling_replicate_data,
        						    sep='\s+',
        						    header=0,
        						    na_values='NaN',
        						    index_col=False
        						    )

            Tbp_K_final_replicate_data_list = \
        	    data_final_boiling_replicate.loc[:, output_column_Tbp_K_title]
            Pbp_bar_final_replicate_data_list = \
        	    data_final_boiling_replicate.loc[:, output_column_Pbp_bar_title]
            Hv_kJ_per_mol_Claus_Clap_final_replicate_list = \
        	    data_final_boiling_replicate.loc[:, output_column_Hv_kJ_per_mol_Claus_Clap_title]

            lowest_T_K_for_Tbp_final_replicate_data_list = \
        	    data_final_boiling_replicate.loc[:, output_column_lowest_T_K_for_Tbp]
            highest_T_K_for_Tbp_final_replicate_data_list = \
        	    data_final_boiling_replicate.loc[:, output_column_highest_T_K_for_Tbp]
            lowest_Tr_K_for_Tbp_final_replicate_list = \
        	    data_final_boiling_replicate.loc[:, output_column_lowest_Tr_K_for_Tbp]
            highest_Tr_K_for_Tbp_final_replicate_list = \
        	    data_final_boiling_replicate.loc[:, output_column_highest_Tr_K_for_Tbp]
            No_T_K_for_Tbp_final_replicate_list = \
        	    data_final_boiling_replicate.loc[:, output_column_No_T_K_for_Tbp]

        	# check that all replicates have same Temps used for the analysis:
            for temp_iter_k in range(0, len(lowest_T_K_for_Tbp_final_replicate_data_list)):
                if len(lowest_T_K_for_Tbp_final_replicate_data_list) >= 1 \
        		    and len(highest_T_K_for_Tbp_final_replicate_data_list) >= 1 \
        		    and len(lowest_Tr_K_for_Tbp_final_replicate_list) >= 1 \
        		    and len(highest_Tr_K_for_Tbp_final_replicate_list) >= 1 \
        		    and len(No_T_K_for_Tbp_final_replicate_list) >= 1:

                    if not math.isclose(lowest_T_K_for_Tbp_final_replicate_data_list[0],
        				    lowest_T_K_for_Tbp_final_replicate_data_list[temp_iter_k],
        				    rel_tol=0, abs_tol=1e-9
        				    ) \
        			    and not math.isclose(Pbp_bar_final_replicate_data_list[0],
        					     Pbp_bar_final_replicate_data_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			    and not math.isclose(highest_T_K_for_Tbp_final_replicate_data_list[0],
        					     highest_T_K_for_Tc_final_replicate_data_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			    and not math.isclose(lowest_Tr_K_for_Tbp_final_replicate_list[0],
        					     lowest_Tr_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			    and not math.isclose(highest_Tr_K_for_Tbp_final_replicate_list[0],
        					     highest_Tr_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ) \
        			    and not math.isclose(No_T_K_for_Tbp_final_replicate_list[0],
        					     No_T_K_for_Tc_final_replicate_list[temp_iter_k],
        					     rel_tol=0, abs_tol=1e-9
        					     ):
                        raise ValueError("ERROR: In the boiling point data, "
        				     "the replicate data temperatures or number of points used is "
        				     "different for the replicates, and they need to be the same.  ")

                else:
                    raise ValueError("ERROR: There is not 1 or any replicate data for the boiling point analysis.")

            boiling_data_avg_std_txt_file = open(
        	    f'analysis/{output_boiling_data_avg_std_of_replicates_txt_file_name}', "w"
        	)
            boiling_data_avg_std_txt_file.write(output_boiling_data_avg_std_txt_file_header)

            Tbp_K_mean = np.mean(Tbp_K_final_replicate_data_list)
            Tbp_K_std = np.std(Tbp_K_final_replicate_data_list, ddof=1)

            Pbp_bar = np.mean(Pbp_bar_final_replicate_data_list)

            Hv_kJ_per_mol_Claus_Clap_mean = np.mean(Hv_kJ_per_mol_Claus_Clap_final_replicate_list)
            Hv_kJ_per_mol_Claus_Clap_std = np.std(Hv_kJ_per_mol_Claus_Clap_final_replicate_list, ddof=1)

            lowest_T_K_for_Tbp = lowest_T_K_for_Tbp_final_replicate_data_list[0]
            highest_T_K_for_Tbp = highest_T_K_for_Tbp_final_replicate_data_list[0]
            lowest_Tr_K_for_Tbp = lowest_Tr_K_for_Tbp_final_replicate_list[0]
            highest_Tr_K_for_Tbp = highest_Tr_K_for_Tbp_final_replicate_list[0]
            No_T_K_for_Tbp = No_T_K_for_Tbp_final_replicate_list[0]

            boiling_data_avg_std_txt_file.write(
        	    f"{Tbp_K_mean: <30} "
        	    f"{Tbp_K_std: <30} "
        	    f"{Pbp_bar: <30} "
        	    f"{Hv_kJ_per_mol_Claus_Clap_mean: <30} "
        	    f"{Hv_kJ_per_mol_Claus_Clap_std: <30} "
        	    f"{lowest_T_K_for_Tbp: <30} "
        	    f"{highest_T_K_for_Tbp: <30} "
        	    f"{lowest_Tr_K_for_Tbp: <30} "
        	    f"{highest_Tr_K_for_Tbp: <30} "
        	    f"{No_T_K_for_Tbp: <30} "
        	    f" \n"
        	)

    # ***********************
    # calc the Boiling points (end)
    # ***********************
# ******************************************************
# ******************************************************
# data analysis - get the critical and boiling point data avg and std. dev across the replicates (end)
# ******************************************************
# ******************************************************






# ******************************************************
# ******************************************************
# signac end code (start)
# ******************************************************
# ******************************************************
if __name__ == "__main__":
    pr = Project()
    pr.main()
# ******************************************************
# ******************************************************
# signac end code (end)
# ******************************************************
# ******************************************************
