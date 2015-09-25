from astropy.io import fits
from astropy.io import ascii
import numpy as np


files = ascii.read('NIRC2_sci_20020_1.txt')
files = np.array(files['fileNames'])

f = open('starPositions.txt','w')
f.write('file\tx\ty\n')

def findStar(im, (xg, yg)):
    x, y, tf = 0, 0, 0
    for i in range(xg-5,xg+6):
        for j in range(yg-5,yg+6):
            if (np.sqrt((i-xg)**2+(j-yg)**2)<=5):
                f = im[i,j]
                tf += f
                x += f*i
                y += f*j

    x = x/tf
    y = y/tf
    return (x, y)

xg, yg = 611, 471
for i in files:
    im = fits.getdata('calfits/'+i[:-5]+'_drp.fits')
    x, y = findStar(im, (xg, yg))
    f.write(i[12:-5]+'\t'+str(x)+"\t"+str(y)+'\n')

f.close()
