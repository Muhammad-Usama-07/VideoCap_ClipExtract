# VideoCap_ClipExtract

## Run the project

Step # 01
  open cmd in projects's folder

Step # 02 (hit this command in cmd)
  uvicorn api:app --reload
  
Step # 02
  it will open the fastapi's swagger with default address http://127.0.0.1:8000

## Task 01
  For task 01 i have made and endpoint i fastapi called "input_video", which take video file as input and save that video file in a folder, after that, it will extract caption from video's frame after every 2 second and the save the data with caption and it's corresponding timestamp of the video in a csv file

### Data extracted from video

![image](https://github.com/user-attachments/assets/d08c4c9e-5e9a-41de-b831-e08f3c475972)


