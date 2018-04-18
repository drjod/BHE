import numpy as np


class Grid:
    def __init__(self, dim):
        self.__dim = dim

        self.__x  = np.empty(dim)
        self.__x2 = np.empty(dim-1)
            
        self.__dx  = np.empty(dim)
        self.__dx2  = np.empty(dim-1)

    @property
    def dim(self):
        return self.__dim

    @property            
    def x(self):
        return self.__x
 
    @property            
    def x2(self):
        return self.__x2
    
    @property 
    def dx(self):
        return self.__dx

    @property 
    def dx2(self):
        return self.__dx2


    def setUp(self, geo):

        self.__x[0] = 0.
        self.__x[1] = 2 * geo.radius_pipe
        self.__x[2] = geo.radius_borehole
        
        # grid gets coarser with distance from borehole
        l =  np.array(range(1, self.__dim-2))
        s = np.sum(l)
        for i in range(l.size+1):
            self.__x[2+i] = geo.radius_borehole + (geo.radius_BHE - geo.radius_borehole) * np.sum(l[:i]/s)

        self.__x2 = (np.roll(self.__x, -1)[:-1] + self.__x[:-1]) / 2

        self.__dx[0] = np.nan
        self.__dx[self.__dim-1] = np.nan
        for i in range(1, self.__dim-1):
            self.__dx[i] = 0.5 * (self.__x[i+1] - self.__x[i-1])
            
        for i in range(0, self.__dim-1):
            self.__dx2[i] = self.__x[i+1] - self.__x[i]
        
        self.__dx[1:-1] = (np.roll(self.__x, -1)[1:-1] - np.roll(self.__x, 1)[1:-1]) / 2
        self.__dx2 = np.roll(self.__x, -1)[:-1] - self.__x[:-1]
       
        # print(self.__x)
        # print(self.__x2)
        # print(self.__dx)
        # print(self.__dx2)


    def setUp_equidistant(self, length):

        for i in range(self.__dim):
            self.__x[i] = i * length / (self.__dim-1)
            
        self.__x2 = np.empty(self.__dim-1)
        for i in range(self.__dim-1):
            self.__x2[i] = i + 0.5

        self.__dx[0] = np.nan
        self.__dx[self.__dim-1] = np.nan
        
        for i in range(1, self.__dim-1):
            self.__dx[i] = 0.5 * (self.__x[i+1] - self.__x[i-1])
            
        for i in range(0, self.__dim-1):
            self.__dx2[i] = self.__x[i+1] - self.__x[i]
        
        # print("x: {}".format(self.__x))
        # print(self.__x2)
        # print(self.__dx)
        # print("dx2: {}".format(self.__dx2))
