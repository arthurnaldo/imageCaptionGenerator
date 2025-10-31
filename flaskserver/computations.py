from PIL import Image
from sentence_transformers import SentenceTransformer
import os
import get_database

model = SentenceTransformer('clip-ViT-B-32')
iid = 0
image_folder = os.path.join(os.path.dirname(__file__), "..", "storage")
curr_folder = None
database = get_database.get_database()
content = ""
image = None

print(database)

def getimage(path):
    global image
    image = Image.open(path)

def loadimage():
    global curr_folder
    filename = f"image{iid}.png"
    foldername = f"folder{iid}"
    curr_folder = foldername
    target_dir = os.path.join(image_folder, foldername)
    os.makedirs(target_dir, exist_ok=True)
    full_path = os.path.join(target_dir, filename)
    image.save(full_path)

def loadvector():
    global curr_folder
    global content
    img_path = os.path.join(image_folder, curr_folder, f"image{iid}.png")
    emb = model.encode([Image.open(img_path)], convert_to_tensor=False, normalize_embeddings=True)
    content = str(emb[0].tolist())
    content_path = os.path.join(image_folder, curr_folder, f"embedding{iid}.txt")
    with open(content_path, "w") as file:
        file.write(content)

def insert_into_database():
    response = (
        database.table("image_embeddings")
        .insert({"id": iid, "embedding": content})
        .execute()
    )

def decodevector():
    pass


def runpipeline(path):
    global iid
    getimage(path)
    loadimage()
    loadvector()
    insert_into_database()
    iid += 1

def getcaption():
    pass