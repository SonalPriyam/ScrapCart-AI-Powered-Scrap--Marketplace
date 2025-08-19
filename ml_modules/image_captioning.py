import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

@st.cache_resource
def get_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def generate_image_caption(image_file):
    processor, model = get_blip_model()
    img = Image.open(image_file).convert('RGB')
    inputs = processor(img, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

