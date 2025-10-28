import torch, clip
from PIL import Image

model, preprocess = clip.load("ViT-B/32", device="cpu")
iid = 0
image_folder = "../storage"
image = None

def getimage(path):
    global image
    image = Image.open(path)

def loadimage():
    filename = f"image{iid}.png"
    full_path = os.path.join(image_folder, filename)
    image.save(full_path)

def getvector():
    img = preprocess(Image.open(f"../storage/image{iid}.png")).unsqueeze(0)
    with torch.no_grad():
        vec = model.encode_image(img)
        vec = vec / vec.norm(dim=-1, keepdim=True)
    return vec

def runpipeline(path):
    getimage(path)
    loadimage()
    return getvector()

def getcaption():
    pass