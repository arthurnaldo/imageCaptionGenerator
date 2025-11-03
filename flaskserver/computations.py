from PIL import Image
from sentence_transformers import SentenceTransformer
import os
from io import BytesIO
import base64
import json
import get_database

model = SentenceTransformer('clip-ViT-B-32')
database = get_database.get_database()

session_data = {"iid": 0, "content": "", "png_b64": None, "image": None}


def getimage(path):
    session_data["image"] = Image.open(path)

def image2base64():
    buf = BytesIO()
    session_data["image"].save(buf, format="PNG")  
    png_bytes = buf.getvalue()   
    session_data["png_b64"] = base64.b64encode(png_bytes).decode("ascii")

def loadvector():
    emb = model.encode(image, convert_to_tensor=False, normalize_embeddings=True)
    session_data["content"] = str(emb.tolist())

def insert_into_database():
    response = (
        database.table("image_embeddings")
        .insert({"id": session_data["iid"], "embedding": session_data["content"], "imagebase64": session_data["png_b64"]})
        .execute()
    )

def getcaption():
    pass

def runpipeline(path):
    global iid
    getimage(path)
    image2base64()
    loadvector()
    insert_into_database()
    iid += 1

def login(user, password):
    #if user does not exist in database, we create a new user pass combo
    response = (
        database.table("auth").select("password").eq("username", user)
        .execute()
    )

    if len(response.data) == 0:
        response = (
            database.table("auth")
            .insert({"username": user, "password": password})
            .execute()
        )
        return "new account created", 200

    #if user does exist in database, we check if valid pass
    if password == response.data[0]["password"]:
        return "login successful", 200

    return "incorrect password", 404