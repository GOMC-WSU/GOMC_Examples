import unyt as u
from mosdef_dihedral_fit.dihedral_fit.fit_dihedral_with_gomc import fit_dihedral_with_gomc
import os

# The MoSDeF force field (FF) XML file which will be used.
forcefield_file = '../src/ff_xml/trappe_ua_butane_CT_CT_CT_CT_gmso.xml'

# The mol2 file which is used.
mol2_file = '../src/starting_coords/butane_aa.mol2'

# The temperature of the Molecular Mechanics (MM) simulation.
temperature_in_unyt_units = 298.15 * u.Kelvin

# Override the chosen mixing rule (combining_rule), 'geometric' or 'lorentz'),
# which was set in the force field (FF) XML file.  This variable is not required and will be
# selected automatically; however, you can override it if you are unsure of the setting.
# selecting None uses the one in the forcefield xml file. 
combining_rule = None

# Atom type naming convention ( str, optional, default=’all_unique’, (‘general’ or ‘all_unique’) )
# Using 'general' is preferred as it makes it easier to create the force field (FF) and makes it 
# and the other generated files more readable.  However, to the 'general' option, the user needs 
# to make sure that all the FF atomclasses in the FF XML file (i.e., atomclass="CT") have the same 
# sigma and epsilon values. Otherwise, it will cause errors.
atom_type_naming_style = 'general'

# The GOMC binary path.
gomc_binary_directory = "/home/brad/Programs/GOMC/GOMC-2.75a/bin" 
#"path_to_GOMC_folder_GOMC_2_75/bin"

# Load 1 or more Gaussian files (keys), and its value ([0]), which is a list of Gaussian points to remove
# from the fitting process, where the first minimized Gaussian point is removed (i.e., ([0])).
# More than 1 Gaussian file can be loaded, allowing the user to run multiple dihedral angles in separate file,
# minimizing the time required to run the simulations
# (i.e., the user can split them up into many simulations to obtain the full dihedral rotation).
qm_log_file_dict = {
    '../src/gaussian_style_output_files/CT_CT_CT_CT': [],
}

# The dihedral which is being fit.
fit_dihedral_atom_types = ['CH3', 'CH2', 'CH2', 'CH3']

# All the other dihedrals which can be zeroed in the fitting process, in a nested list
zero_dihedral_atom_types = None

# Run the "fit_dihedral_with_gomc" command.
fit_dihedral_with_gomc(
    fit_dihedral_atom_types,
    mol2_file,
    forcefield_file,
    temperature_in_unyt_units,
    gomc_binary_directory,
    qm_log_file_dict,
    manual_dihedral_atom_numbers_list=[1 ,2, 3, 4],
    zero_dihedral_atom_types=zero_dihedral_atom_types,
    qm_engine="gaussian_style_final_files",
    combining_rule=combining_rule,
    atom_type_naming_style=atom_type_naming_style,
    gomc_cpu_cores=1,
    r_squared_min=0.98,
    r_squared_rtol=0.02,
    opls_force_k0_zero=False
)

# The OPLS dihedral fit constants
print('The OPLS dihedral fit constants:\n')
os.system("cat opls_dihedral_k_constants_fit_energy.txt")

# The converted OPLS to periodic dihedral fit constants
print('The converted OPLS to periodic dihedral fit constants:\n')
os.system("cat periodic_dihedral_k_constants_fit_energy.txt")

# The converted OPLS to RB-torsions dihedral fit constants
print('The converted OPLS to RB-torsions dihedral fit constants:\n')
os.system("cat RB_torsion_k_constants_fit_energy.txt")

# This file contains the raw points used in the fits (QM - MM_less_dihedral(s)_energy being fit)
print('This file contains the raw points used in the fits (QM - MM_less_dihedral(s)_energy being fit):\n')
os.system("cat all_normalized_energies_in_kcal_per_mol.txt")
