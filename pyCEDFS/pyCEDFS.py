
import os
import sys
import glob
import time
import datetime
import numpy as np
from pathlib import PureWindowsPath
import hashlib
import ctypes
import matplotlib.pyplot as plt
# Load the shared library into c types.
libc = ctypes.CDLL(".//lib//CFS64c.dll")
import logging
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

dataVarTypes = [('INT1', ctypes.c_int), ('WRD1', ctypes.c_ushort),('INT2', ctypes.c_int16),('WRD2', ctypes.c_short),('INT4', ctypes.c_int32), ('RL4', ctypes.c_longdouble), ('RL8', ctypes.c_longdouble), ( 'LSTR', ctypes.create_string_buffer)]
#define INT1    0                            
#define WRD1    1
#define INT2    2
#define WRD2    3
#define INT4    4
#define RL4     5
#define RL8     6
#define LSTR    7

class CFS(object):
    """
    
    """

    def __init__(self, CFSFilePath):

        #self._preLoadData = loadData
        

        self.CFSFilePath = os.path.abspath(CFSFilePath)
        self.CFSFolderPath = os.path.dirname(self.CFSFilePath)


        if not os.path.exists(self.CFSFilePath):
            raise ValueError("CFS file does not exist: %s" % self.CFSFilePath)
        self.CFSID = os.path.splitext(os.path.basename(self.CFSFilePath))[0]
        log.debug(self.__repr__())

        # create more local variables based on the header data
        #self._makeAdditionalVariables()
        open = libc.OpenCFSFile
        open.restype = ctypes.c_short
        # note the file size
        C_file = ctypes.create_string_buffer(self.CFSFilePath.encode())
        handle = open(C_file, 0, 0)
        

        ## Load the File properties and pass them to class
        self._filehandle = handle
        _filedate = ctypes.create_string_buffer(10)  
        _filetime = ctypes.create_string_buffer(10)  
        _comment = ctypes.create_string_buffer(100)
        libc.GetGenInfo(handle, _filedate, _filetime, _comment)
        self.fileDate = _filedate.value.decode()
        self.fileTime = _filetime.value.decode()
        self.fileComment = _comment.value.decode()   
        _channels = ctypes.c_short(14)
        _dsvars = ctypes.c_short(14)
        _fvars = ctypes.c_short(14)
        _ds = ctypes.c_ushort(14)
        test = libc.GetFileInfo(handle, ctypes.byref(_channels),ctypes.byref(_dsvars), ctypes.byref(_fvars), ctypes.byref(_ds))
        print (_channels.value)
        self.channels = _channels.value
        self.datasetVars = _dsvars.value
        self.fileVars = _fvars.value
        ### Populate the Vars list
        files_vars = []
        
        #Create our ctypes to avoid memory hog
        _size = ctypes.c_short()
        _type = ctypes.c_short()
        _units = ctypes.create_string_buffer(20)  
        _desc = ctypes.create_string_buffer(50) 
        ###Populate file Vars
        for x in np.arange(_fvars.value):
            libc.GetVarDesc(handle, ctypes.c_short(x), ctypes.c_short(0), ctypes.byref(_size), ctypes.byref(_type), _units, _desc)
            if _type.value != 7:
                _var = dataVarTypes[_type.value][1](99)
                _datas = ctypes.c_short()
                code = libc.GetVarVal(handle, ctypes.c_short(x), ctypes.c_short(0),ctypes.byref(_datas),ctypes.byref( _var))
                var_val = _var.value
            else:
                _var = dataVarTypes[_type.value][1](_size.value)
                _datas = ctypes.c_short()
                code = libc.GetVarVal(handle, ctypes.c_short(x), ctypes.c_short(0),ctypes.byref(_datas),_var)
                var_val = _var.value.decode()
            dict = {"desc":_desc.value.decode(), "size": _size.value, "units": _units.value.decode(), "type":dataVarTypes[_type.value][0], "value": var_val}
            files_vars.append(dict)
        self.file_vars = files_vars
        ##Populate the DS Vars
        ds_vars = []
        for d in np.arange(_ds.value):
            temp_ds_vars = []
            for x in np.arange(_dsvars.value):
                _datas = ctypes.c_short(d)
                libc.GetVarDesc(handle, ctypes.c_short(x), ctypes.c_short(1), ctypes.byref(_size), ctypes.byref(_type), _units, _desc)
                if _type.value != 7:
                    _var = dataVarTypes[_type.value][1]()
                    code = libc.GetVarVal(handle, ctypes.c_short(x), ctypes.c_short(1),ctypes.byref(_datas),ctypes.byref( _var))
                    var_val = _var.value
                else:
                    _var = dataVarTypes[_type.value][1](_size.value)
                    code = libc.GetVarVal(handle, ctypes.c_short(x), ctypes.c_short(1),ctypes.byref(_datas),_var)        
                    var_val = _var.value.decode()
                dict = {"desc":_desc.value.decode(), "size": _size.value, "units": _units.value.decode(), "type":dataVarTypes[_type.value][0], "value": var_val}
           
                temp_ds_vars.append(dict)
            ds_vars.append(temp_ds_vars)
        self.ds_vars = ds_vars
        ### Populate Channel vars
        ch_vars = []
        _channame = ctypes.create_string_buffer(21) 
        _xunits = ctypes.create_string_buffer(20) 
        _yunits = ctypes.create_string_buffer(20)
        _kind = ctypes.c_short()
        _type = ctypes.c_short()
        _spacing = ctypes.c_short()
        _other = ctypes.c_short()
        for ch in np.arange(_channels.value):
            _ch = ctypes.c_short(ch)
            libc.GetFileChan(handle, _ch, _channame, _xunits, _yunits, ctypes.byref(_type), ctypes.byref(_kind), ctypes.byref(_spacing), ctypes.byref(_other))
            dict = {'Channel': ch, 'Channel Name': _channame.value.decode(), 'X Units': _xunits.value.decode(), 'Y Units': _yunits.value.decode(), 'Type': dataVarTypes[_type.value][0], 'Kind': _kind.value, 'Spacing': _spacing.value, 'Other': _other.value}
            ch_vars.append(dict)
        dsch_vars = []
        _start = ctypes.c_long()
        _points = ctypes.c_long()
        _yscale = ctypes.c_float()
        _yoffset = ctypes.c_float()
        _xscale = ctypes.c_float()
        _xoffset = ctypes.c_float()
        for ch in np.arange(_channels.value):
            ds_dict = []
            for x in np.arange(1, _dsvars.value):
                libc.GetDSChan(handle, 
                               ctypes.c_short(ch), ##Channel
                               ctypes.c_ushort(x),
                               ctypes.byref(_start),
                               ctypes.byref(_points),
                               ctypes.byref(_yscale),
                               ctypes.byref(_yoffset),
                               ctypes.byref(_xscale),
                               ctypes.byref(_xoffset),
                                 )
                dict = {'Channel': ch, 'ch start': _start.value, 'points': _points.value, 'yscale': _yscale.value, 'yoffset': _yoffset.value, 'xscale': _xscale.value, 'xoffset': _xoffset.value}
                ds_dict.append(dict)
            dsch_vars.append(ds_dict)

        ##try to read data
        dataX = []
        dataY = []
        chanData = libc.GetChanData
        chanData.argtypes = (ctypes.c_short,ctypes.c_short,ctypes.c_ushort,ctypes.c_long,ctypes.c_short, ctypes.POINTER(ctypes.c_int16), ctypes.c_long)
        for ch in np.arange(0, _channels.value):
            ch_x =[]
            ch_y = []
            for x in np.arange(1, _dsvars.value-1):
                channel_p = dsch_vars[ch][x]['points'] * 2
                _dataarray = (ctypes.c_int16 * channel_p)()

                pointsRead = chanData(handle, 
                          ctypes.c_short(ch), ##Channel
                                 ctypes.c_ushort(x), ##DS
                                 ctypes.c_long(0), ##first element
                                 ctypes.c_short(0), 
                                _dataarray, 
                                 ctypes.c_long(channel_p * 16))
                data = np.ctypeslib.as_array(_dataarray)
                ds_y = data[:int(channel_p/2)]
                ds_x = data[int(channel_p/2):]
                
                yscale = dsch_vars[ch][x]['yscale']
                yoffset = dsch_vars[ch][x]['yoffset']
                xscale = dsch_vars[ch][x]['xscale']
                xoffset = dsch_vars[ch][x]['xoffset']
                ds_y = ds_y * yscale + yoffset
                #ds_x = ds_x * xscale
                ds_x = np.cumsum(np.hstack((xoffset,np.full(int(channel_p/2)-1,xscale))))
                if pointsRead > 0:
                    plt.plot(ds_x, ds_y)

                    ch_x.append(ds_x)
               
                    ch_y.append(ds_y)
            ch_x = np.vstack(ch_x)
            ch_y = np.vstack(ch_y)
            dataX.append(ch_x)
            dataY.append(ch_y)
        print(handle)
        plt.show()
        


def main():
    test = CFS('debug.cfs')
    return





if __name__ == "__main__":
    main()
