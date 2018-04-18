from BHE import BHE
from output import Print, Plot
from scheme import CranckNicholson
from geometry import Geometry
from material import MaterialSet
from boundary import ConstantBoundary, RandomBoundary, FluidBoundary, ConeBoundary


def run_BHE():

    # boundary_centre = RandomBoundary(-2., 2.)
    # boundary_centre = ConstantBoundary(2.)
    boundary_centre = FluidBoundary()
    boundary_fringe = ConeBoundary()

    numberOfNodes = 20
    timeStepSize = 10000000
    numberOfTimesteps = 30
    numberOfLayers = 3

    BHE_inst = BHE(Geometry(), numberOfNodes, timeStepSize, 
                   CranckNicholson(),
                   boundary_centre, boundary_fringe, 
                   MaterialSet(numberOfLayers),
                   fluid_velocity=0.2
                  )

    BHE_inst.assemble_matrix()
    BHE_inst.step_forward(numberOfTimesteps)


if __name__ == '__main__':
    run_BHE()
