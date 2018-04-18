from grid import Grid
from memory import Memory

import numpy as np
from random import random


class Fluid:
    def __init__(self, fluid_material, area, dim):
        self.__result = np.zeros(dim)

        self.__fluid_material = fluid_material
        self.__factor = area * fluid_material.capacity

    @property
    def resultList(self):
        return [self.__result]

    @property
    def result(self):
        return self.__result

    def solve(self, velocity, memory):
        # layer thickness is 1 meter
        self.__result[0] = random() * 4 - 2
        for i in range(1, self.__result.size):
            self.__result[i] = self.__result[i-1] - memory.get_current_flux(i-1) / (self.__factor * velocity)
