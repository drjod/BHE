import numpy as np


class Memory:
    def __init__(self, numberOfLayers):
        self.__times = np.zeros(2000)
        self.__current_step = 0
        self.__fluxesList = list()
        for i in range(numberOfLayers):
            self.__fluxesList.append(np.zeros(20))

        self.__current_fluid_temperatureList = np.zeros(numberOfLayers+1)

    @property
    def current_step(self):
        return self.__current_step

    @property
    def times(self):
        return self.__times

    @property
    def fluxesList(self):
        return self.__fluxesList

    @property
    def current_fluid_temperatureList(self):
        return self.__current_fluid_temperatureList

    @current_fluid_temperatureList.setter
    def current_fluid_temperatureList(self, valueList):
        self.__current_fluid_temperatureList = valueList

    def set_current_time(self, time):
        self.__current_step += 1
        self.__times[self.__current_step] = time

    def set_current_fluxesList(self, fluxesList):
        for ndx, flux in enumerate(fluxesList):
            self.__fluxesList[ndx][self.__current_step] = flux

    def get_current_flux(self, layerNumber):
        return self.__fluxesList[layerNumber][self.__current_step]

    def get_current_time(self):
        return self.__times[self.__current_step]


