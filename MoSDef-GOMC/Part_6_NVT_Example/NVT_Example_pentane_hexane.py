# GOMC Example for the NVT Ensemble using MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the force field (FF),
# box dimensions, density, and mol ratios [1, 2, 5-10, 13-17].

import mbuild as mb
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control

FF_to_use = 'trappe-ua'

liquid_box_length_Ang = 45
liquid_box_density_kg_per_m_cubed = 642

pentane_mol_ratio = 0.5
hexane_mol_ratio = 0.5

# Create the pentane and hexane molecules with residue names
# and minimize their structures [1, 2, 13-17]¶.

# Generate the lists for the molecules, residues, and mol ratios,
# residues/molecules force fields [1, 2, 13-17].

## Note: For GOMC, the residue names are treated as molecules,
# so the residue names must be unique for each different molecule [1, 2, 13-17].


pentane = mb.load('../common/pentane.mol2')
pentane.name = 'PEN'
pentane.energy_minimize(forcefield=FF_to_use , steps=10**5)


hexane = mb.load('../common/hexane.mol2')
hexane.name = 'HEX'
hexane.energy_minimize(forcefield=FF_to_use , steps=10**5)


molecule_list = [pentane, hexane]
residues_list = [pentane.name, hexane.name]
mol_ratio_list = [pentane_mol_ratio, hexane_mol_ratio]


## Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17]

pentane_hexane_box_liq = mb.fill_box(compound=molecule_list,
                                     density=liquid_box_density_kg_per_m_cubed,
                                     compound_ratio=mol_ratio_list,
                                     box=[liquid_box_length_Ang / 10,
                                          liquid_box_length_Ang / 10,
                                          liquid_box_length_Ang / 10]
                                     )


# Build the Charmm object, which is required to write the
# FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(pentane_hexane_box_liq,
                          'NVT_pentane_hexane_liq',
                          ff_filename="NVT_pentane_hexane_FF",
                          forcefield_selection=FF_to_use,
                          residues= residues_list,
                          )


## Write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

### Note:  The electrostatics and Ewald are turned off in the
# GOMC control file (i.e., False) since the n-alkanes beads in the
# trappe-ua force field have no charge (i.e., the bead charges are all zero)

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()


gomc_control.write_gomc_control_file(charmm, 'in_NVT.conf',  'NVT', 100, 300,
                                     input_variables_dict={"ElectroStatic": False,
                                                           "Ewald": False,
                                                           }
                                     )



