import os
import torch
import open_clip
from PIL import Image
from torchvision import transforms
import numpy as np
import faiss
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# CONFIGURATION
IMAGE_DIR = "data/processed"
BATCH_SIZE = 64
OUTPUT_INDEX = "embeddings/image.index"
OUTPUT_META = "embeddings/metadata.npy"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load OpenCLIP
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model = model.to(DEVICE).eval()

# Image preprocessing
def load_image(path):
    try:
        img = Image.open(path).convert("RGB")
        return preprocess(img)
    except:
        return None

# Load all image paths
image_paths = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('jpg', 'png'))])

# Parallel load with thread pool
def load_images_batch(batch_paths):
    with ThreadPoolExecutor() as executor:
        batch_images = list(executor.map(load_image, batch_paths))
    valid = [(img, path) for img, path in zip(batch_images, batch_paths) if img is not None]
    if not valid:
        return None, None
    images, paths = zip(*valid)
    return torch.stack(images), list(paths)

# Process in batches
all_embeddings = []
all_metadata = []

for i in tqdm(range(0, len(image_paths), BATCH_SIZE)):
    batch_paths = image_paths[i:i + BATCH_SIZE]
    image_tensor, valid_paths = load_images_batch(batch_paths)

    if image_tensor is None:
        continue

    image_tensor = image_tensor.to(DEVICE)

    with torch.no_grad():
        image_features = model.encode_image(image_tensor).cpu().numpy()

    all_embeddings.append(image_features)
    all_metadata.extend(valid_paths)

# Concatenate and index
emb_matrix = np.concatenate(all_embeddings, axis=0).astype('float32')
index = faiss.IndexFlatL2(emb_matrix.shape[1])
index.add(emb_matrix)

os.makedirs("embeddings", exist_ok=True)
faiss.write_index(index, OUTPUT_INDEX)
np.save(OUTPUT_META, np.array(all_metadata))

print(f"Done: {len(all_metadata)} embeddings indexed.")
