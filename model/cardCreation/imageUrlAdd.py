from . import  imageHelper
import json
def imageUrlAdder(jsonList):
    print("Started to find and add URL's for images and all ...")
    for i in range(len(jsonList)):
        # print(jsonList[i],type(jsonList[i]))
        jsonList[i]["url"]=imageHelper.fetch_image_url(jsonList[i]["image_keywords"][0])
    return jsonList


