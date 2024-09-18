from utils import read_video, save_video
from trackers import Tracker
import cv2
from teams_assigment import TeamAssigment

def main():
    video_frames = read_video("videos/08fd33_4.mp4")

    tracker = Tracker("models/best.pt")
    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path="stubs/track_stubs.pkl")
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


    #save cropped player
    # for track_id, player in tracks["players"][0].items():
    #    bbox = player["bbox"]
    #    frame = video_frames[0]
    #    cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
    #    cv2.imwrite("output_videos/cropped_img.jpg", cropped_image)
    #    break

    #Draw output 
    output_video_frames = tracker.draw_annotations(video_frames, tracks)
    
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()

