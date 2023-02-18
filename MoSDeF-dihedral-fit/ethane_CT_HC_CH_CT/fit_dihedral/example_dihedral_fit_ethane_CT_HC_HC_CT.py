
import unyt as u
from mosdef_dihedral_fit.dihedral_fit.fit_dihedral_with_gomc import fit_dihedral_with_gomc


# The MoSDeF force field (FF) XML file which will be used
FF_XML_file = \
    '../src/ff_xml/oplsaa_ethane_CT_HC_HC_CT.xml'

# The mol2 file which is used.
mol2_file = \
    '../src/starting_coords/ethane_aa.mol2'

# The temperature of the Molecular Mechanics (MM) simulation.
temperature_in_unyt_units = 298.15 * u.Kelvin

# Choose mixing rule (override_VDWGeometricSigma_bool) to override use the bool (True or False)
# that was chosen in the force field (FF) XML file.  This variable is not required and will be
# selected automatically; however, you should override to the correct setting if unsure.
override_VDWGeometricSigma_bool = True

# Atom type naming convention ( str, optional, default=’all_unique’, (‘general’ or ‘all_unique’) )
# General is safe and recommended since we are using a single FF XML file.
atom_type_naming_style = 'general'

# the GOMC binary path
gomc_binary_directory = "/Users/brad/Programs/GOMC/GOMC_2_75/bin"


# Load 1 or more Gaussian file (key), and the value ([0]) is a list of Gaussian point to remove
# from the fitting process.  More than 1 Gaussian file can be loaded, allowing the user
# to run multiple dihedral angles in separate file, minimizing the time required to run
# the simimulaiton (i.e., the user can split them up into many simulations to obtain
# the full dihedral rotation.)
log_files_and_removed_points = {
    '../src/guassian_runs_multiplicity_1/HC_CT_CT_HC_multiplicity_1.log': [0],
}

# The dihedral which is being fit
fit_dihedral_atom_types = ['HC', 'CT', 'CT', 'HC']

# All the other dihedrals which can be zeroed in the fitting process, in a nexted list
zeroed_dihedrals = None

# run the "fit_dihedral_with_gomc" command
fit_dihedral_with_gomc(
    fit_dihedral_atom_types,
    mol2_file,
    FF_XML_file,
    temperature_in_unyt_units,
    gomc_binary_directory,
    log_files_and_removed_points,
    zeroed_dihedral_atom_types=zeroed_dihedrals,
    qm_engine="gaussian",
    override_VDWGeometricSigma=override_VDWGeometricSigma_bool,
    atom_type_naming_style=atom_type_naming_style,
    gomc_cpu_cores=1,
    fit_min_validated_r_squared=0.99,
    fit_validation_r_squared_rtol=1e-03
)
