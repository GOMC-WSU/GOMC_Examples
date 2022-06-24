# GOMC Example for the NPT Ensemble via MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the box dimensions, number of molecules, and mol ratios [1, 2, 5-10, 13-17].

import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control

Liquid_box_length_Ang = 45
Liquid_box_Total_molecules = 850

hexane_mol_ratio = 0.5
water_mol_ratio = 0.5

# Create the water and hexane molecules with residue names [1, 2, 13-17].

# Generate the list for the molecules, residues, and mol ratios.
# Make the dictionaries to customize the bead's atoms names, and set the residues/molecules force fields [1, 2, 13-17].

# Note: For GOMC, the residue names are treated as molecules,
# so the residue names must be unique for each different molecule [1, 2, 13-17].
# The force field (FF) dictionary (forcefield_files variable) can set each residue
# with a different FF, by the FF name (via the foyer FF repository)
# or a specified FF xml file [1, 2, 13-17].

forcefield_files_hexane = 'trappe-ua'
hexane =mb.load('../common/hexane.mol2')
hexane.energy_minimize(forcefield = forcefield_files_hexane , steps=10**4)
hexane.name = 'HEX'

forcefield_files_water = '../common/spce_trappe.xml'
water = mb.load('O', smiles=True)
water.energy_minimize(forcefield = forcefield_files_water , steps=10**4)
water.name = 'H2O'

Molecule_Type_list = [hexane, water]
Molecule_mol_ratio_list = [hexane_mol_ratio, water_mol_ratio]
Molecules_of_each_type_Liquid_list = [int(Liquid_box_Total_molecules * hexane_mol_ratio),
                                      int(Liquid_box_Total_molecules * water_mol_ratio)]

Molecule_ResName_list = [hexane.name, water.name ]

Bead_to_atom_name_dict = { '_CH3':'C', '_CH2':'C',  '_CH':'C', '_HC':'C'}

forcefield_files = {hexane.name : forcefield_files_hexane , water.name : forcefield_files_water}

fixed_bonds_angles_list = [water.name]


# Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17]

box_liq = mb.fill_box(compound=Molecule_Type_list,
                      n_compounds=Molecules_of_each_type_Liquid_list,
                      box=[Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10])

# Build the Charmm object, which is required to write the
# FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(box_liq,
                          'NPT_n_hexane_water_liq',
                          structure_box_1=None  ,
                          filename_box_1=None,
                          ff_filename ="NPT_n_hexane_water_FF" ,
                          forcefield_selection=forcefield_files ,
                          residues=Molecule_ResName_list ,
                          bead_to_atom_name_dict=Bead_to_atom_name_dict ,
                          gomc_fix_bonds_angles=fixed_bonds_angles_list,
                         )

## Write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()


gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf',  'NPT', 100, 300,
                                     input_variables_dict={"Pressure": 10}
                                     )
