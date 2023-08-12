# GOMC Example for the Exp6 FF GMSO version NVT Ensemble using MoSDeF [1, 2, 5-10, 13-17]

# Import the required packages and specify the force field (FF),
# box dimensions, density, and mol ratios [1, 2, 5-10, 13-17].

import mbuild as mb
import unyt as u
import mosdef_gomc.formats.gmso_charmm_writer as mf_charmm
import mosdef_gomc.formats.gmso_gomc_conf_writer as gomc_control


FF_to_use = '../common/gmso_hexane_Exp6_periodic_dihedral_ua_K_energy_units.xml'

liquid_box_length_Ang = 45
liquid_box_density_kg_per_m_cubed = 642


# Create the hexane molecule with residue names

# Generate the lists for the molecule, residue, and
# residues/molecules force fields [1, 2, 13-17].

## Note: For GOMC, the residue names are treated as molecules,
# so the residue names must be unique for each different molecule [1, 2, 13-17].

## Note: When importing mol2 files, the residue names (hexane.name) must be the same name as in the mol2 file.

hexane = mb.load('../common/hexane.mol2')
hexane.name = 'HEX'

molecule_list = [hexane]
residues_list = [hexane.name]

## Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17]

hexane_box_liq = mb.fill_box(compound=molecule_list,
                             density=liquid_box_density_kg_per_m_cubed,
                             compound_ratio=[1],
                             box=[
                                 liquid_box_length_Ang / 10,
                                 liquid_box_length_Ang / 10,
                                 liquid_box_length_Ang / 10
                                  ]
                             )


# Build the Charmm object, which is required to write the
# FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(hexane_box_liq,
                          'NVT_hexane_exp6_liq',
                          ff_filename="NVT_hexane_exp6_FF",
                          forcefield_selection=FF_to_use,
                          residues= residues_list,
                          atom_type_naming_style="general",
                          )


## Write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()


gomc_control.write_gomc_control_file(charmm, 'in_NVT.conf',  'NVT', 100, 300 * u.Kelvin,
                                     input_variables_dict={},
                                     )
