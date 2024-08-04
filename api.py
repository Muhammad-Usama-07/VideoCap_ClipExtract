# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# import os
# import cv2

# app = FastAPI()

# # Ensure the upload directory exists
# UPLOAD_DIRECTORY = "./uploaded_videos"
# OUTPUT_DIRECTORY  = "./processed_videos"
# os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
# os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# @app.post("/input_video/")
# async def video(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
#     output_file_path = os.path.join(OUTPUT_DIRECTORY, "processed_" + file.filename)
    
#         # with open(file_path, "wb") as f:
#         #     f.write(await file.read())
#         # # return {"filename": file.filename}

#     # Process the video file
#     video_capture = cv2.VideoCapture(file_path)
#     frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     frame_rate = video_capture.get(cv2.CAP_PROP_FPS)

#     # Define the codec and create VideoWriter object
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID', 'MJPG', 'X264', etc.
#     out = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (frame_width, frame_height))
    
#     frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_number = 0

#     while video_capture.isOpened():
#         ret, frame = video_capture.read()
#         if not ret:
#             break
#         # Calculate the timestamp for the current frame
#         timestamp = frame_number / frame_rate
#         print(f"Frame {frame_number}: Timestamp {timestamp:.2f} seconds")

#         # Process the frame (you can add any processing here)
#         # For example, convert to grayscale
#         # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Write the frame into the output video
#         out.write(frame)
#         frame_number += 1

#     video_capture.release()
#     out.release()
    
#     return {"filename": file.filename, "output_file": "processed_" + file.filename, "total_frames": frame_count, "processed_frames": frame_number}



# @app.post("/user_input/")
# async def text(text: str):
#     return {"text": text}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import cv2

app = FastAPI()

# Ensure the upload directory exists
UPLOAD_DIRECTORY = "./uploaded_videos"
OUTPUT_DIRECTORY = "./processed_videos"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

@app.post("/input_video/")
async def video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    output_file_path = os.path.join(OUTPUT_DIRECTORY, "processed_" + file.filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Process the video file
    video_capture = cv2.VideoCapture(file_path)
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID', 'MJPG', 'X264', etc.
    out = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (frame_width, frame_height))
    
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        # Calculate the timestamp for the current frame
        timestamp = frame_number / frame_rate
        print(f"Frame {frame_number}: Timestamp {timestamp:.2f} seconds")

        # Process the frame (you can add any processing here)
        # For example, convert to grayscale
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Write the frame into the output video
        out.write(frame)
        frame_number += 1

    video_capture.release()
    out.release()
    
    return {"filename": file.filename, "output_file": "processed_" + file.filename, "total_frames": frame_count, "processed_frames": frame_number}

@app.post("/user_input/")
async def text(text: str):
    return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
