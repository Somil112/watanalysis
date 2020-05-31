from flask import Flask, request,Response
import json
from flask_cors import CORS
from helper_funcs import process,topics
from time import time
import datetime
import traceback
import os


# TOTAL TIME TAKEN is 44.45044136047363 seconds
# TOTAL TIME TAKEN is 10.7 seconds
# TOTAL TIME TAKEN is 7.222671747207642 seconds


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024


CORS(app)

@app.route("/upload", methods=['POST'])
def upload():
    """
    Format : {"data": dict, "corpus":array}
    """
    file = request.files['file']
    if os.path.splitext(file.filename)[1].lower() == ".txt":
        a = time()
        try:
            print("RECEIVED DATA")
            data = process(file)
        except Exception:
            err = traceback.format_exc()
            print(err)
            with open("errors.txt", "a") as myfile:
                myfile.write(datetime.datetime.now().strftime("%d %b %Y %I:%m %p") + "\n" + err)
            
            return Response("",status=500)
        b = time()
        print("TOTAL TIME TAKEN is {}".format(b-a))
        return Response(json.dumps(data),status=200,mimetype="application/json")
    else:
        print("Server Error")
        return Response("Server Error",status=500)


@app.route("/gen_topics",methods=['POST'])
def gen_topics():
    data = request.json
    try:
        gentopics = topics(data["data"],data["corpus"])
    except:
        return Response("",status=500)
    
    return Response(json.dumps({"data":gentopics}),status=200,mimetype="application/json")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

    