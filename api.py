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
    
    # Calculate the total number of frames
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use 'XVID', 'MJPG', 'X264', etc.
    out = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (frame_width, frame_height))
    
    frame_number = 0

    # Process each frame
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Calculate timestamp
        timestamp = frame_number / frame_rate
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)
        milliseconds = int((timestamp - int(timestamp)) * 1000)
        
        # Print timestamp slices
        if frame_number % int(frame_rate * 2) == 0:  # Every 2 seconds
            print(f"Frame number {frame_number + 1} timestamp {minutes:02}:{seconds:02}:{milliseconds:03}")
        
        out.write(frame)
        frame_number += 1

    # Print remaining timestamp if less than 2 seconds
    remaining_time = frame_count / frame_rate
    if remaining_time % 2 != 0:
        remaining_minutes = int(remaining_time // 60)
        remaining_seconds = int(remaining_time % 60)
        remaining_milliseconds = int((remaining_time - int(remaining_time)) * 1000)
        print(f"Frame number {frame_number} timestamp {remaining_minutes:02}:{remaining_seconds:02}:{remaining_milliseconds:03}")

    video_capture.release()
    out.release()
    
    return {"filename": file.filename, "output_file": "processed_" + file.filename, "total_frames": frame_count, "processed_frames": frame_number}

@app.post("/user_input/")
async def text(text: str):
    return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
