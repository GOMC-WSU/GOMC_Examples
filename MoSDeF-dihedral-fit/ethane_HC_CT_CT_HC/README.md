# MoSDeF-dihedral-fit: Ethane OPLS-AA HC-CT-CT-HC dihedral fit example
This HC-CT-CT-HC dihedral example shows how many of the same dihedral types are fit at the same time. 
In this case, nine (9) dihedrals are fit simultaneously, only allowing the n=3 term in cos(n*phi) to fit because the other terms are invalid due to the molecule's symmetry.  

The MoSDeF-dihedral-fit package is located [here](https://github.com/GOMC-WSU/MoSDeF-dihedral-fit)


## run the file below after installing the ``MoSDeF-dihedral-fit`` package, using the ``mosdef_dihedral_fit`` enviornment

`conda activate mosdef_dihedral_fit`

`cd fit_dihedral`

`python example_dihedral_fit_ethane_CT_HC_HC_CT.py`