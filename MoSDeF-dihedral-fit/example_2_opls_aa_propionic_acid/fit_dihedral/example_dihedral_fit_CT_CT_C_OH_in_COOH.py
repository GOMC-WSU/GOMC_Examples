import unyt as u
from mosdef_dihedral_fit.dihedral_fit.fit_dihedral_with_gomc import fit_dihedral_with_gomc
import os

# The MoSDeF force field (FF) XML file which will be used.
forcefield_file = '../src/ff_xml/oplsaa_CT_CT_C_OH_in_COOH.xml'

# The mol2 file which is used.
mol2_file = '../src/starting_coords/CT_CT_C_3_OH.mol2'

# The temperature of the Molecular Mechanics (MM) simulation.
temperature_in_unyt_units = 25 * u.Celcius


# Override the chosen mixing rule (combining_rule), 'geometric' or 'lorentz'),
# which was set in the force field (FF) XML file.  This variable is not required and will be
# selected automatically; however, you can override it if you are unsure of the setting.
combining_rule = 'geometric'

# Atom type naming convention [str, optional, default='all_unique', ('general' or 'all_unique')].
# -----------------------------------------------------------------------------------------------
# Using 'general' is preferred as it makes it easier to create the force field (FF) and is much 
# more human readable.  For CHARMM-style FFs, like GOMC and NAMD, this means that all the general 
# atom/bead types that are in an atom class must have the same non-bonded VDW parameters 
# (i.e., for LJ -> sigma and epsilon), but are allowed to have different partial charges; 
# otherwise, it will cause errors. This is because the partial charges are listed in the PSF file 
# for each atom individually, and not in the NAMD or GOMC FF file (.inp).   
# Typically, the bonded parameters are all handled as using general atom/bead classes 
# (Example: the carbon atoms in butane (C in CH3 and C in CH2) would have the same VDW and bonded 
# parameters, but will have different partial charges). The 'general' setting allows the fitting 
# of a group of atom/bead types together as an same atom class, where atom/bead class is 
# determined in the FF XML file for each atom/bead type.
# -----------------------------------------------------------------------------------------------
# Using 'all_unique' basically sets each atom type as its own separate atom class.  Therefore, 
# there is no distinction between atom type and atom class. This dihedral fit will on take into 
# account the specific atom type, and not fit the general class (ignoring any FF XML file settings), 
# which may make some dihedral fits more difficult. However, this could be the desired outcome in 
# some situations.  Note: The MoSDeF force field does allow specific atom type dihedrals and other 
# bonded parameters, which override the atom class values, but all the atoms in the bonded FF 
# parameters must be the atom types.  
atom_type_naming_style = 'general'

# The GOMC binary path.
gomc_binary_directory = "path_to_GOMC_folder_GOMC_2_75/bin"

# Load 1 or more Gaussian files (keys), and its value ([0]), which is a list of Gaussian points to remove
# from the fitting process, where the first minimized Gaussian point is removed (i.e., ([0])).
# More than 1 Gaussian file can be loaded, allowing the user to run multiple dihedral angles in separate file,
# minimizing the time required to run the simulations
# (i.e., the user can split them up into many simulations to obtain the full dihedral rotation).
qm_log_file_dict = {
    '../src/gaussian_style_output_files/CT_CT_C_OH_split_part_1/output': [],
    '../src/gaussian_style_output_files/CT_CT_C_OH_split_part_2/output': [],
}

# The dihedral which is being fit.
fit_dihedral_atom_types = ['CT', 'CT', 'C', 'OH']

# All the other dihedrals which can be zeroed in the fitting process, in a nested list
zero_dihedral_atom_types = [['CT', 'CT', 'C', 'O_3']]

# Run the "fit_dihedral_with_gomc" command.
fit_dihedral_with_gomc(
    fit_dihedral_atom_types,
    mol2_file,
    forcefield_file,
    temperature_in_unyt_units,
    gomc_binary_directory,
    qm_log_file_dict,
    manual_dihedral_atom_numbers_list=[3, 2, 1, 4],
    zero_dihedral_atom_types=zero_dihedral_atom_types,
    qm_engine="gaussian_style_final_files",
    combining_rule=combining_rule,
    atom_type_naming_style=atom_type_naming_style,
    gomc_cpu_cores=1,
    r_squared_min=0.99,
    r_squared_rtol=5e-03,
    opls_force_k0_zero=True
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
