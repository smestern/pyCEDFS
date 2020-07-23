import pyCEDFS
import matplotlib.pyplot as plt



def main():
    test = pyCEDFS.CFS('C:\\Users\\SMest\\Documents\\Signal Demo\\Data\\Actions.cfs')
    #test = pyCEDFS.CFS('debug.cfs')
    test._debug_plot()
    plt.legend()
    plt.show()
    return





if __name__ == "__main__":
    main()
