import numpy as np
from astropy.io import fits
from astropy.io import ascii
import sys
import imageSubs as iS
import glob

print 'finding objects'

#pixel scale of NIRC2 'narrow' from www2.keck.hawaii.edu/inst/nirc2/genspecs.html
s = 0.009942 #arcsec/pizel +/-0.00005

#grab all of the psf subtracted images
ROXs42B= glob.glob('results/*target1rotmed*')
ROXs12= glob.glob('results/*target2rotmed*')

#guess the positions of the objects
ob42 = [(554,470),(631,512)]
ob12 = [(486,690)]

#prepare output file
f = open('objectPositions.txt','w')
f.write('file\tx1\ty1\tx2\ty2\tr1\tPA1\tr2\tPA2\n')

for i in ROXs42B:
    im = fits.getdata(i)
    #find positions
    x1, y1 = iS.findStar(im, ob42[0], 6)
    x2, y2 = iS.findStar(im, ob42[1], 6)
    #translate to r/PA
    r1 = s*np.sqrt((x1-512.)**2+(y1-512.)**2)
    r2 = s*np.sqrt((x2-512.)**2+(y2-512.)**2)
    PA1 = np.degrees(np.arctan2(-(x1-512.),(y1-512.)))
    PA2 = np.degrees(np.arctan2(-(x2-512.),(y2-512.)))
    #output to file
    f.write(i+'\t'+str(x1)+'\t'+str(y1)+'\t'+str(x2)+'\t'+str(y2)+'\t'+str(r1)+'\t'+str(PA1)+'\t'+str(r2)+'\t'+str(PA2)+'\n')
for i in ROXs12:
    im = fits.getdata(i)
    x, y = iS.findStar(im, ob12[0], 6)
    r = s*np.sqrt((x-512.)**2+(y-512.)**2)
    PA = np.degrees(np.arctan2(-(x-512.),(y-512.)))
    f.write(i+'\t'+str(x)+'\t'+str(y)+'\t0\t0'+str(r)+'\t'+str(PA)+'\t0\t0\n')

f.close()

