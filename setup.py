import numpy as np


class Stratification:
    def __init__(self, grid, materialSet):
        self.numberOfLayers = len(materialSet.groundList)

        self.layers = list()
        for ndx in range(self.numberOfLayers):
            self.layers.append(Layer(grid, materialSet, ndx))

class Layer:
    def __init__(self, grid, materialSet, number):
        self.__number = number

        self.__capacity = np.empty(grid.dim)
        self.__conductivity = np.empty(grid.dim-1)

        self.__capacity[0] = materialSet.fluid.capacity * np.pi * grid.x2[0] * grid.x2[0]
        self.__capacity[1] = materialSet.filling.capacity * np.pi * (grid.x2[1] * grid.x2[1] - grid.x2[0] * grid.x2[0])
        self.__capacity[2:-1] = materialSet.groundList[number].capacity * np.pi * (np.roll(grid.x2, -1)[1:-1] * np.roll(grid.x2, -1)[1:-1] - grid.x2[1:-1] * grid.x2[1:-1]   )
        self.__capacity[-1] = materialSet.groundList[number].capacity * np.pi * (grid.x[-1] * grid.x[-1] - grid.x2[-1] * grid.x2[-1])

        # fluid resistance neglected
        self.__conductivity[0] = 2 * np.pi * materialSet.filling.conductivity / np.log(grid.x[1] / grid.x2[0])
        self.__conductivity[1] = 2 * np.pi * materialSet.filling.conductivity / np.log(grid.x2[1] / grid.x[1])
        self.__conductivity[1] += 2 * np.pi * materialSet.groundList[number].conductivity / np.log(grid.x[2] / grid.x2[1]) 
        self.__conductivity[2:] = 2 * np.pi * materialSet.groundList[number].conductivity / np.log(grid.x[3:] / np.roll(grid.x, 1)[3:]) 

    @property
    def number(self):
        return self.__number

    @property
    def capacity(self):
        return self.__capacity
    
    @property
    def conductivity(self):
        return self.__conductivity

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value
 
    @conductivity.setter
    def conductivity(self, value):
        self.__conductivity = value

