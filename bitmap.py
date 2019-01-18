import ctypes
from PIL import Image
import numpy as np

tsclibrary = ctypes.WinDLL(".//libs//TSCLIB.dll");

# Config
PWIDTH	= 62		# tag width, measured in mm
PHEIGHT = 20		# tag height
PGAP 	= 2			# gap between tags
DPI		= 200		# DPI of printer
SPEED	= 3			# printing speed
DENSITY = 15		# ink density
SENSOR	= 0			# type of sensor 0>gap 1>black mark
OFFSET  = 0			# GAP offset
DOT 	= DPI//100*4# Dots per mm
CONTRAST= 128		# A number between 0~255


def printPic(imName,x,y,mode):
	print("PRINTING ", imName)
	im = Image.open(imName)
	# im.thumbnail((PWIDTH*DOT//2,PHEIGHT*DOT))
	im.thumbnail((PWIDTH*DOT,PHEIGHT*DOT),Image.ANTIALIAS)
	width,height = im.size

	if width<248:	# report err for now, edit later
		print("FAILURE: IMAGE IS TOO SMALL\n")
		return -1

	im = im.convert("L") 
	data = im.getdata()
	data = np.matrix(data)
	data = data.tolist()[0]

	im1 = [1 for i in range(width*height)]
	for i in range(width*height):
		if data[i] < CONTRAST:
			im1[i] = 0
	bitmap = [0   for i in range(width*height//8)]	# sending 0 may cause some err
	offset = [255 for i in range(width*height//8)]	# so use offset to make it work
	for i in range(width*height//8):
		bitmap[i] = eval("0b"+str(im1[i*8:(i+1)*8]).replace(" ","").replace(",",'').replace("[",'').replace("]",''))
		if bitmap[i] == 0:
			bitmap[i] = 1
			offset[i] = 254
	# seeBitmap(bitmap)
	ini = "BITMAP "+str(x)+","+str(y)+","+str(width//8)+","+str(height)+","+str(mode)+","
	ini = ini.encode()
	bm = bytes(bitmap)
	ofs = bytes(offset)
	end = "\0".encode()
	tsclibrary.sendcommand(ini + bm + end);
	tsclibrary.sendcommand(ini + ofs + end);
	return 

def seeBitmap(bitmap):
	ss = ""
	for i in bitmap:
		if i == 1:
			ss += "00 "
		else:
			tt = str(hex(i))[2:].upper()
			if len(tt)==1:
				tt = "0"+tt
			ss+=tt+" "
	print(ss)


left = l = 0
right = r = 253
def printOnTop(imName,position):
	printPic(imName,position,0,1)



tsclibrary.openportW("USB");
# tsclibrary.setup(str(PWIDTH),str(PHEIGHT),str(SPEED),str(DENSITY),str(SENSOR),str(PGAP),str(OFFSET))
tsclibrary.sendcommandW("DENSITY "+str(DENSITY));
tsclibrary.sendcommandW("SIZE " + str(PWIDTH) +" mm, " + str(PHEIGHT) +" mm");
# tsclibrary.sendcommandW("GAP "+str(PGAP)+" mm, 0");
# tsclibrary.sendcommandW("DIRECTION 1");
# tsclibrary.sendcommandW("GAPDETECT ["+str(PHEIGHT*DOT)+","+str(PGAP*DOT)+"]");
# tsclibrary.sendcommandW("HOME");
tsclibrary.clearbuffer();
tsclibrary.sendcommandW("CLS");

printOnTop(".//image//testBitmap.bmp",left)
# printOnTop(".//image//im05.png",right)

tsclibrary.printlabelW("1","1");
tsclibrary.closeport();
	