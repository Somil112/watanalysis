from flask import Flask, request,Response
import json
from flask_cors import CORS
from helper_funcs import process,topics
from time import time
import traceback

# TOTAL TIME TAKEN is 44.45044136047363 seconds
# TOTAL TIME TAKEN is 10.7 seconds
# TOTAL TIME TAKEN is 7.222671747207642 seconds


app = Flask(__name__)

CORS(app)

@app.route("/upload", methods=['POST'])
def upload():
    """
    Format : {"data": dict, "corpus":array}
    """
    file = request.files['file']
    a = time()
    try:
        print("RECEIVED DATA")
        data = process(file)
    except Exception:
        print(traceback.format_exc())
        return Response("",status=500)
    b = time()
    print("TOTAL TIME TAKEN is {}".format(b-a))
    return Response(json.dumps(data),status=200,mimetype="application/json")


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

    