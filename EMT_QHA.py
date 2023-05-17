## Workflow for one-key to calculate thermal expansion by QHA 
##Modify some code to match your requirement.

#Build primitive cell(unit cell) in diffenet LC
from ase.io import read,write
import sys, os
from ase.calculators.emt import EMT
from pathlib import Path
from ase.lattice.cubic import FaceCenteredCubic
from ase.build import bulk
import numpy as np
import copy
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
import yaml

metal='Pt'
file_path = "FORCE_SETS"
dataEV=[]
LatticeConstant=np.arange(3.89,3.96,0.01)## Lattice constant range
for k,LC in enumerate(LatticeConstant):
    ##If you want to build the conventinal cell use the code below:
    #atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    #      symbol='Pt',
    #      size=(1, 1, 1),
    #      pbc=True,latticeconstant=LC)
    atoms = bulk(metal, 'fcc', a=LC) #primitive cell of Pt
    atoms.write('POSCAR')
    os.system("phonopy -d --dim='3 3 3'")##generate displacements and super cell
    #write a loop here if you have more than 1 displacement
    atoms2=read('POSCAR-001')##
    #Set the calulater and get forces
    atoms2.calc = EMT() # you can attach to any calculator
    my_force_array = atoms2.get_forces()
    # Load the YAML data from the file
    with open('phonopy_disp.yaml', 'r') as file:
        data = yaml.safe_load(file)
    # Extract the displacement array and atom value
    displacement_array = data['displacements'][0]['displacement']
    atom = data['displacements'][0]['atom']
    with open(file_path, 'w') as file:
        # Iterate over each row in the array
        file.write(str(len(atoms2)) +'\n')
        file.write(str(len(atoms)) +'\n\n')
        #Write out the displacement 
        file.write(str(atom) +'\n')
        formatted_row = '  '.join('{:18.10f}'.format(d) for d in displacement_array)
        file.write(' ' + formatted_row + '\n')
        for row in my_force_array:
            # Convert each value in the row to the desired format and write to the file
            formatted_row = '  '.join(f"{value:20.16f}" for value in row)
            file.write(' ' + formatted_row + '\n')
    n='%02d' %k
    print(n)
    os.system("phonopy -t -p -s --tmax=2000 --dim='3 3 3' --mp='64 64 64'")#write the parameter of the thermal properties
    os.system('cp thermal_properties.yaml thermal_properties.yaml-'+n)
    dataEV.append([atoms2.get_volume(),atoms2.get_potential_energy()])##collect the E-V data
    
    
##Write E V data
filename = 'e-v.dat'
with open(filename, 'w') as file:
    file.write('#   cell volume        energy of cell other than phonon \n')
    for row in dataEV:
        line = '{:18.8f}  {:18.8f}\n'.format(row[0], row[1])
        file.write(line)

os.system("phonopy-qha -p -s --tmax=2000 e-v.dat thermal_properties.yaml-{00..06}")##Run QHA
