
import os
os.chdir("pyCEDFS")
import sys
sys.path.append("")
print(os.getcwd())
import CFSConverter
import pyCEDFS

def main():
    con = CFSConverter.CFSConverter('C:\\Users\\SMest\\Documents\\Signal Demo\\Data\\Actions.cfs', "test.nwb")
    con = CFSConverter.CFSConverter('C:\\Users\\SMest\\Documents\\Signal Demo\\Data\\', "test2.nwb", globalSettingsFile='template.json')
    return


if __name__ == "__main__":
    main()