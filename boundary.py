import numpy as np
from random import random


class Boundary:
    def __init__(self, flag_iteration_required):
        self.__flag_iteration_required = flag_iteration_required

    @property
    def flag_iteration_required(self):
        return self.__flag_iteration_required
        
    def set_parameter(self, materialSet, radius):
        pass


class ConstantBoundary(Boundary):
    def __init__(self, value):
        Boundary.__init__(self, False)
        self.__value = value
        
    def execute(self, layer, memory):
        return self.__value    


class RandomBoundary(Boundary):
    def __init__(self, threshold_lower, threshold_upper):
        Boundary.__init__(self, False)
        self.__threshold_lower = threshold_lower
        self.__threshold_upper = threshold_upper

    def execute(self, layer, memory):
        return random() * (self.__threshold_upper - self.__threshold_lower) + self.__threshold_lower   


class FluidBoundary(Boundary):
    def __init__(self):
        Boundary.__init__(self, True)

    def execute(self, layer, memory):
        value = (memory.current_fluid_temperatureList[layer.number] + memory.current_fluid_temperatureList[layer.number+1]) / 2 
        # print(value)
        return value

class ConeBoundary(Boundary):
    def __init__(self):
        Boundary.__init__(self, True)

    def set_parameter(self, materialSet, radius):
        self.__radius = radius
        self.__materialSet = materialSet

    def execute(self, layer, memory):
        factor = self.__materialSet.groundList[layer.number].capacity * self.__radius * self.__radius / (
                                            4 * self.__materialSet.groundList[layer.number].conductivity)
        factor2 = 4 * np.pi * self.__materialSet.groundList[layer.number].conductivity 

        dT = 0
        for i in range(memory.current_step):
            Wu = self.calculate_Wu(factor / (memory.get_current_time() - memory.times[i]))

            Wu2 = self.calculate_Wu(factor / (memory.get_current_time() - memory.times[i+1])
                                   ) if i < memory.current_step-1 else 0

            dT += (Wu - Wu2) * memory.fluxesList[layer.number][i+1] / factor2

        return dT

    def calculate_Wu(self, u, accuracy=1.e-4, flag_print_u=False):
 
        if u >= 1:
            print("WARNING: 1 <= u = {}".format(u))
        if flag_print_u:
            print("u: {}".format(u))

        Wu, term, sign = -0.5772 - np.log(u), 1, 1

        for i in range(1, 1000):
            term *= u /(i * i)
            Wu += sign * term

            if term < accuracy:
                break

            sign -= sign

        return Wu

