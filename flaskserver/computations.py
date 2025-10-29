from PIL import Image
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('clip-ViT-B-32')
iid = 0
image_folder = os.path.join(os.path.dirname(__file__), "..", "storage")
curr_folder = None
image = None

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
    img_path = os.path.join(image_folder, curr_folder, f"image{iid}.png")
    emb = model.encode([Image.open(img_path)], convert_to_tensor=False, normalize_embeddings=True)
    content = str(emb[0].tolist())
    content_path = os.path.join(image_folder, curr_folder, f"embedding{iid}.txt")
    with open(content_path, "w") as file:
        file.write(content)

def runpipeline(path):
    global iid
    getimage(path)
    loadimage()
    loadvector()

def getcaption():
    pass