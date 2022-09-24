import mbuild as mb
import unyt as u
import mosdef_gomc.formats.gmso_charmm_writer as mf_charmm
import mosdef_gomc.formats.gmso_gomc_conf_writer as gomc_control


# set the force field and create the all-atom (AA) pentane molecule via a smiles string
pentane = mb.load('CCCCC', smiles=True)
pentane.name = 'PEN'


# create the liquid and vapor boxes
box_liq = mb.fill_box(compound = [pentane],
                      n_compounds=[574],
                      box = [4.5, 4.5, 4.5])

box_vap = mb.fill_box(compound = [pentane],
                      n_compounds=[105],
                      box = [8.0, 8.0, 8.0])


# build the MoSDeF Charmm object
charmm = mf_charmm.Charmm(box_liq,
                          'GEMC_NVT_n_pentane_liq',
                          structure_box_1=box_vap,
                          filename_box_1='GEMC_NVT_n_pentane_vap',
                          ff_filename="GEMC_NVT_n_pentane_FF",
                          forcefield_selection='oplsaa',
                          residues=[pentane.name],
                          bead_to_atom_name_dict=None,
                          gomc_fix_bonds_angles=None,
                          )

# write the pdb, psf, and inp (parameter/force field) files
charmm.write_inp()
charmm.write_psf()
charmm.write_pdb()

# create the GOMC control file
gomc_control.write_gomc_control_file(charmm, 'in_GEMC_NVT.conf',  'GEMC_NVT', 100, 300 * u.Kelvin,
                                     input_variables_dict={"Potential" : 'SWITCH',
                                                           "Rswitch" : 10 * u.angstrom,
                                                           "Rcut": 12 * u.angstrom,
                                                           "RcutLow": 1 * u.angstrom,
                                                           "VDWGeometricSigma": True
                                                           }
                                     )

