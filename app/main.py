import cv2
import io
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from paddleocr import PaddleOCR
from PIL import Image
from typing import Dict
from ocr.extract_data import extract_data

app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.get('/')
async def home() -> Dict[str, str]:
    return {'message': 'Welcome to the ReceiptLogger API'}

@app.post('/extract-receipt')
async def extract_receipt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        raise HTTPException(status_code=400, detail='Invalid file type. Only PNG and JPG are supported.')

    # Read file content
    content = await file.read()
    
    # Open image with PIL
    img = Image.open(io.BytesIO(content)).convert('RGB')
    
    # Convert PIL image to NumPy array (RGB)
    img_np = np.array(img)
    
    # Convert RGB to BGR
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    response = ocr.ocr(img_bgr, cls=True)

    if not response or not response[0]:
        raise HTTPException(status_code=400, detail='Failed to extract receipt data.')

    return extract_data(response)
