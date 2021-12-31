#
#  Example from code built on the Flask web framework (and Werkzeug)
#  Accepts uploading a photo file in the 'photo' form member, then
#  copies it into a memory byte array and converts it to a numpy array
#  which in turn can be decoded by OpenCV.
#
#  Beware that this increases the memory pressure and you should 
#  configure a max request size before doing so.
# 
#  It saves a round-trip to a temporary file, though.

import flask
from flask import render_template, json, jsonify, request
import numpy as np
import cv2
import io
# ...

# Remember to set a max content length 
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

# ...

# Here is the code to convert the post request to an OpenCV object

if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)