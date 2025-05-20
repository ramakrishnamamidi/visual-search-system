from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .search import search_images
from .explain import generate_explanation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
async def search(query: str = Form(...)):
    results = search_images(query)
    explanations = [generate_explanation(query, res) for res in results]
    return {"results": results, "explanations": explanations}