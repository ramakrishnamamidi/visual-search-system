import faiss
import numpy as np

def save_faiss_index(embeddings, metadata, index_path="image.index", metadata_path="metadata.npy"):
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    faiss.write_index(index, index_path)
    np.save(metadata_path, metadata)

def load_faiss_index(index_path="image.index", metadata_path="metadata.npy"):
    index = faiss.read_index(index_path)
    metadata = np.load(metadata_path, allow_pickle=True).item()
    return index, metadata
