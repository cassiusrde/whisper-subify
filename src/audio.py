
from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path

from src.utils import get_logger, init_logger
_logger = get_logger()

def extract_audio(video_path, out_directory):
    video = VideoFileClip(video_path)
    audio = video.audio

    audio_path = f"{out_directory}/{Path(video_path).stem}.mp3"
    audio.write_audiofile(audio_path)
    audio.close()
    _logger.info("Audio track saved: %s", audio_path)
    return audio_path

def get_duration(audio):
    _logger.info("Getting duration of audio file %s", audio.filename)
    return float(audio.duration)

def clip_audio(audio, start, end, output_path):    
    _logger.info("Clipping audio file %s from %d to %d and saving to %s",
                 audio.filename, start, end, output_path)
    
    clip = audio.subclip(t_start=start, t_end=end)
    clip.write_audiofile(output_path)
    clip.close()
  
    _logger.info("Audio segment saved: %s", output_path)


def segment_audio(audio_path, output_directory,
                  segment_length, overlap, reuse):
   
    _logger.info("Segmenting audio file %s into segments of length %d with overlap %d",
                 audio_path, segment_length, overlap)
       
    audio = AudioFileClip(audio_path)

    duration = get_duration(audio)
    _logger.info("Duration of audio file: %f seconds", duration)

    #segments: List[Tuple[Path, int, int]] = []
    segments = []

    start = 0
    while start < duration:
        end = start + segment_length
        if end > duration:
            end = int(duration)
        output_path = f"{output_directory}/{start:05d}-{end:05d}.wav"

        if reuse and output_path.exists():
            _logger.info('Reuse generated audio: %s', output_path)
        else:
            clip_audio(audio, start, end, output_path)

        segments.append((output_path, start, end))
        
        if end >= duration:
            break
        start += segment_length - overlap

    return segments
