"""Initialize signac statepoints."""

import os
import numpy as np
import signac
import unyt as u

# *******************************************
# the main user varying state points (start)
# *******************************************

#project=signac.init_project()
project=signac.get_project()

production_temperatures = [270, 250, 242, 240, 220, 200, 180] * u.K
#production_temperatures = [270] * u.K

# [0, 1, 2, 3, 4]
replicas = [0,1,2,3,4]

# *******************************************
# the main user varying state points (end)
# *******************************************


print("os.getcwd() = " +str(os.getcwd()))

pr_root = os.getcwd()
pr = signac.get_project(pr_root)

# filter the list of dictionaries
total_statepoints = list()

for prod_temp_i in production_temperatures:
    for replica_i in replicas:
        statepoint = {
            "production_temperature_K": np.round(prod_temp_i.to_value("K"), ).item(),
            "replica_number_int": replica_i,
        }
        total_statepoints.append(statepoint)

for sp in total_statepoints:
    pr.open_job(
        statepoint=sp,
    ).init()
