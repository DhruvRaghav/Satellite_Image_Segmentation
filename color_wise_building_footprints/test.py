# # Python 3 program to calculate Distance Between Two Points on Earth
# from math import radians, cos, sin, asin, sqrt
#
#
# def distance(lat1, lat2, lon1, lon2):
#     # The math module contains a function named
#     # radians which converts from degrees to radians.
#     lon1 = radians(lon1)
#     lon2 = radians(lon2)
#     lat1 = radians(lat1)
#     lat2 = radians(lat2)
#
#     # Haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#
#     c = 2 * asin(sqrt(a))
#
#     # Radius of earth in kilometers. Use 3956 for miles
#     r = 6371
#
#     # calculate the result
#     return (c * r)
#
#
# # driver code
# lat1 = 53.32055555555556
# lat2 = 53.31861111111111
# lon1 = -1.7297222222222221
# lon2 = -1.6997222222222223
# print(distance(lat1, lat2, lon1, lon2), "K.M")




'''------------------------------------------------------------------------------------'''



from flask import Flask, request,Response,jsonify,make_response
app = Flask(__name__)
import jwt
import datetime
from functools import wraps
app.config['SECRET_KEY'] = 'thisisthekey'
def token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token=request.args.get('token')


@app.route('/unprotected')
def unprotected():
    return '1'


@app.route('/protected')
def protected():

    return '2'

@app.route('/login',methods=['POST'])

def login():
    print(" Welcome, now authentication would be required:")

    auth=int(request.form.get['token'])
    print(auth)
    if auth and auth.password =="password":
        token =jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])

        return jsonify({'token':token.decode('UTF-8')})

    return make_response("could not  verify",401,{'WWW.Authenticate':'Basic realm="Login Required"'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
