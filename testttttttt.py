import http.client
import mimetypes
from codecs import encode

conn = http.client.HTTPSConnection("10.10.21.159", 5009)
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('122222.json')))

fileType = mimetypes.guess_type('/home/dhruv/Desktop/122222.json')[0] or 'application/octet-stream'
dataList.append(encode('Content-Type: {}'.format(fileType)))
dataList.append(encode(''))

with open('/home/dhruv/Desktop/122222.json', 'rb') as f:
  dataList.append(f.read())
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
   'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/batchfacedetection", payload, headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))