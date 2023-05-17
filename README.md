# ASE-phonopy-Interface
This is the Interface between Atomic Simulation Environment(ASE) and phonopy. The forces calculation from ASE can be generated and ordered in the format of phonopy. And then passes through phonopy for further calculation.

In the example, we will use EMT potential to calculate the energy and forces and pass through phonopy package to calculate thermal expansion of Pt (QHA).

You will need to install the ASE and phonopy package first. 

Run the code block in ASE_phonopy_Example.ipynb and you will get the results.

The ensemble code in script EMT_QHA.py, so that you are able to run QHA in one script and run a lot of tests. 
