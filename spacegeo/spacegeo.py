import urllib.request as request
import os
import sys
import json
import urllib.error
import cv2
import numpy as np
from PIL import Image 
import io
import base64

from nasa import earth

class SpaceGeo:
    ISS_POS_API_URL = "http://api.open-notify.org/iss-now.json"
    GEO_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    MIN_CLOUD_SCORE = 0.15

    def __init__(self, nasa_api_key, geo_api_key):
        self.geo_api_key = geo_api_key
        
        if not 'NASA_API_KEY' in os.environ:
            os.environ['NASA_API_KEY'] = nasa_api_key

    def convertCvImage(self, pil_image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def getEarthImage(self, latlon=None, begin='2016-01-01', size=None, h_ratio=None, w_ratio=None, encode=False):
        if latlon==None or len(latlon) != 2:
            latlon = self.getIssLatlon()
        if latlon:
            try:
                assets = earth.assets(lat=latlon[0],lon=latlon[1], begin=begin)
                for asset in assets:
                    image = asset.get_asset_image(cloud_score=True)
                    if image.cloud_score and image.cloud_score < self.MIN_CLOUD_SCORE:
                        cv_im = self.convertCvImage(image.image)
                        if h_ratio or w_ratio:
                            if h_ratio==None: h_ratio=1.0
                            if w_ratio==None: w_ratio=1.0
                            cv_im = cv_im[0:int(cv_im.shape[0]*h_ratio), 0:int(cv_im.shape[1]*w_ratio)]

                        if size:
                            cv_im = cv2.resize(cv_im,(int(cv_im.shape[0]*size),int(cv_im.shape[1]*size)))                            

                        result_image = Image.fromarray(cv_im[::-1, :, ::-1])
                        
                        if encode:
                            result_image = self.getByteImage(result_image)
                        return result_image
            except urllib.error.HTTPError as e:
                print(e)
                return None
        return None

    def getIssPosition(self):
        res = self.getJson(self.ISS_POS_API_URL)
        if res and 'iss_position' in res:
            return res['iss_position']
        return None
    
    def getGeoInfo(self, latlon=None, lang='ja', result_type='administrative_area_level_1'):
        if latlon==None or len(latlon) != 2:
            latlon = self.getIssLatlon()
               
        if latlon:
            url = self.GEO_API_URL \
                    + '?latlng=' + str(latlon[0]) + ',' + str(latlon[1]) \
                    + '&key=' + self.geo_api_key \
                    + '&language='+lang \
                    + '&result_type=' + result_type
            res = self.getJson(url)
            if 'results' in res and len(res['results']) >0:
                return res['results'][0]['formatted_address']        
        return None

    def getJson(self, url):
        try:
            res = request.urlopen(url)
        except urllib.error.HTTPError  as e:
            print(e)
            return None
        return json.loads(res.read().decode('utf-8'))
    
    def getIssLatlon(self):
        iss_pos = self.getIssPosition()
        return (float(iss_pos['latitude']), float(iss_pos['longitude']))
    
    def getByteImage(self, image):
        in_mem_file = io.BytesIO()
        image.save(in_mem_file, format = "PNG")
        in_mem_file.seek(0)
        return in_mem_file.read()
