# SpaceGeo

SpaceGeo can get International Space Station (ISS) location and the location earth image.

## Confirmed environments
- Python 3.5.2 :: Anaconda custom (64-bit)
- cv2 (OpenCV)
- numpy
- PIL ([Python Imaging Library](http://www.pythonware.com/products/pil/))
- nasa-api ([brendanv/nasa-api](https://github.com/brendanv/nasa-api))

etc.

## Tutorial

### Git clone
git clone https://github.com/dyson-yamashita/spacegeo.git

Python notebook tutorial in spacegeo/notebook.

## Sample
```python
import sys

sys.path.append('../spacegeo') 
from spacegeo import SpaceGeo

# Set API keys.
nasa_api_key = '<NASA API KEY>'
ggl_geo_api_key = '<GOOGLE GEOCODING API KEY>'
sg = SpaceGeo(nasa_api_key, ggl_geo_api_key)

# Get latitude and longitude of ISS.
latlon = sg.getIssLatlon()

# Get geolocation information.
geo_info = sg.getGeoInfo(latlon=latlon)

# Get geolocation image.
sg.getEarthImage(latlon=latlon)
```

