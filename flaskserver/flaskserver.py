from flask import Flask, request
import computations
import os

app = Flask(__name__)
state = {"caption": "", "image": None}

@app.route("/loadimage")
def loadimage():
    path = request.args.get("path")
    return computations.runpipeline(path)

@app.route("/returncaption")
def returncaption():
    return state["caption"]

# @app.after_serving
# def on_shutdown():
#     directory_path = "../storage"
#     for item in os.listdir(directory_path):
#         item_path = os.path.join(directory_path, item)
#         try:
#             if os.path.isfile(item_path) or os.path.islink(item_path):
#                 os.unlink(item_path)  # Remove file or symbolic link
#             elif os.path.isdir(item_path):
#                 shutil.rmtree(item_path)  # Remove directory and its contents
#         except OSError as e:
#             print(f"Error deleting {item_path}: {e}")

if __name__ == '__main__':
    app.run(debug=True) # debug=True enables debug mode with reloader and debugger
