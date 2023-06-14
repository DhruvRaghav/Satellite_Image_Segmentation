import PIL
from flask import Flask, request, jsonify
from PIL import Image
import base64
import io

from matplotlib import pyplot as plt

app = Flask(__name__)


@app.route('/processing', methods=['POST'])
def process():
    file = request.files['image']


    # data = file.stream.read()
    # data = base64.b64encode(data).decode()


    #img.save(buffer, 'png')
    #buffer.seek(0)

    # data = buffer.read()
    # data = base64.b64encode(data).decode()

    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7009, debug=False)