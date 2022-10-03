# Benzene's NPT Ensemble using the GMSO FF XML style and the GAFF FF via MoSDeF [1, 2, 5-10, 13-17]

# NOTE: This format will not work correctly for BENZENE using the GOMC engine because this
# GAFF FF for BENZENE uses impropers, and GOMC does not currently support impropers.
# However, the GAFF FF for BENZENE can be used for the NAMD engine because NAMD does support impropers.

# Import the required packages and specify the box dimensions, and number of molecules [1, 2, 5-10, 13-17].

import mbuild as mb
import unyt as u
import mosdef_gomc.formats.gmso_charmm_writer as mf_charmm
import mosdef_gomc.formats.gmso_gomc_conf_writer as gomc_control

Liquid_box_length_Ang = 42.17
Liquid_box_Total_molecules = 400


# Create the benzene molecules with a residue name [1, 2, 13-17].

# Generate the list for the molecules, and residues.

# Set the residue/molecule force field [1, 2, 13-17].

# Note: For GOMC, the residue names are treated as molecules names,
# so the residue names must be unique for each different molecule [1, 2, 13-17].
# The force field (FF) dictionary (forcefield_files variable) can set each residue
# with a different FF, by the FF name (via the foyer FF repository)
# or a specified FF xml file [1, 2, 13-17].
# Here we are just entering FF as a string, which applies the FF to all molecules.

forcefield_files_benzene = '../common/gmso_benzene_GAFF.xml'
benzene = mb.load('c1ccccc1', smiles=True)
benzene.name = 'BEN'

Molecule_Type_list = [benzene]

Molecule_ResName_list = [benzene.name]

# Build the main liquid simulation box (box 0) for the simulation [1, 2, 13-17]

box_liq = mb.fill_box(compound=Molecule_Type_list,
                      n_compounds=Liquid_box_Total_molecules,
                      box=[Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10,
                           Liquid_box_length_Ang/10
                           ]
                      )

# Build the Charmm object, which is required to write the
# FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm = mf_charmm.Charmm(box_liq,
                          'NPT_benzene_liq',
                          structure_box_1=None,
                          filename_box_1=None,
                          ff_filename ="NPT_benzene_FF" ,
                          forcefield_selection=forcefield_files_benzene,
                          residues=Molecule_ResName_list,
                         )

## Write the write the FF (.inp), psf, pdb, and GOMC control files [1, 2, 5-10, 13-17]

charmm.write_inp()

charmm.write_psf()

charmm.write_pdb()


gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf',  'NPT', 100, 450 * u.Kelvin,
                                     input_variables_dict={"Pressure": 22.30447 * u.atm}
                                     )
