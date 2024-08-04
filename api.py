from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import cv2
from transformers import pipeline
import pandas as pd
from fuzzywuzzy import fuzz
from moviepy.video.io.VideoFileClip import VideoFileClip

app = FastAPI()


image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file_path, fourcc, frame_rate, (frame_width, frame_height))
    
    frame_number = 0
    cap_number = 0
    data = {'cap_number':[],'caption': [], 'timestamp': []}

    prev_minutes, prev_seconds, prev_milliseconds = 0, 0, 0
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
        
        time_stamp = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

        if frame_number % int(frame_rate * 2) == 0:  # Every 2 seconds
            if frame_number == 0:
                print(f"Frame number {frame_number + 1} timestamp {time_stamp}")
            else:
                cv2.imwrite(f'processed_videos/frame_{frame_number + 1}.jpg', frame)
                previous_timestamp = f"{prev_minutes:02}:{prev_seconds:02}:{prev_milliseconds:03}"
                time_range = [previous_timestamp, time_stamp]
                print(f"\n***** Frame number {frame_number + 1} timestamp {time_range}")
                
                cap = image_to_text(f"processed_videos/frame_{frame_number + 1}.jpg")[0]['generated_text']
                print(f"***** Caption {cap}\n")
                cap_number+=1
                data['cap_number'].append('cap_'+ str(cap_number))
                data['caption'].append(cap)
                data['timestamp'].append(time_range)

            prev_minutes, prev_seconds, prev_milliseconds = minutes, seconds, milliseconds
            
            
        out.write(frame)
        frame_number += 1

        if frame_number == frame_count:
            cv2.imwrite(f'processed_videos/frame_{frame_number}.jpg', frame)
            previous_timestamp = f"{prev_minutes:02}:{prev_seconds:02}:{prev_milliseconds:03}" 
            time_range = [previous_timestamp, time_stamp]
            print(f"\n*****Frame number {frame_number} timestamp {time_range}")
            cap = image_to_text(f"processed_videos/frame_{frame_number}.jpg")[0]['generated_text']
            print(f"*****Caption {cap}\n")
            data['cap_number'].append('cap_'+ str(cap_number))
            data['caption'].append(cap)
            data['timestamp'].append(time_range)
            

    video_capture.release()
    out.release()
    

    # Create a list of formatted timestamps
    formatted_timestamps = [
        f"{ts[0]} - {ts[1]}" for ts in data["timestamp"]
    ]

    # Create a DataFrame
    df = pd.DataFrame({
        "cap_number": data["cap_number"],
        "caption": data["caption"],
        "timestamp": formatted_timestamps
    })

    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)


    return {
        "data": data
    }
@app.post("/user_input/")
async def text(text: str):
    input_text = text
    df = pd.read_csv('output.csv') 
    # Load the video
    video_path = 'uploaded_videos/video_file.mp4'  # Replace with your video file path
    video = VideoFileClip(video_path)

    matching_clips = []
    matching_captions = []
    matching_timestamps = []
    clip_output_path = []

    for index, row in df.iterrows():
        caption = row['caption']
        similarity_score = fuzz.token_set_ratio(input_text, caption)
        print('similarity_score', similarity_score)
        
        if similarity_score >= 85:  # Or any threshold you consider perfect
            
            start_time, end_time = row['timestamp'].split(' - ')
            start_seconds = timestamp_to_seconds(start_time)
            end_seconds = timestamp_to_seconds(end_time)

            # Slice the video
            clip = video.subclip(start_seconds, end_seconds)

            # Save the clip
            output_path = f"uploaded_videos/{clip_num}.mp4"
            clip.write_videofile(output_path, codec='libx264')

            # saving all items in the list
            matching_clips.append(row['cap_number'])
            matching_captions.append(caption)
            matching_timestamps.append(row['timestamp'])
            clip_output_path.append(output_path)

    if matching_captions:
        return {
            "data": {
                "clip_num":matching_clips,
                "caption": matching_captions,
                "timestamp": matching_timestamps,
                'clip_path': clip_output_path
            }
        }
    else:
        return {"data": {"caption": [], "timestamp": []}}
    # return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
