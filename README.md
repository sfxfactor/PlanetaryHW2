# PlanetaryHW2
A git repo for Planetary Astrophysics HW2 (requires `numpy`, `scipy`, and `astropy`)

To generate the pdf's run:
```bash
source exeCode.sh
```
This script will create a directory called `results/` and run all the code for the homework.

#Notes
I manually went through each image and tagged it as an acquisition image, ROXs42B or ROXs12; this corresponds to the values (0, 1, or 2 respectively) in the 'target' column in the text file `NIRC2_sci_20020_1.txt` which also contains a list of all the file names. 

#Code corresponding to each Part
**Part 1:** data is in `calfits/`.

**Part 2:** this code is contained in the `findStar` method in `imageSubs.py` and is executed in `findStars.py`. This code outputs the text file `starPositions.txt` which contains the name of each file and the position of the star (x, y). NOTE: values are incorrect for acquisition images as the initial guess is too far from the true position. 

**Part 3 and 4:** this code is contained in the `register` method in `imageSubs.py` and executed in `psf.py`. This method shifts and rotates the images as well as creating sum and median images of the result. All furthur code uses the 'registered' images such that the location of the star is in the center of the image (512, 512).

**Part 5:** this code is contained and executed in `averings.py`.

**Part 6:** this code is contained and executed in `adi.py`.

**Part 7:** this code is contained and executed in `bdi.py` and outputs the text file `bestFitPSF.txt` which contains the name of the best fit psf for each image.

**Part 8:** this code uses the `findStar` method in imageSubs and is executed in `findObjects.py`. It outputs the text file `objectPositions.txt` which contains the locations of each object as well as the relative astrometry (r, PA).

#Output Files:#
Target 1 = ROXs 42B, Target 2 = ROXs 12.

The following table gives the location of each relevant file *after running the code*. I have coppied all relevant output files to `finalResults/` so that if you run the code and something fails you still have a copy of the results. 

| Part | Contents | file name/location |
|---|-------------|---------------------|
| 2 | x-y coordinates of the stars | starPositions.txt |
| 4 | sum/median registered images | results/target[1,2][sum,med].fits |
| 4 | sum/median rotated images | results/target[1,2]rot[sum,med].fits |
| 5 | sum/median rotated radially subtracted | results/ringsub.target[1,2]rot[med,sum].fits |
| 6 | sum/median rotated adi images | results/adi.target[1,2]rot[med,sum].fits |
| 7 | sum/median rotated bdi images | results/bdi.target[1,2]rot[med,sum].fits |
| 7 | table of best fit images | bestFitPSF.txt |
| 8 | table of positions of objects of interest | objectPositions.txt |
