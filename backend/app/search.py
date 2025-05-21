import open_clip
from PIL import Image
import numpy as np
import faiss
import torch
import os

model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device).eval()

index = faiss.read_index('embeddings/image.index')
metadata = np.load('embeddings/metadata.npy', allow_pickle=True)

def search_images(query: str, top_k: int = 5):
    with torch.no_grad():
        text_input = tokenizer([query])
        text_features = model.encode_text(text_input.to(device)).cpu().numpy().astype('float32')

    scores, indices = index.search(text_features, top_k)
    results = []
    for idx in indices[0]:
        image_path = str(metadata[idx]).replace("\\", "/")
        results.append({"image_url": image_path})
    return results
