# pyCEDFS

A very WIP python module to allow reading and import of Ced File System (CFS) electrophysiology files generated by 
the signal software suite: http://ced.co.uk/products/sigovin.
Leverages the CFS c library provided by CED to read data.

Currently supports opening the file and reading metadata, and data 
Currently only functions on 64-bit installations of windows. 

## Install  
``` 
pip install git+https://github.com/smestern/pyCEDFS.git
```
## Example Usage
```python
import pyCEDFS

cfsfile = pyCEDFS.CFS('debug.cfs') #Loads the file 
sweep1 = cfsfile.dataY[channel][sweepnumber,:] #data is loaded into dataY and dataX attributes.
y_units cfsfile.chVars[channel]['units'] #Other variables can be fetched from var dictionaries
```

## Conversion to NWB
Conversion to NWB is currently supported. Although requires some set up.





## Acknowledgements
