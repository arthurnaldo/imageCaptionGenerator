from flask import Flask
import computations


app = Flask(__name__)
state = {"caption": "", "image": None}

@app.route("/loadimage")
def loadimage(path):
    return computations.runpipeline(path)

@app.route("/returncaption")
def returncaption():
    return state["caption"]

