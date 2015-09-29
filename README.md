# PlanetaryHW1
A git repo for Planetary Astrophysics HW2

To generate the pdf's run:
```bash
source exeCode.sh
```
This script will create a directory called `results/` and run all the code for the homework.

NOTE: I manually went through each image and tagged it as an allignment image, ROXs42B or ROXs12; this corresponds to the target column in the text file `NIRC2_sci_20020_1.txt` (0, 1, or 2 respectively) which also contains a list of all the file names. 

Part 1: data is in `calfits/`.

Part 2: this code is contained in the `findStar` method in `imageSubs.py` and is executed in `findStars.py`. This code outputs the text file `starPositions.txt` which contains the name of each file and the position of the star (x, y).

Part 3 and 4: this code is contained in the `register` method in `imageSubs.py` and executed in `psf.py`. This method shifts and rotates the images as well as creating sum and median images of the result. All furthur code uses the 'registered' images such that the location of the star is in the center of the image (512, 512).

Part 5: this code is contained and executed in `averings.py`.

Part 6: this code is contained and executed in `adi.py`.

Part 7: this code is contained and executed in `bdi.py` and outputs the text file `bestFitPSF.txt` which contains the name of the best fit psf for each image.

Part 8: this code is contained and executed in `findObjects.py` and outputs the text file `objectPositions.txt` which contains the locations of each object as well as the relative astrometry (r, PA).
