from astropy.io import fits
from astropy.io import ascii
import numpy as np
import imageSubs as iS

print 'finding stars'

#load file names
files = ascii.read('NIRC2_sci_20020_1.txt')
files = np.array(files['fileNames'])

#prepare output file
f = open('starPositions.txt','w')
f.write('file\tx\ty\n')

#initial guess for star positions
xg, yg = 611, 471
for i in files:
    #load image, find star, write out to file.
    im = fits.getdata('calfits/'+i)
    x, y = iS.findStar(im, (xg, yg),6)
    f.write(i[12:-5]+'\t'+str(x)+"\t"+str(y)+'\n')
    if (np.abs(np.abs(x-xg)-5)<0.05 or np.abs(np.abs(y-yg)-5)<0.05):
        print "##### Warning centroid is near bounding circle for "+i+"#####"

f.close()
