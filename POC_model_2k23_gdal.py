import base64
import requests

from geotiff import *
from flask import Flask
app = Flask(__name__)
from pixel_to_lat_lon import *
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/satellite_model/',methods=['POST'])  # Single Api
def FP():
    values = {}

    resp=Response(status=200,content_type='application/json')
    mask_1=request.values['mask']
    image_1=request.values['image']
    d=request.values['d']
    d = json.loads(d)
    # print("d", type(d))

    decodeit = open('1_mask.png', 'wb')
    decodeit.write(base64.b64decode((mask_1)))
    decodeit.close()

    # print(d['I M A G E'])
    decodeit = open('1.jpg', 'wb')
    decodeit.write(base64.b64decode((image_1)))
    decodeit.close()

    sw_lat = d['BOUNDS']['_southWest']['lat']

    print(sw_lat)
    sw_long = d['BOUNDS']['_southWest']['lng']
    print(sw_long)
    ne_lat = d['BOUNDS']['_northEast']['lat']
    print(ne_lat)
    ne_long = d['BOUNDS']['_northEast']['lng']
    print(ne_long)
    southwest = [str(sw_lat), str(sw_long)]

    # print("southwest",southwest)

    northeast = [str(ne_lat), str(ne_long)]
    # print("northeast",northeast)
    gdal_convert("/home/ceinfo/PycharmProjects/Satellite_part_2", "1", southwest, northeast)
    #resp = geojson5("/home/ceinfo/PycharmProjects/Satellite_part_2","1")

    '''=========================================================='''

    with open("/home/ceinfo/PycharmProjects/Satellite_part_2/1.tif", "rb") as r1:
        converted_string = base64.b64encode(r1.read())

    with open("/home/ceinfo/PycharmProjects/Satellite_part_2/1_mask.png", "rb") as r2:
        converted_string_1 = base64.b64encode(r2.read())



    # os.remove("/home/ceinfo/PycharmProjects/Satellite_part_2/1.tif")
    # os.remove("/home/ceinfo/PycharmProjects/Satellite_part_2/1_mask.png")
    # os.remove("/home/ceinfo/PycharmProjects/Satellite_part_2/1.jpg")


    mask = json.dumps({'T I F': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8'))})

    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type

    url = 'http://10.10.21.228:7005/satellite_model/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask)]
    #print("files", files)
    values["geotag"] = request.form['geotag']
    #print("geotag", values)
    values["scale"] = request.form['scale']
    values["img_type"] = request.form['img_type']
    values["mask"] = mask
    print("hello")
    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)
    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=False)

