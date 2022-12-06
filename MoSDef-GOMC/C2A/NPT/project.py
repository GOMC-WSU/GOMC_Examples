#project.py

import signac
import os
from os.path import isfile
import shutil
import json
import glob
import subprocess
import mbuild as mb
import numpy as np
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control
import flow
from flow import FlowProject
from flow.environment import DefaultSlurmEnvironment
import warnings

## define project
project=signac.init_project('C2A-NPT')

class Project(FlowProject):
    """Subclass of FlowProject to provide custom methods and attributes."""

    def __init__(self):
        super().__init__()


class Local(DefaultSlurmEnvironment):  # Grid(StandardEnvironment):
    """Subclass of DefaultSlurmEnvironment for WSU's Grid cluster."""
    #signac seems to have trouble setting the environment variable with the fully qualified
    #for the grid, use:
    #hostname_pattern = r".*\.grid\.wayne\.edu"

    template = "local.sh"

@FlowProject.label
def sim_started(job):
    return job.isfile('out.dat')

@FlowProject.label
def averages_written(job):
    return job.isfile('dens0.dat')

@FlowProject.label
def input_written(job):
    input_written_bool=False
    if job.isfile("in_NPT.conf"):
        input_written_bool = True
    return input_written_bool

@FlowProject.label
def job_completed(job):
    simulation_complete_bool = False
    if job.isfile("out.dat"):
        with open("workspace/{job.id}/out.dat", "r") as fp:
            if "Completed" in fp:
                simulation_complete_bool=True

    return simulation_complete_bool

#build system
@FlowProject.operation
@FlowProject.post(input_written)
def build_input(job):
    warnings.filterwarnings('ignore')

 #   working_dir=os.getcwd()

    # gives an initial density of ~ 0.2 
    Liquid_box_length_Ang = 50
    Liquid_box_total_molecules = 500

    forcefield_file = 'trappe-ua'
    FF_Molecule = Forcefield(name = forcefield_file)
    Molecule = mb.load('files/ethane.mol2')
# PROBLEM IS THIS LINE HERE:
    #Molecule.energy_minimize(forcefield = forcefield_file, steps=10**4)
    Molecule.name = 'C2A'

    Molecule_Type_List = [Molecule]
    Molecule_mol_ratio_List = [1]
    Molecules_of_each_type_liquid_list = [int(Liquid_box_total_molecules) ]

    Molecule_ResName_List = [Molecule.name]

    Bead_to_atom_name_dict = { '_CH3':'C', '_CH2':'C',  '_CH':'C', '_HC':'C'} #{'_CH3':'C', '_CH2':'C', '_CH':'C', '_HC':'C'}

    forcefield_files = {Molecule.name : forcefield_file}

    print('Running: liquid phase box packing')
    box_liq = mb.fill_box(compound = Molecule_Type_List,
                      n_compounds=Molecules_of_each_type_liquid_list,
                      box = [Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10])

    print('Completed: liquid phase box packing')

    print('Running: GOMC FF file, and the psf and pdb files')
    #needed to write files in each directory
    with(job):

        charmm = mf_charmm.Charmm(box_liq,
                          'C2A_input',
                          structure_box_1 =None  ,
                          filename_box_1 = None,
                          ff_filename ="C2A_FF" ,
                          forcefield_selection  = forcefield_files ,
                          residues= Molecule_ResName_List ,
                          bead_to_atom_name_dict = Bead_to_atom_name_dict ,
                          gomc_fix_bonds_angles = None,
                         )

        charmm.write_inp()

        charmm.write_psf()

        charmm.write_pdb()

        Temperature=float(job.sp.Temperature)
        Pressure=float(job.sp.Pressure)
        MC_steps=20000000
        Output_name='C2A_output'
        gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf',  'NPT', MC_steps, Temperature,
                                         input_variables_dict={"Pressure": Pressure,
                                                            "OutputName": Output_name,
                                                            "VDWGeometricSigma": False,
                                                            "LRC":True,
                                                            "Rcut": 10,
                                                            "RcutLow" : 1,
                                                            "Ewald":False,
                                                            "ElectroStatic":False,
                                                            "DisFreq":0.40,
                                                            "RotFreq":0.40,
                                                            "RegrowthFreq":0.1,
                                                            "SwapFreq": 0.0,
                                                            "VolFreq": 0.01,
                                                            "IntraSwapFreq":0.09,
                                                            "EqSteps":5000000,
                                                            "PressureCalc":[False, 1000000],
                                                            "BlockAverageFreq":[True, 1000000],
                                                            "HistogramFreq":[False,10000],
                                                            "CheckpointFreq":[True, 5000000],
                                                            "RestartFreq":[True, 5000000],
                                                            "CoordinatesFreq":[False, 5000000],
                                                            "DCDFreq":[True,1000000],
                                                            "OutPressure":[False, False],
                                                            "CBMC_First":12,
                                                            "CBMC_Nth":10,
                                                            "CBMC_Ang":50,
                                                            "CBMC_Dih":50
                                                               }
                                     )

        print('Completed: GOMC FF file, and the psf and pdb files')

# ==completed build ###
# run job

@FlowProject.pre(input_written)
@FlowProject.post(sim_started)
@FlowProject.operation
@flow.with_job
@flow.cmd
def run_gomc_command(job):
    run_command="~/bin/GOMC_CPU_NPT +p2 in_NPT.conf >out.dat"
    
    #os.system(run_command)

    #exec_run_command = subprocess.Popen(
    #        run_command, shell=True, stderr=subprocess.STDOUT)
    #os.waitpid(exec_run_command.pid, 0)  # os.WSTOPPED) # 0)
    return run_command



   
if __name__ == '__main__':
    FlowProject().main()


