import matplotlib.pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.axes_grid1 import host_subplot

from pylab import ion, figure, plot
import time

class Print:
    def execute(self, obj):
        for ndx, result in enumerate(obj.resultList):
            print("{}: {} ".format(ndx, result))

class Plot:
    def __init__(self):
        plt.ion()
        pass

    def execute(self, obj):
        for ndx, result in enumerate(obj.resultList):
            print("result: {}".format(result))
            ax = host_subplot(len(obj.resultList), 1, ndx+1)
            #plt.subplots_adjust(hspace=.5)
            ax.grid(b=True, which='major', color='k', linestyle='-')
            ax.set_ylim([-2, 2]) 
            ax.plot(obj.grid.x, result, color='r')
            if ndx == 0:
                ax.set_title("Time: {0:.2f} days".format(obj.memory.get_current_time()/86400))
            # + r" - Outlet Temperature [$^0C$] {0:.2f} ".format(obj.memory.current_fluid_temperatureList[len(obj.resultList)]))
            ax.text(0.01, 0, "Flux: {0:.2f} m/s".format(obj.memory.get_current_flux(ndx)), fontsize=12, color='b')
            if ndx == len(obj.resultList)-1:
                ax.set_xlabel("Radius [m]", fontsize=9)
            else:
                ax.tick_params(labelbottom='off')
            ax.set_ylabel(r"Temperature [$^0C$]", fontsize=9)

        #plt.draw()
        plt.show()
        plt.pause(0.1)
        plt.clf()
        time.sleep(1)

