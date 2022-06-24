# GOMC Example for calculating the free energy of neon in cyclohexane with
# the NPT Ensemble via MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the box dimensions and number of molecules. [1, 2, 5-10, 13-17].
# NOTE: Only 1 neon is used to do the free energy calculation of neon in cyclohexane
import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control

Liquid_box_length_Ang = 38.0

liquid_box_neon_molecules = 1
liquid_box_cyclohexane_molecules = 300

# Create the neon and cyclohexane with residue names [1, 2, 13-17].

# Generate the list for the molecules and residues.
# Make the dictionaries to customize the bead's atoms names, and set the residues/molecules force fields [1, 2, 13-17].

# Note: For GOMC, the residue names are treated as molecules,
# so the residue names must be unique for each different molecule [1, 2, 13-17].
# The force field (FF) dictionary (forcefield_files variable) can set each residue
# with a different FF, by the FF name (via the foyer FF repository)
# or a specified FF xml file [1, 2, 13-17].

forcefield_files_neon = '../common/neon_LB_mixing.xml'
neon = mb.Compound(name="Ne")

forcefield_files_cyclohexane = '../common/cyclohexane-ua.xml'
cyclohexane = mb.load('../common/cyclohexane-ua.mol2')
cyclohexane.name = 'CHX'

Molecule_Type_list = [neon, cyclohexane]
Molecules_of_each_type_Liquid_list = [int(liquid_box_neon_molecules),
                                      int(liquid_box_cyclohexane_molecules)
                                      ]

Molecule_ResName_list = [neon.name, cyclohexane.name]

Bead_to_atom_name_dict = { '_CH2': 'C'}

forcefield_files = {neon.name: forcefield_files_neon,
                    cyclohexane.name: forcefield_files_cyclohexane
                    }

# Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17].

box_liq = mb.fill_box(compound=Molecule_Type_list,
                      n_compounds=Molecules_of_each_type_Liquid_list,
                      box=[Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10])

# Build the Charmm object, which is required to write the FF (.inp), psf, pdb, and
# GOMC control files and write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(box_liq,
                          'NPT_neon_cyclohexane_liq',
                          structure_box_1=None,
                          filename_box_1=None,
                          ff_filename ="NPT_neon_cyclohexane_FF",
                          forcefield_selection=forcefield_files,
                          residues=Molecule_ResName_list,
                          bead_to_atom_name_dict=Bead_to_atom_name_dict,
                          gomc_fix_bonds_angles=None,
                         )

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()

# In this Example, six (6) separate GOMC simulaitons are needed to calculate the free energy, one (1) for each of the
# six (6) lambda states (0.0, 0.2, 0.4, 0.6, 0.8, 1).
# Therefore, 6 separate GOMC files need written, one for each of the six lambda states 0 to 5.

# NOTE: The actual free energy simulation will need to be run longer, as this is just a quick example.
# NOTE: Depending on the exact system, more or less lambda states may be required to get accurate results.

# Set the variables that will be used for all the lambda states

Rcut = 15
Pressure = 1.01325
CBMC_First = 12
CBMC_Nth = 10
CBMC_Ang = 50
CBMC_Dih = 50
FreeEnergyCalc = [True, 1000]
MoleculeType = [neon.name, 1]
lambda_states =[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

simulation_temp = 300
simulation_steps = 10000

# The GOMC control file for lambda state 0 (InitialState=0).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_0.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 0,
                                         "OutputName": "out_NPT_lambda_number_0"
                                     }
                                     )

# The GOMC control file for lambda state 1 (InitialState=1).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_1.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 1,
                                         "OutputName": "out_NPT_lambda_number_1"
                                     }
                                     )

# The GOMC control file for lambda state 2 (InitialState=2).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_2.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 2,
                                         "OutputName": "out_NPT_lambda_number_2"
                                     }
                                     )

# The GOMC control file for lambda state 3 (InitialState=3).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_3.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 3,
                                         "OutputName": "out_NPT_lambda_number_3"
                                     }
                                     )

# The GOMC control file for lambda state 4 (InitialState=4).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_4.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 4,
                                         "OutputName": "out_NPT_lambda_number_4"
                                     }
                                     )

# The GOMC control file for lambda state 5 (InitialState=5).
gomc_control.write_gomc_control_file(charmm, 'in_NPT_lambda_number_5.conf', 'NPT', simulation_steps, simulation_temp,
                                     input_variables_dict={
                                         "Rcut": Rcut,
                                         "Pressure": Pressure,
                                         "CBMC_First": CBMC_First,
                                         "CBMC_Nth": CBMC_Nth,
                                         "CBMC_Ang": CBMC_Ang,
                                         "CBMC_Dih": CBMC_Dih,
                                         "FreeEnergyCalc": FreeEnergyCalc,
                                         "MoleculeType": MoleculeType,
                                         "LambdaVDW": lambda_states,
                                         "InitialState": 5,
                                         "OutputName": "out_NPT_lambda_number_5"
                                     }
                                     )
