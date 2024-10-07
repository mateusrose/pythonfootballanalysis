import camera_movement
from utils import read_video, save_video
from trackers import Tracker
import cv2
import numpy as np
from teams_assigment import TeamAssigment
from player_ball_assigment import PlayerBallAssigment
from camera_movement import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistanceEstimator

def main():
    video_name = "03_trimmed"
    video_frames = read_video(f"videos/analysis_videos/{video_name}.mp4")

    tracker = Tracker("models/best.pt")
    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path="stubs/track_stubs.pkl")
    #get obj positions 
    tracker.add_position_to_tracks(tracks)

    #Camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames, read_from_stub = True, stub_path="stubs/camera_movement_stub.pkl")
    camera_movement_estimator.add_adjust_position_to_tracks(tracks,camera_movement_per_frame)


    #View transformer 
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)

    #interpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_position(tracks["ball"])

    #speed and distance 
    speed_and_distance_estimator = SpeedAndDistanceEstimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)


    #assign teams
    team_assigment = TeamAssigment()
    team_assigment.assign_team_color(video_frames[0],
                                     tracks["players"][0])
 
    for frame_num, player_track in enumerate(tracks["players"]):
        for player_id, track in player_track.items():
            team = team_assigment.get_player_team(video_frames[frame_num],
                                                  track["bbox"],
                                                  player_id)
            tracks["players"][frame_num][player_id]["team"] = team
            tracks["players"][frame_num][player_id]["team_color"] = team_assigment.team_colors[team]
## black player being recognized as white color

    #Assing ball to player
    team_ball_control = []

    player_assigment = PlayerBallAssigment()
    for frame_num, player_track in enumerate(tracks["players"]):
        ball_bbox = tracks["ball"][frame_num][1]["bbox"]
        assigned_player = player_assigment.assign_ball_to_player(player_track,ball_bbox)
        if assigned_player != -1:
            tracks["players"][frame_num][assigned_player]["has_ball"] = True
            team_ball_control.append(tracks["players"][frame_num][assigned_player]["team"])
        else:
            pass
        #team_ball_control.append(team_ball_control[0])
    team_ball_control = np.array(team_ball_control)


   # i = 0
    #save cropped player
   # for track_id, player in tracks["players"][0].items():
   #     bbox = player["bbox"]
   #     frame = video_frames[0]
   #     cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
   #     cv2.imwrite(f"output_videos/cropped_img{i}.jpg", cropped_image)
   #     i += 1
   #     if i > 24:
   #         break

    #Draw output 
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    #Draw camera movement
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    
    #draw speed and distance
    speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)
    save_video(output_video_frames, f"output_videos/{video_name}.avi")

if __name__ == "__main__":
    main()

