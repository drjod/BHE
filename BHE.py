from setup import Stratification, Layer
from output import Plot, Print
from grid import Grid
from equationSystem import EquationSystem
from memory import Memory
from fluid import Fluid

import numpy as np


class BHE:
    def __init__(self, geo, dim, dt, scheme, bc_centre, bc_fringe, materialSet, fluid_velocity):     
        self.__dt = dt
        grid = Grid(dim)
        grid.setUp(geo)

        self.__numberOfIterations = 10 if bc_fringe.flag_iteration_required else 1
        bc_centre.set_parameter(materialSet, geo.radius_pipe)
        bc_fringe.set_parameter(materialSet, geo.radius_BHE)

        self.__stratification = Stratification(grid, materialSet)
        self.__equationSystem = EquationSystem(grid, scheme, bc_centre, bc_fringe,
                                               self.__stratification.layers)
        self.__fluid_velocity = fluid_velocity

        self.__plot = Plot()

        self.__fluid = Fluid(materialSet.fluid, np.pi * geo.radius_pipe * geo.radius_pipe, self.__stratification.numberOfLayers+1)
        self.__numberOfSubTimeSteps = dt

    @property
    def dt(self):
        return self.__dt

    @property
    def dim(self):
        return self.__dim

    @property
    def m(self):
        return self.__m

    @property
    def r(self):
        return self.__r

    @property
    def memory(self):
        return self.__memory

    def step_forward(self, numberOfTimeSteps):
        for timeStep in range(numberOfTimeSteps):
            print("Time step {} of {}".format(timeStep, numberOfTimeSteps))
            self.__equationSystem.assemble_rightHandSide(timeStep, self.__dt)
            self.__equationSystem.set_boundary_centre()

            for j in range(self.__numberOfIterations):
                # print("     Iteration {} of {}".format(j, self.__numberOfIterations))
                self.__fluid.solve(self.__fluid_velocity, self.__equationSystem.memory)   
                self.__equationSystem.memory.current_fluid_temperatureList = self.__fluid.result

                self.__equationSystem.set_boundary_fringe()
                self.__equationSystem.solve()
                self.__equationSystem.calculate_fluxes()
                
            self.show_result(Print())
            self.show_result(self.__plot)

    def assemble_matrix(self):
        self.__equationSystem.assemble_matrix(self.__dt)

    def show_result(self, output):
        output.execute(self.__equationSystem)
