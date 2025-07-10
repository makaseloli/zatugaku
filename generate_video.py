from moviepy import ImageClip, AudioFileClip, VideoFileClip, concatenate_audioclips, CompositeAudioClip
import os
import pathlib

def create_video(image_path, audio_path, output_filename):
    """1つの画像と音声から動画を作成"""

    audio_clip = AudioFileClip(audio_path)

    image_clip = ImageClip(image_path, duration=audio_clip.duration)
    
    video_clip = image_clip.with_audio(audio_clip)


    output_dir = pathlib.Path("./temp/video")
    output_dir.mkdir(parents=True, exist_ok=True)

    
    output_path = output_dir / output_filename
    video_clip.write_videofile(
        str(output_path),
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"動画を保存しました: {output_path}")
    
    # メモリ解放
    video_clip.close()
    audio_clip.close()
    image_clip.close()

def create_all_videos():
    """全ての画像と音声から動画を作成"""

    file_list = sorted(os.listdir("./temp/cv"))

    for filename in file_list:
        filename = filename.replace(".wav", "")
        create_video(
            image_path=f"./temp/key/{filename}.png",
            audio_path=f"./temp/cv/{filename}.wav",
            output_filename=f"{filename}.mp4"
        )

def merge_videos():
    """全ての動画を結合"""

    from moviepy import concatenate_videoclips

    video_clips = []
    for filename in sorted(os.listdir("./temp/video")):
        if filename.endswith(".mp4"):
            video_clips.append(VideoFileClip(f"./temp/video/{filename}"))

    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile("./temp/merged_video.mp4", codec='libx264', audio_codec='aac')
    final_clip.close()


def add_bgm():
    """動画にBGMを追加"""

    bgm_path = sorted(os.listdir("./temp/bgm"))[0]
    bgm_path = f"./temp/bgm/{bgm_path}"
    print(f"BGMファイル: {bgm_path}")
    video_path = "./temp/merged_video.mp4"
    
    video_clip = VideoFileClip(video_path)
    bgm_clip = AudioFileClip(bgm_path)

    video_duration = video_clip.duration
    bgm_duration = bgm_clip.duration

    if bgm_duration < video_duration:
        loop_count = int(video_duration / bgm_duration) + 1
        bgm_clips = [bgm_clip] * loop_count
        bgm_clip = concatenate_audioclips(bgm_clips)

    bgm_clip = bgm_clip.with_duration(video_clip.duration)

    final_audio = CompositeAudioClip([video_clip.audio, bgm_clip.with_volume_scaled(0.3)])
    
    final_video = video_clip.with_audio(final_audio)
    
    final_video.write_videofile(
        "./temp/final_video_with_bgm.mp4",
        codec='libx264',
        audio_codec='aac'
    )
    
    final_video.close()
    video_clip.close()
    bgm_clip.close()

def finally_create_video():
    """全ての動画を作成し、BGMを追加"""

    create_all_videos()
    merge_videos()
    add_bgm()
    print("動画の作成が完了しました")


if __name__ == "__main__":
    finally_create_video()