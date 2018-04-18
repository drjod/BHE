from solver import Solver
from memory import Memory

import numpy as np


class EquationSystem:
    def __init__(self, grid, scheme, bc_centre, bc_fringe, layers):
        self.__grid = grid
        self.__scheme = scheme
        self.__solver = Solver()

        self.__layers = layers

        self.__resultList = list()
        self.__matrixList = list()
        self.__rhsList = list()

        for i in range(len(layers)):
            self.__resultList.append(np.zeros(grid.dim))
            self.__matrixList.append(None)
            self.__rhsList.append(np.zeros(grid.dim))

        self.__memory = Memory(len(layers))

        self.__bc_centre = bc_centre
        self.__bc_fringe = bc_fringe

    @property
    def resultList(self):
        return self.__resultList

    @property
    def grid(self):
        return self.__grid

    @property
    def memory(self):
        return self.__memory

    def assemble_matrix(self, dt):
        for ndx, layer in enumerate(self.__layers):
            self.__matrixList[ndx] = self.__scheme.assemble_matrix(layer, self.__grid, dt)

    def assemble_rightHandSide(self, timeStep, dt):
        for ndx, layer in enumerate(self.__layers):
            self.__rhsList[ndx] = self.__scheme.assemble_rightHandSide(
                layer, self.__grid, dt, self.__rhsList[ndx], self.__resultList[ndx])

        self.__memory.set_current_time((timeStep+1) * dt)

    def set_boundary_centre(self):
        for ndx, layer in enumerate(self.__layers):
            self.__matrixList[ndx].c[0] = 0
            self.__matrixList[ndx].b[0] = 1.

            self.__rhsList[ndx][0] = self.__bc_centre.execute(layer, self.__memory)

    def set_boundary_fringe(self):
        for ndx, layer in enumerate(self.__layers):
            self.__matrixList[ndx].a[self.__grid.dim-1] = 0
            self.__matrixList[ndx].b[self.__grid.dim-1] = 1.

            self.__rhsList[ndx][self.__grid.dim-1] = self.__bc_fringe.execute(layer, self.__memory)

    def solve(self):
        for ndx, layer in enumerate(self.__layers):
            self.__resultList[ndx] = self.__solver.solve(self.__matrixList[ndx], self.__rhsList[ndx])

    def calculate_fluxes(self):
        fluxesList = list()
        for ndx, layer in enumerate(self.__layers):
            fluxesList.append( - layer.conductivity[0] * (
                                   self.__resultList[ndx][1] - self.__resultList[ndx][0]
                                   ) / self.__grid.dx2[0])

        self.__memory.set_current_fluxesList(fluxesList)

