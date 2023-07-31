from pathlib import Path
from moviepy.editor import VideoFileClip
from ffprobe import FFProbe
import whisper

from src.audio import extract_audio, segment_audio
from src.subtitles import save_subs, merge_subtitles
from src.translate import translate_subs
from src.utils import get_logger, init_logger

_logger = get_logger()

def is_video_file(movie_path) -> False:
    if len(FFProbe(movie_path).video) > 0:
        return True
    else:
        return False

def detect_language(model, audio_path):    
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    _logger.info(f"Detected language: {max(probs, key=probs.get)}")
    return max(probs, key=probs.get)

def speech_to_text(model, audio_path, language="pt"):
    options = dict(language=language)
    transcribe_options = dict(task="transcribe", **options)
    result = model.transcribe(audio_path, **transcribe_options)
    return result['segments']

def transcribe_media(video_path: str, main_directory: str,
                          segment_length: int, overlap: int,
                          delete_duplicates: int, reuse: bool, translate: str) -> None:

    if is_video_file(video_path) == False:
        _logger.info("File format invalid: %s", video_path)
        raise RuntimeError("File format invalid")
        
    audio_path = extract_audio(video_path, main_directory)
   
    model = whisper.load_model("large")
    _logger.info("Whisper large model loaded")

    language = detect_language(model, audio_path)
    
    #translations: List[Tuple[Path, int, int]] = []
    translations = []

    for segment_path, start, end in segment_audio(audio_path, main_directory, segment_length, overlap, reuse):
        srt_path = Path(f"{main_directory}/{start:05d}-{end:05d}.srt")
        _logger.info("Using whisper to translate %s", segment_path)
        response = speech_to_text(model, segment_path, language)

        save_subs(response, srt_path)
        _logger.info("Translation saved: %s", srt_path)
        
        translations.append((srt_path, start, end))
   
    merge_path = f"{main_directory}/{Path(video_path).stem}.srt"
    _logger.info("Merging subtitles into %s", merge_path)
    merge_subtitles(translations, merge_path, delete_duplicates)

    if (translate != '') and (language != translate):
        out_path = merge_path.replace('.srt', f'-{translate}.srt')
        _logger.info("Translate srt from %s from %s", language, translate)
        translate_subs(merge_path, out_path, language, translate)
    else:
        out_path = merge_path
    
    """
    clean_temp_files(main_directory, out_path)
    """
    
if __name__ == "__main__":
    init_logger()

    movie_path = "c:/Storage/naruto.mp4"
    main_directory = "./out"
    #main_directory.mkdir(parents=True, exist_ok=True)
    segment = 60
    overlap = 10
    delete_duplicates = 3
    reuse = False
    translate = 'pt'
    
    transcribe_media(movie_path, main_directory,
                    segment, overlap, delete_duplicates, reuse, translate)