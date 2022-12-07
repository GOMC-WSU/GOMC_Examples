#init.py
#initialized data space for free energy calculations

import signac
import numpy as np
project=signac.init_project('C2A-NPT')
#pressure is in bar
pressure=['26.491','46.083','54.2', '59.358','66.61','71.729','78.532','81.986','93.878']
temperature=['316']
for p in pressure:
    for t in temperature:
        sp={'Pressure':p,'Temperature':t}
        job=project.open_job(sp)
        job.init()
