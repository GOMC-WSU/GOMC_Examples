These workflows work with MoSDeF-GOMC cloned from https://github.com/GOMC-WSU/MoSDeF-GOMC
after 1/21/2026.

To use tabulated potentials, the XML files have to be modified.
The typical analytical expression must be replaced by:  AtomTypes expression="TABULATED" 

The python script "table_gen.py" can be used to turn an analytical two-body potential into a tabulated potential.
table_gen.py produces a tabulated potential file that GOMC can read.


