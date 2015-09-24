from astropy.io import fits
from astropy.io import ascii
import numpy as np


files = ascii.read('NIRC2_sci_20020_1.txt')
files = np.array(files['fileNames'])

f = open('starPositions.txt','w')
f.write('file\tx\ty\n')
xg, yg = 611, 471

def findStar(im, (xg, yg)):
    return (xg, yg)

for i in files:
    im = fits.getdata('calfits/'+i[:-5]+'_drp.fits')
    x, y = findStar(im, (xg, yg))
    f.write(i[12:-5]+'\t'+str(x)+"\t"+str(y)+'\n')

f.close()


