
import requests
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
import re

app = FastAPI()


@app.middleware("http")
async def verify_asset(request, call_next):

    if 'Authorization' in request.headers:
        pass
    else:
        print('Parameter token missing')
        return JSONResponse(content={"code": "401", "auth": "unsuccessful", "error": "Authorization parameter missing",
                                     "message": "Authorization Parameter cannot be Missing"}, status_code=401)

    token = request.headers.get('Authorization')

    if len(token) != 0:
        print("1")
        try:
            print("2")
            token = str(token).lower().strip()
            print(token)
            if 'bearer' in token:
                token = token.replace('bearer ', '')

            assetid = 'ast1661851488i1868784548'

            print(token)

            ip = '127.0.0.1'
            domain = request.headers.get('host')

            url = f"https://outpost.mapmyindia.com/api/security/oauth/check_token?token={token}&api={assetid}&ip={ip}&domain={domain}"

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic '
                                 'c0sySUxhcF9fcC03d2xtaGZjdGhiM01IMkN1OENQdmV2V0k4UjlnOUZKS1hETDFBQ05GLVM4NEFtdi1uNDJUd'
                                 'FZLaVB6SHhoZmxtQ0dURExSSFhvQlE9PTp0TThpUlZwRkp6VHdlaFltY2JWVjJMNzk2QzhSNTBvZGMtWUd2S'
                                 'khnaV9PeUY3QkhZZjg1RVFra3MzZ21tZi0weWdDVV96ZjNOSDY2Qzc2RktnR1Iwb3dyYWpxOGNpcVQ= '
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            print('outpost response ', response)

            if response.status_code != 200:
                print("invalid token")

                return JSONResponse(
                    content={"code": "401", "auth": "unsuccessful", "error": "Access Denied",
                             "message": "Invalid Authorization token"},
                    status_code=401)

            else:
                print('token verified')

        except Exception as e:
            print(e)

            return JSONResponse(
                content={"code": "503", "auth": "unsuccessful", "error": f"error while verifying token \n{str(e)}",
                         "message": "Service down temporarly for maintainence"},
                status_code=401)

    else:
        return JSONResponse(
            content={"code": "401", "auth": "unsuccessful", "error": "empty token parameter",
                     "message": "Authorization Parameter cannot be Empty"},
            status_code=401)

    response = await call_next(request)
    return response




@app.post('/Habitation')
async def Habitation(geotag: str = Form(default=None),
                scale: str = Form(default=None),
                img_type: str = Form(default=None),
                file: UploadFile = File(default=None),
                bounds: str = Form(default=None)):
    try:
        if not file or file.filename == '':
            return JSONResponse(content={"code": "400", "error": "Image file is required",
                                         "message": "File parameter cannot be empty or missing."}, status_code=400)

        elif not geotag:
            return JSONResponse(content={"code": "400", "error": "Geotag is required",
                                         "message": "Geotag cannot be empty or missing."}, status_code=400)

        elif not img_type:
            content = {"code": "400", "error": "Image type is required",
                       "message": "Image type cannot be empty or missing."}
            return JSONResponse(content=content, status_code=400)

        elif not scale:
            content = {"code": "400", "error": "Scale is required",
                       "message": "Scale parameter cannot be empty or missing."}
            return JSONResponse(content=content, status_code=400)

        if not file.filename.split('.')[1].lower() in ['jpg', 'jpeg', 'png', 'tiff', 'tif']:
            return JSONResponse(content={"code": "400", "error": "Invalid Image Format",
                                         "message": "Invalid image format. Valid file formats : png, jpg, jpeg, tiff, "
                                                    "tif"}, status_code=400)
        try:
            scale = int(scale)
        except:
            return JSONResponse(content={"code": "400", "error": "Scale should be a valid integer",
                                         "message": "Invalid Scale. Scale should be a valid integer."}, status_code=400)

        if not scale > 0:
            return JSONResponse(content={"code": "400", "error": "Scale should be greater than 0",
                                         "message": "Invalid Scale value. Scale should be greater than zero"},
                                status_code=400)

        if not img_type.lower() in ['google' ,'bhuvan']:
            return JSONResponse(content={"code": "400", "error": "Invalid Image Type",
                                         "message": "Invalid image_type, valid image type are: google and bhuvan"}, status_code=400)

        if geotag not in ['0', '1', '2']:
            return JSONResponse(content={"code": "400", "error": "Invalid Geotag value",
                                         "message": "Invalid Geotag Value. Valid geotag values : 0, 1 and 2"},
                                status_code=400)

        if geotag == '0' and not file.filename.split('.')[1].lower() in ['jpg', 'jpeg', 'png']:
            return JSONResponse(content={"code": "400", "error": "Invalid Image format for geotag 0",
                                         "message":"Invalid Image file format for geotag value 0, valid file format for geotag 0 are png, jpg and jpeg"}, status_code=400)

        if geotag == '1' and not file.filename.split('.')[1].lower() in ['tiff', 'tif']:
            return JSONResponse(content={"code": "400", "error": "Invalid Image format for geotag 1",
                                         "message":"Invalid Image file format for geotag value 1, valid file format for geotag 1 are tiff and tif"}, status_code=400)

        if geotag == '2' and not bounds:
            return JSONResponse(content={"code": "400", "error": "Bounds Required for geotag 2",
                                         "message": "Bounds cannot be empty or missing for Geotag 2"}, status_code=400)

        if geotag == '2' and not file.filename.split('.')[1].lower() in ['jpg', 'jpeg', 'png']:
            return JSONResponse(content={"code": "400", "error": "Invalid Image format for geotag 2",
                                         "message":"Invalid Image file format for geotag value 2, valid file format for geotag 2 are png, jpg and jpeg"}, status_code=400)

        url1 = 'http://10.10.21.159:6003/Habitation'

        clean_file_name = re.sub(r'[^\w.-]', '_', file.filename)
        files = {
            'file': (clean_file_name, file.file),
            'scale': (None, scale),
            'geotag': (None, geotag),
            'img_type': (None, img_type)
        }

        headers = {}

        if geotag == "0":
            r = requests.post(url1, headers=headers, files=files)

        elif geotag == "1":
            r = requests.request("POST", url1, files=files, headers=headers)

        elif geotag == "2":
            try:
                param3 = eval(str(bounds))
                assert isinstance(param3, dict)
                files["bounds"] = (None, bounds)
                print(files)
            except:
                return JSONResponse(
                    content={"code": "400", "error": "Invalid bounds parameter",
                             "message": "Invalid bounds."},
                    status_code=400)

            r = requests.request("POST", url1, files=files, headers=headers)

        if r.status_code == 200:
            print('returning status code', r.status_code)

            x = {
                "code": "200",
                "message": "success",
                "result": r.json()
            }

            # return r.json()
            return x
        else:
            return JSONResponse(
                content={"code": "400", "error": "Something went wrong while processing the image",
                         "message": "Something went wrong while processing your image. Please try again later."},
                status_code=400)
    except Exception as e:
        print(e)
        return JSONResponse(content={"code": "500", "error": str(e),
                                     "message": "SERVER ERROR. Please try again later"}, status_code=500)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=7000)






