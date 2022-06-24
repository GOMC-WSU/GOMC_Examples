# GOMC Example for the Grand Canonical (GCMC) Ensemble using MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the box information, 
# mol ratios, and FF being used [1, 2, 5-10, 13-17].

## Note: Box 0 is the simulated box and Box 1 is the reservoir for the simulation.


import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control

Box_0_box_length_Ang = 45
Box_0_box_Total_molecules = 574

Box_1_box_length_Ang = 175
Box_1_box_Total_molecules = 105

Molecule_A_mol_ratio = 0.5
Molecule_B_mol_ratio = 0.5


forcefield_files = 'trappe-ua'
FF =  Forcefield(name = forcefield_files )


# Select the united-atom (UA) molecules mol2 files and set the residue name, molecule types, and box 0 & 1 values.  Box 1 is the reservoir.

# Note: For GOMC, the residue names are treated as molecules, so the residue names must be unique for each different molecule [1, 2, 13-17].

Molecule_A =mb.load('../common/pentane.mol2')
FF.apply(Molecule_A)
Molecule_A.name = 'PEN'

Molecule_B =mb.load('../common/hexane.mol2')
FF.apply(Molecule_B)
Molecule_B.name = 'HEX'


Molecule_Type_List = [Molecule_A, Molecule_B]
Molecule_mol_ratio_List = [Molecule_A_mol_ratio, Molecule_B_mol_ratio]
Molecules_of_each_type_Box_0_List = [int(Box_0_box_Total_molecules * Molecule_A_mol_ratio),
                                      int(Box_0_box_Total_molecules * Molecule_B_mol_ratio) ]
Molecules_of_each_type_Box_1_List = [int(Box_1_box_Total_molecules * Molecule_A_mol_ratio),
                                      int(Box_1_box_Total_molecules * Molecule_B_mol_ratio) ]

# Put the residue names in a list for the Charmm object writer  [5-10, 13-17].  

# Select the bead_to_atom_name_dict parameters, which changes the long force field specified atom name to a shorter version that will fit in the pdb files, allowing unique atom names for each atom per molecule.  This unique atom naming allows the special Monte Carlo (MC) moves to be applied in GOMC [5-10, 13-17].

Molecule_ResName_List = [Molecule_A.name, Molecule_B.name ]

bead_to_atom_name_dict = { '_CH3':'C', '_CH2':'C',  '_CH':'C', '_HC':'C'} #{'_CH3':'C', '_CH2':'C', '_CH':'C', '_HC':'C'}



# Build the main simulation box (box 0) and its reservoir (box 1) for the simulation

box_0 = mb.fill_box(compound = Molecule_Type_List,
                    n_compounds=Molecules_of_each_type_Box_0_List,
                    box = [Box_0_box_length_Ang/10,
                           Box_0_box_length_Ang/10,
                           Box_0_box_length_Ang/10])


box_1 = mb.fill_box(compound = Molecule_Type_List,
                    n_compounds=Molecules_of_each_type_Box_1_List,
                    box = [Box_1_box_length_Ang/10 ,
                           Box_1_box_length_Ang/10 ,
                           Box_1_box_length_Ang/10 ])


## Build the Charmm object, which is required to write the force field (.inp), psf, pdb, and GOMC control files  [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(box_0,
                          'GCMC_n_pentane_n_hexane_Box_0',
                          structure_box_1=box_1,
                          filename_box_1='GCMC_n_pentane_n_hexane_Box_1',
                          ff_filename ="GCMC_n_pentane_n_hexane_FF",
                          forcefield_selection=forcefield_files,
                          residues= Molecule_ResName_List,
                          bead_to_atom_name_dict=bead_to_atom_name_dict ,
                          gomc_fix_bonds_angles=None,
                         )


## Write the write the force field (.inp), psf, pdb, and GOMC control files  [1, 2, 5-10, 13-17]

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()

gomc_control.write_gomc_control_file(charmm, 'in_GCMC.conf',  'GCMC', 100, 300,
                                     input_variables_dict = {
                                         "ChemPot" : {"PEN" : -4000, "HEX" : -8000}
                                     }
                                     )

print('Completed: GOMC FF file, and the psf and pdb files')
