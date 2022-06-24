# GOMC Example for the TIP4P-2005 water with the NPT Ensemble via MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the box dimensions and number of molecules. [1, 2, 5-10, 13-17].

import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control

Liquid_box_length_Ang = 32.1
Liquid_box_Total_molecules = 1100

# Create the TIP4P-2005 water with residue names [1, 2, 13-17].

# Generate the list for the molecules and residues.
# Make the dictionaries to customize the bead's atoms names, and set the residues/molecules force fields [1, 2, 13-17].

# Note: For GOMC, the residue names are treated as molecules,
# so the residue names must be unique for each different molecule [1, 2, 13-17].
# The force field (FF) dictionary (forcefield_files variable) can set each residue
# with a different FF, by the FF name (via the foyer FF repository)
# or a specified FF xml file [1, 2, 13-17].

# NOTE: The exact bond, angle, and configuration (i.e., a planar water) must be set in the .mol2 file [1, 2, 13-17].
# When using a TIP4P water, minimizing the structure here could result in the lone pair being
# pushed in out of plane [1, 2, 13-17].
# Therefore, if you need to minimize the sytem, we recommend minimizing it in an engine that takes that
# into consideration [1, 2, 13-17].

forcefield_files_water = '../common/tip4p_2005_oplsaa.xml'
water = mb.load('../common/tip4p_2005.mol2')
water.name = 'H2O'

Molecule_Type_list = [water]
Molecules_of_each_type_Liquid_list = [int(Liquid_box_Total_molecules)]

Molecule_ResName_list = [water.name]

Bead_to_atom_name_dict = { '_LP':'LP'}

forcefield_files = forcefield_files_water

fixed_bonds_angles_list = [water.name]


# Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17]

box_liq = mb.fill_box(compound=Molecule_Type_list,
                      n_compounds=Molecules_of_each_type_Liquid_list,
                      box=[Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10])

# Build the Charmm object, which is required to write the
# FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]
# NOTE: You must set the gomc_fix_bonds_angle for water or the angles
# will be off, and the lone pair may not stay in plane.

charmm = mf_charmm.Charmm(box_liq,
                          'NPT_TIP4P_2005_water_liq',
                          structure_box_1=None,
                          filename_box_1=None,
                          ff_filename ="NPT_TIP4P_2005_water_FF",
                          forcefield_selection=forcefield_files,
                          residues=Molecule_ResName_list,
                          bead_to_atom_name_dict=Bead_to_atom_name_dict,
                          gomc_fix_bonds_angles=fixed_bonds_angles_list,
                         )

## Write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()


gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf',  'NPT', 1000, 300,
                                     input_variables_dict={"Pressure": 1.01325}
                                     )
