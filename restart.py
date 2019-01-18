'''
Created on 2018

@author: programmer
'''
import ctypes

'''tsclibrary = ctypes.WinDLL("c:\\64\\TSCLIB.dll");'''
tsclibrary = ctypes.WinDLL(".//libs//TSCLIB.dll");

# if __name__ == '__main__':
    # pass

restart = chr(27) + '!R'

'''
tsclibrary.about();
'''
tsclibrary.openportW("USB");
tsclibrary.sendcommandW(restart);
tsclibrary.closeport();




