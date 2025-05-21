from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from .search import search_images
from .explain import generate_explanation
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(query: str = Query(..., description="Search query")):
    results = search_images(query)
    tasks = [generate_explanation(query, res["image_url"]) for res in results]
    explanations = await asyncio.gather(*tasks)

    output = [
        {"image_url": f"/image/{os.path.basename(result['image_url'])}", "explanation": explanation}
        for result, explanation in zip(results, explanations)
    ]
    return {"results": output}

@app.get("/image/{filename}")
async def get_image(filename: str):
    image_path = os.path.join("data", "processed", filename)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path, media_type="image/jpeg")