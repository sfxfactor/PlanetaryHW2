from astropy.io import fits
from astropy.io import ascii
import numpy as np


files = ascii.read('NIRC2_sci_20020_1.txt')
files = np.array(files['fileNames'])

f = open('starPositions.txt','w')
f.write('file\tx\ty\n')

def findStar(im, (xg, yg)):
    x, y, tf = 0, 0, 0
    for i in range(-6,+7):
        for j in range(-6,7):
            if (np.sqrt((i)**2+(j)**2)<=6):
                f = im[xg+i,yg+j]
                tf += f
                x += f*i
                y += f*j

    x = x/tf
    y = y/tf
    return (x+xg, y+yg)

xg, yg = 611, 471
for i in files:
    im = fits.getdata('calfits/'+i)
    x, y = findStar(im, (xg, yg))
    f.write(i[12:-5]+'\t'+str(x)+"\t"+str(y)+'\n')
    if (np.abs(np.abs(x-xg)-5)<0.05 or np.abs(np.abs(y-yg)-5)<0.05):
        print "##### Warning centroid is near bounding circle for "+i+"#####"

f.close()
