from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Ensure the upload directory exists
UPLOAD_DIRECTORY = "./uploaded_videos"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.post("/echo-text/")
async def echo_text(text: str = Form(...)):
    return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
