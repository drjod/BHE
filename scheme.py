from matrix import Matrix
import numpy as np


class CranckNicholson:
    __matrix = None

    def assemble_matrix(self, layer, grid, dt):
        self.__matrix = Matrix(grid.x.size)
        
        self.assemble_laplace(layer, grid, dt)
        self.assemble_capacity(layer)

        return self.__matrix

    def assemble_laplace(self, layer, grid, dt):
         conductivity = layer.conductivity

         self.__matrix.b[1:-1] = dt * (
                              conductivity[:-1] / grid.dx2[:-1] + conductivity[1:] / grid.dx2[1:]
                                   ) / ( 2 * grid.dx[1:-1] )

         self.__matrix.a[0] = np.nan
         self.__matrix.a[1:-1] = - dt * conductivity[:-1] / ( 2 * grid.dx2[:-1] * grid.dx[1:-1] )

         self.__matrix.c[1:] = - dt * conductivity[1:] / ( 2 * grid.dx2[1:] * grid.dx[1:-1] )

    def assemble_capacity(self, layer):
         self.__matrix.b[1:-1] += layer.capacity[1:-1]

    def assemble_rightHandSide(self, layer, grid, dt, rhs, result):
         factor = dt / (2 * grid.dx[1:-1])

         rhs[1:-1] = result[1:-1] * layer.capacity[1:-1]
         rhs[1:-1] += factor * layer.conductivity[1:] * (
                                    np.roll(result, -1)[1:-1] - result[1:-1]) / grid.dx2[1:]
         rhs[1:-1] -= factor * np.roll(layer.conductivity, 1)[1:] * (
                                    result[1:-1] - np.roll(result, 1)[1:-1]) / grid.dx2[:-1]

         return rhs

