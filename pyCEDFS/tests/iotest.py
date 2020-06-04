import pyCEDFS
import matplotlib.pyplot as plt



def main():
    test = pyCEDFS.CFS('debug.cfs')
    test._debug_plot()
    plt.show()
    return





if __name__ == "__main__":
    main()
