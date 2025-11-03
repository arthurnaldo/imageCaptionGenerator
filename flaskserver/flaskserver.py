from flask import Flask, request, redirect
import computations
import os

app = Flask(__name__, static_folder="../client/src", static_url_path="")
state = {"caption": "", "image": None}
auth_state = {"username": None, "password": None}

@app.route("/login", methods=['POST'])
def auth():
    if auth_state["username"]:
        return "already logged in", 404
    
    auth_state["username"] = request.form.get("uname")
    auth_state["password"] = request.form.get("psw")

    payload, status = computations.login(auth_state["username"], auth_state["password"])
    if status >= 400: #is 404
        return payload, status

    return redirect("usercaptions.html")


@app.route("/getusername")
def getusername():
    if not auth_state["username"]:
        return "Username not found", 404
    return auth_state["username"]

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
