import numpy as np

class Matrix:
    # a = 0  # lower diagonal a[0] = 0
    # b = 0  # diagonal
    # c = 0  # upper diagonal c[dim-1] = 0
        
    def __init__(self, dim):
        self.__a = np.empty(dim)
        self.__b = np.empty(dim)
        self.__c = np.empty(dim-1)

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def c(self):
        return self.__c

    @a.setter
    def a(self, value):
        self.__a = value

    @b.setter
    def b(self, value):
        self.__b = value

    @c.setter
    def c(self, value):
        self.__c = value
