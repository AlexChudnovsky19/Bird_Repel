import os
import cv2
from ultralytics import YOLO  

model = YOLO('best (6).pt')  # Loads your trained YOLO model

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

        # Run the YOLO model on the current frame
        results = model(frame)

        # Render detections and update the frame
        for result in results:
            # Modify the frame with the detections (bounding boxes and labels)
            frame = result.plot()  # Assign the frame with rendered detections back to `frame`

        cv2.imshow(f'Bird Detection - {video_path}', frame)

        # Press 'q' to stop the video early and move to the next video
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

process_all_videos(video_folder)
