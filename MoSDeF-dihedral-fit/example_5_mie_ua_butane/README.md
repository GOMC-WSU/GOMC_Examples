# MoSDeF-dihedral-fit: Butane Mie-UA _CH3-_CH2-_CH2-_CH3 dihedral fit example
This Mie United Atom (UA) dihedral (_CH3-_CH2-_CH2-_CH3 or CH3-CH2-CH2-CH3) is fit using the QM All-Atom (AA) data set. 
This is done by zeroing out all the non-contribuing atoms (hydrogens) in the forcefield (FF) XML file.. 
Since the Carbon atoms are the UA/bead centers (_CH3 and _CH2 or CH3 and CH2), they will be the only contributing forces in the FF XML file.

The MoSDeF-dihedral-fit package is located [here](https://github.com/GOMC-WSU/MoSDeF-dihedral-fit)


## run the file below after installing the ``MoSDeF-dihedral-fit`` package, using the ``mosdef_dihedral_fit`` enviornment

`conda activate mosdef_dihedral_fit`

`cd fit_dihedral`

`python example_dihedral_fit_butane_CT_CT_CT_CT.py`