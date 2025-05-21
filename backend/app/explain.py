from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import asyncio
from .utils import load_image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

def sync_generate(query: str, image_url: str):
    raw_image = load_image(image_url)
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return f"{caption}. Relevant to query: '{query}'"

async def generate_explanation(query: str, image_url: str):
    return await asyncio.to_thread(sync_generate, query, image_url)