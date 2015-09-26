import numpy as np
from scipy.ndimage import interpolation as intp
from astropy.io import fits
from astropy.io import ascii
import sys


files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

positions = ascii.read('starPositions.txt')
xref, yref = 512., 512.

ROXs42B = np.array([])
ROXs42Br = np.array([])
ROXs12 = np.array([])
ROXs12r = np.array([])
n = np.size(targets)
for i in range(n):
    
    im = fits.getdata('calfits/'+fileNames[i])
    sim = intp.shift(im,[yref-positions['y'][i],xref-positions['x'][i]])
    fits.writeto('results/'+filenames[i][:-5]+'.reg.fits'
    hdr = fits.getheader('calfits/'+fileNames[i])
    PA = hdr['PARANG']+hdr['ROTPPOSN']-hdr['EL']-hdr['INSTANGL']
    rim = intp.rotate(sim,-PA,reshape=False)
    if targets[i]==1:
        if ROXs42B.sum()==0:
            ROXs42B=np.array([sim])
            ROXs42Br=np.array([rim])
        else:
            ROXs42B = np.append(ROXs42B,[sim],axis=0)
            ROXs42Br = np.append(ROXs42Br,[rim],axis=0)
    if targets[i]==2:
        if ROXs12.sum()==0:
            ROXs12=np.array([sim])
            ROXs12r=np.array([rim])
        else:
            ROXs12 = np.append(ROXs12,[sim],axis=0)
            ROXs12r = np.append(ROXs12r,[rim],axis=0)

    percent = float(i) / n
    hashes = '#' * int(round(percent * 20))
    spaces = ' ' * (20 - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()


sum42B = np.sum(ROXs42B,axis=0)
fits.writeto('results/ROXs42Bsum.fits',sum42B)
sum12 = np.sum(ROXs12,axis=0)
fits.writeto('results/ROXs12sum.fits',sum12)

med42B = np.median(ROXs42B,axis=0)
fits.writeto('results/ROXs42Bmed.fits',med42B)
med12 = np.median(ROXs12,axis=0)
fits.writeto('results/ROXs12med.fits',med12)

sum42Br = np.sum(ROXs42Br,axis=0)
fits.writeto('results/ROXs42Brotsum.fits',sum42Br)
sum12r = np.sum(ROXs12r,axis=0)
fits.writeto('results/ROXs12rotsum.fits',sum12r)

med42Br = np.median(ROXs42Br,axis=0)
fits.writeto('results/ROXs42Brotmed.fits',med42Br)
med12r = np.median(ROXs12r,axis=0)
fits.writeto('results/ROXs12rotmed.fits',med12r)
