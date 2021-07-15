# ### Generates trajectories and saves file
# import numpy as np
# from ase import Atoms
# from ase.calculators.emt import EMT
# from ase.io import read
# from ase.units import kJ
# from ase.eos import EquationOfState
# from ase.build import bulk, mx2
# from ase.io import Trajectory
# from ase.db import connect
# from ase.visualize import view
# import Flask
# """Simple molecular dynamics.
#
# A block of 27 cubic unit cells of Cu is set up, a single atom is given
# a significant momentum, and constant energy molecular dynamics is
# performed.
#
# """
#
# from numpy import *
# from asap3 import Atoms, EMT, units
# from ase.lattice.cubic import FaceCenteredCubic
# from asap3.md.verlet import VelocityVerlet
#
# # Create the atoms
# atoms = FaceCenteredCubic(size=(3,3,3), symbol="Cu", pbc=False)
#
# # Give the first atom a non-zero momentum
# atoms[0].momentum = array([0, -11.3, 0])
# print("Kinetic energies of all atoms:")
# p = atoms.get_momenta()
# kinenergies = 0.5 * (p * p).sum(1) / atoms.get_masses()
# print(kinenergies)
#
# # Associate the EMT potential with the atoms
# atoms.set_calculator(EMT())
#
# # Now do molecular dynamics, printing kinetic, potential and total
# # energy every ten timesteps.
# dyn = VelocityVerlet(atoms, 5.0*units.fs)
# print("")
# print("Energy per atom:")
# print("  %15s %15s %15s" % ("Pot. energy", "Kin. energy", "Total energy"))
#
# for i in range(25):
#     dyn.run(10)
#     epot = atoms.get_potential_energy()/len(atoms)
#     ekin = atoms.get_kinetic_energy()/len(atoms)
#     print("%15.5f %15.5f %15.5f" % (epot, ekin, epot+ekin))
#
# #
# '''
# a1 = bulk('Cu', 'fcc', a=3.6)
# view(a1)
#
# from gpaw import GPAW, PW
# calc = GPAW(mode=PW(600), kpts=(8, 8, 8),
#             setups={'Ag': '11'})
#
# calc.write('Ag.gpw')
#
# '''
# '''
# # a1 = bulk('Cu', 'fcc', a=3.6)
# # a2 = bulk('Cu', 'fcc', a=3.6, orthorhombic=True)
# # a3 = bulk('Cu', 'fcc', a=3.6, cubic=True)
# #
# a = mx2(formula = 'MoS2', kind = '2H', a = 3.18, thickness = 3.19, size = (1,1,1), vacuum = None)
# # a = bulk('MoS2', a=3.1596,b=3.1596,c=12.295)
# view(a)
# #
# # print(a1.cell)
# #
#
# import matplotlib.pyplot as plt
# from ase.visualize.plot import plot_atoms
# from ase.lattice.cubic import FaceCenteredCubic
# # slab = FaceCenteredCubic('Au', size=(2, 2, 2))
# # fig, ax = plt.subplots()
# # plot_atoms(slab, ax, radii=0.3, rotation=('90x,45y,0z'))
# # plt.show()
#
# # view(a1)
# # db1 = connect('GNR.db')
#
# from ase.build import bulk
# from ase.calculators.test import FreeElectrons
#
# # a = bulk('Cu')
# a.calc = FreeElectrons(nvalence=0,
#                        kpts={'path': 'GKMG', 'npoints': 200})
# a.get_potential_energy()
# bs = a.calc.band_structure()
# bs.plot(emin=0, emax=20, filename='moly.png')
# '''


from ase.build import molecule
from ase.build import bulk
from ase.visualize import view
from ase.build import graphene_nanoribbon


# gnr1 = graphene_nanoribbon(3, 4, type='armchair', saturated=True,
#                                vacuum=3.5)
# gnr2 = graphene_nanoribbon(2, 6, type='zigzag', saturated=True,
#                            C_H=1.1, C_C=1.4, vacuum=3.0,
#                            magnetic=True, initial_mag=1.12)


# view(gnr1)
# view(gnr2)

from ase.lattice import *
from ase import lattice
from ase.lattice.cubic import BodyCenteredCubic
from ase.lattice.hexagonal import Hexagonal
# print(lattice.attributes)
# print(dir(lattice))
print(lattice.HEX2D)
print(lattice.HEX)
# print(dir(lattice.HEX))
# atoms = BodyCenteredCubic('Si' ,directions=[[1,-1,0],[1,1,-1],[0,0,1]],
#                           miller=[None, None, [1,1,2]])

# moly = Hexagonal('Mo', latticeconstant = {'a':3.1596, 'c':12.295})
# view(moly)
from ase.lattice.hexagonal import HexagonalFactory
from ase.lattice.hexagonal import *
from ase.lattice.compounds import *

# gra = Graphene()
import inspect

# def get_class_that_defined_method(meth):
#     for cls in inspect.getmro(meth.im_class):
#         if meth.__name__ in cls.__dict__:
#             return cls
#     return None

# get_class_that_defined_method(HEX_Fe2O3)
# print(p)

class HexagonalMoS2Factory(HexagonalFactory):


    import ase.io as io
    # from ase import Atoms, Atom
    from ase.lattice.bravais import Bravais
    #
    index1=1
    index2=1
    index3=1
    # mya = 1
    # myb = 1
    # myc = 1
    mya = 3.1956
    myb = 3.1956
    myc = 12.295
    myalpha = 90
    mybeta = 90
    mygamma = 120
    gra = MoS2(symbol = ('Mo', 'S'),latticeconstant={'a':mya,'b':myb, 'c':myc,
    'alpha':myalpha,
    'beta':mybeta,
    'gamma':mygamma},size=(index1,index2,index3))
    # gra.symbol = ('Mo', 'S')
    # gra.latticeconstant={'a':mya,'b':myb, 'c':myc,
    # 'alpha':myalpha,
    # 'beta':mybeta,
    # 'gamma':mygamma}
    # gra.size=(index1,index2,index3)
    io.write('MoS2.xyz', gra, format='xyz')

    #
    # bravais_basis = [[1.580, 0.912, 1.514],
    #                  [0.000, 1.824, 3.074],
    #                  [1.580, 0.912, 4.634],
    #                  [0.000, 1.824, 7.661],
    #                  [1.580, 0.912, 9.221],
    #                  [0.000, 1.824, 10.781]]
    # bravais_basis = (np.array(bravais_basis).astype(float))/12.295
    # print(bravais_basis)
    # element_basis = (1, 0, 1, 1, 0, 1)


moly = HexagonalMoS2Factory()
import ase.io as io
from ase.build import mx2
# moly2 = mx2(formula='MoS2', kind='2H', a=3.18, thickness=3.19, size=(1, 1, 1), vacuum=None)
# view(moly2)


# view(moly)

# from ase.lattice.cubic import FaceCenteredCubicFactory
# class DiamondFactory(FaceCenteredCubicFactory):
#     """A factory for creating diamond lattices."""
#     xtal_name = 'diamond'
#     bravais_basis = [[0, 0, 0], [0.25, 0.25, 0.25]]

# Diamond = DiamondFactory()

# view(Diamond)
# view(HEX_Fe2O3)
# print(dir(HEX_Fe2O3))
#
# class NaClFactory(SimpleCubicFactory):
#     "A factory for creating NaCl (B1, Rocksalt) lattices."
#
#     bravais_basis = [[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0], [0, 0.5, 0.5],
#                      [0.5, 0, 0], [0.5, 0, 0.5], [0.5, 0.5, 0],
#                      [0.5, 0.5, 0.5]]
#     element_basis = (0, 1, 1, 0, 1, 0, 0, 1)
#
#
# # B1 = NaCl = Rocksalt = NaClFactory()



# view(B1)
