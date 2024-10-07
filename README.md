# Sports Tracking & Analytics

This project implements a tracking and analysis system for sports videos, extracting useful player statistics such as speed, distance covered, and team ball possession. The objective is to analyze player movements in real-time by processing video footage and calculating individual and team metrics.
Features

    Player and Ball Tracking: Detects and tracks players and the ball in each frame of the video.
    Speed & Distance Calculation: Computes player speeds (in km/h) and total distance covered (in meters) over time.
    Camera Movement Estimation: Adjusts the positions of players to compensate for camera movement, ensuring accurate tracking data.
    Team Identification: Uses jersey colors to assign players to teams, with corrections for specific known player IDs.
    Ball Possession: Automatically assigns ball possession to the closest player and tracks team control of the ball throughout the game.

## Tools & Libraries Used

    YOLOv5: Used for detecting players and the ball in each frame of the video.
    OpenCV (cv2): Utilized for image processing tasks, including feature tracking for camera movement estimation and drawing player statistics on frames.
    Pandas: Used for handling structured data related to player positions and statistics.
    NumPy: For efficient numerical calculations, especially in transforming coordinates and calculating distances.
    Scikit-learn: Utilized for KMeans clustering to identify team affiliations based on jersey colors.

## How It Works

    Tracking: YOLOv5 is applied to detect players and the ball in each frame. The detected positions are tracked over time.
    Perspective Transformation: The players' positions in the video frame are transformed into real-world coordinates using OpenCV, allowing accurate measurement of speed and distance.
    Camera Movement Compensation: A camera movement estimation algorithm adjusts player positions to account for any panning or zooming of the camera.
    Team Assignment: Player jersey colors are analyzed and clustered to determine which team each player belongs to.
    Ball Possession: The system determines which player has the ball at any given moment based on proximity and tracks team control of the ball.

## Analysis Videos

Here are some example videos where this system was applied for analysis:

    Video Analysis 1 – Link to the first video
    Video Analysis 2 – Link to the second video

## Future Improvements

    Dynamic Field of View: Adjust the perspective transformation dynamically to handle changing camera angles.
    Enhanced Team Detection: Improve the team assignment logic to handle edge cases more reliably.
    More Robust Ball Possession: Refine the ball possession algorithm to handle edge cases where the nearest player isn't always the one controlling the ball.
    Player Tracking at All Times: Implement continuous player tracking to avoid misidentifying players when they disappear or reappear in the frame.
    Better AI Training with More Data: Train the object detection models with larger and more diverse datasets for more accurate and consistent analysis.
