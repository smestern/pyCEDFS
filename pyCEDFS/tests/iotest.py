import pyCEDFS
import matplotlib.pyplot as plt
import glob


def main():
    cfs_files = glob.glob('C:\\Users\\SMest\\Documents\\Signal Demo\\Data\\*.cfs')
    for i, fp in enumerate(cfs_files):
        test = pyCEDFS.CFS(fp)
        test._debug_plot(fignum=i)
        plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    main()
