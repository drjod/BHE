import numpy as np

class Solver:
    
    def __init__(self):
        self.__a = 0
        self.__beta = 0
        self.__gamma = 0
        
    
    def do_LU_decomposition(self, m):

        dim = m.b.size
        
        self.__a = m.a
        self.__beta = np.zeros(dim)
        self.__gamma = np.zeros(dim-1)  # last entry 0

        self.__beta[0] = m.b[0]
        self.__gamma[0] = m.c[0] / self.__beta[0]

        for i in range(1, dim-1):
            self.__beta[i] = m.b[i] - (m.a[i]*self.__gamma[i-1])
            self.__gamma[i] = m.c[i] / self.__beta[i]

        self.__beta[dim-1] = m.b[dim-1] - (m.a[dim-1]* self.__gamma[dim-2])
        
        # print(self.__beta)
        # print(self.__gamma)

    def solve_LU(self, r):
        
        dim = self.__beta.size
        # forward step
        z = np.zeros(dim)
        z[0] = r[0] / self.__beta[0]

        for i in range(1, dim):
            z[i] = (r[i] - self.__a[i] * z[i-1]) / self.__beta[i]

        # backward step        
        u = np.zeros(dim)
        
        u[dim-1] = z[dim-1]
        for i in reversed(range(0, dim-1)):
            u[i] = z[i] - self.__gamma[i] * u[i+1]
            
        return u
    
    def solve(self, m, r):
        self.do_LU_decomposition(m)
        return self.solve_LU(r)
