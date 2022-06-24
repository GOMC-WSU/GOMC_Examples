# Obtaining the Charmm object and GOMC control file parameters via MoSDeF 

# Import the required packages
import mbuild.formats.charmm_writer as mf_charmm
import mbuild.formats.gomc_conf_writer as gomc_control


# Obtaining the Charmm object variable parameters, attributes, and functions [5-10, 13-17]
help(mf_charmm.Charmm)


# Display the required inputs for the GOMC control file writer (write_gomc_control_file function) via the print_required_input function [1, 2, 13-17]

# The examples show the required variables in the function. 

# Example ->   gomc_control.write_gomc_control_file(Charmm_object, 'GOMC_control_file_name(.conf)',
#                                                   Ensemble_type, No_of_steps, Temp_K)
# Example ->   gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf', 'NPT', 10, 300)

gomc_control.print_required_input(description=True)


# Display the optional ensemble input variables (input_variables_dict variables) for the GOMC control file writer via the print_valid_ensemble_input_variables function  [1, 2, 13-17].

# The NPT ensemble is used for the example below.

#  Note: Most input_variables_dict keys are the same as the GOMC Manual commands or may have "_box_0" or "_box_1" added at the end of the GOMC Manual naming convention  [1, 2].

# Example -> gomc_control.write_gomc_control_file(charmm, 'in_NPT.conf', 'NPT', 10, 300,
#                                                 input_variables_dict={"Pressure": 10,
#                                                                       "DisFreq": 0.20,
#                                                                       "RotFreq": 0.20,
#                                                                       "IntraSwapFreq": 0.20,
#                                                                       "RegrowthFreq": 0.20,
#                                                                       "CrankShaftFreq": 0.20,
#                                                                       }
#                                                )

gomc_control.print_valid_ensemble_input_variables('NPT', description=True)


# Alternatively, we can display both the required and optional ensemble input variables for the GOMC control file writer via the help function  [1, 2, 13-17].

# However, this method does not report the ensemble-specific functions.  The user will have to read each variable to acquire this information.

help(gomc_control.write_gomc_control_file)