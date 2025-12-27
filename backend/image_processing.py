from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def enhance_image(image):
    """
    Natural image enhancement that preserves realistic look while improving quality.
    """
    try:
        if image is None:
            return image
        
        # Ensure image is uint8 BGR
        if image.dtype != np.uint8:
            image = cv2.convertScaleAbs(image)
        
        # Step 1: Gentle denoising
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 6, 6, 7, 21)
        
        # Step 2: Subtle sharpening
        gaussian = cv2.GaussianBlur(denoised, (0, 0), 2.0)
        sharpened = cv2.addWeighted(denoised, 1.2, gaussian, -0.2, 0)
        
        # Step 3: CLAHE for contrast
        lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        
        lab_enhanced = cv2.merge((l_clahe, a, b))
        enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 4: Subtle color saturation
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.1, 0, 255)
        enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 5: Bilateral filter
        enhanced = cv2.bilateralFilter(enhanced, 5, 50, 50)
        
        # Step 6: Final sharpening
        kernel = np.array([[0, -0.5, 0],
                          [-0.5, 3, -0.5],
                          [0, -0.5, 0]])
        final = cv2.filter2D(enhanced, -1, kernel)
        final = cv2.addWeighted(enhanced, 0.7, final, 0.3, 0)
        
        return final
    
    except Exception as e:
        print(f"Error in enhance_image: {str(e)}")
        return image  # Return original if enhancement fails

@app.post("/enhance")
async def enhance_endpoint(file: UploadFile = File(...)):
    try:
        # Read uploaded file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"error": "Could not decode image"}
        
        # Enhance image
        enhanced_img = enhance_image(img)
        
        # Convert back to bytes
        success, buffer = cv2.imencode('.jpg', enhanced_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        if not success:
            return {"error": "Could not encode image"}
        
        io_buf = BytesIO(buffer.tobytes())
        
        return StreamingResponse(io_buf, media_type="image/jpeg")
    
    except Exception as e:
        print(f"Error in enhance_endpoint: {str(e)}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Image Enhancement API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)