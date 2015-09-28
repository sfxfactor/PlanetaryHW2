rm -rf results
mkdir results
python findStar.py
python psf.py
python averings.py
python adi.py
python bdi.py
