import os
import cv2
from ultralytics import YOLO  

model = YOLO('best (7).pt')  

video_folder = './Test_Videos'

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print(f"End of video or can't fetch the frame for {video_path}.")
            break

        results = model(frame)

        for result in results:

            frame = result.plot() 

        cv2.imshow(f'Bird Detection - {video_path}', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            print(f"Quitting video: {video_path}")
            break

    cap.release()
    cv2.destroyAllWindows()

def process_all_videos(video_folder):
    for filename in os.listdir(video_folder):
        if filename.endswith(".mp4"): 
            video_path = os.path.join(video_folder, filename)
            print(f"Processing video: {video_path}")
            process_video(video_path)

#process_all_videos(video_folder)

video_path = os.path.join(video_folder, 'testvideo11.mp4')
process_video(video_path)