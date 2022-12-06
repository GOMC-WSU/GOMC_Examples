#init.py
#initialized data space for free energy calculations

import signac
import numpy as np
project=signac.init_project('C2A-NVT')
#pressure is in bar
density = ['0.0371','0.08618','0.12966','0.1958','0.2723','0.2964','0.3076','0.3164','0.3337']
temperature=['316']
for d in density:
    for t in temperature:
        sp={'Density':d,'Temperature':t}
        job=project.open_job(sp)
        job.init()
