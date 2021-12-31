# importing the requests library
import requests

# defining the api-endpoint
API_ENDPOINT = "http://10.10.21.159:7005/satellite_FP"

# data to be sent to api
data = {'geotag': '0'}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)
print(r.text)
