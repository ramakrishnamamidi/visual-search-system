from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_explanation(query: str, image_url: str):
    raw_image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
    inputs = processor(raw_image, query, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return f"{caption}. Relevant to query: '{query}'"