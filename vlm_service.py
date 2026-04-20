import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import os
import io
# Check if GPU is available, else use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# Use float16 for GPU (faster), float32 for CPU (more stable)
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

print(f"Loading Moondream2 on {device}...")

# 1. Load the Base Model (Unit 1 & 5: LLM Architectures)
model_id = "vikhyatk/moondream2"
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True, 
    dtype=dtype
).to(device)

tokenizer = AutoTokenizer.from_pretrained(model_id)

def process_image_with_vlm(image_input):
    """
    Handles both a file path (string) or an UploadedFile object.
    """
    try:
        # Check if the input is already a PIL Image or an UploadedFile
        if hasattr(image_input, 'read'):
            # It's an UploadedFile object from Streamlit/FastAPI
            image = Image.open(io.BytesIO(image_input.read()))
        elif isinstance(image_input, str):
            # It's a string path
            image = Image.open(image_input)
        else:
            # It's already an Image object or something else
            image = image_input

        # Convert to RGB to ensure compatibility (handles PNG/RGBA)
        image = image.convert("RGB")
        
        # Inference
        with torch.no_grad():
            finding = model.answer_question(image, "Describe the car damage.", tokenizer)
        
        return {
            "status": "success",
            "model": "moondream2-base",
            "finding": finding,
            "estimated_cost": 6000,
            "confidence": 0.85
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}