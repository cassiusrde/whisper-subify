import pysubs2

from src.utils import get_logger, init_logger
_logger = get_logger()

def save_subs(result, file_path):
    subs = pysubs2.SSAFile()
    subs = pysubs2.load_from_whisper(result)
    subs.save(file_path)

def merge_subtitles(subtitle_segments, output_path, delete_duplicates):
    
    merged_subtitles = []

    # The real split position is the middle of current segment end and next segment start.
    real_segments = []
    for i in range(len(subtitle_segments)):
        if (i + 1) == len(subtitle_segments):
            segment_end = subtitle_segments[i][2]
        else:
            segment_end = (subtitle_segments[i][2] + subtitle_segments[i + 1][1]) // 2

        if i == 0:
            segment_start = subtitle_segments[i][1]
        else:
            segment_start = (subtitle_segments[i][1] + subtitle_segments[i - 1][2]) // 2

        real_segments.append((segment_start, segment_end))
   
    
    for (subtitle_path, segment_start, segment_end), (valid_start, valid_end) in zip(subtitle_segments, real_segments):
        _logger.info("Merging subtitle %s into %s, used segment: %d - %d",
                     subtitle_path, output_path, valid_start, valid_end)
        subtitle = pysubs2.load(subtitle_path, encoding="utf-8")
           
        for sub in subtitle:
            start_in_seconds = sub.start / 1000 + segment_start
            if not valid_start <= start_in_seconds < valid_end:
                continue
            sub.shift(s=segment_start)
            
            _logger.debug("%s", str(sub))
            
            merged_subtitles.append(sub)
        
    # Delete consecutive duplicate subtitles.
    merged_subtitles_wo_duplicates = []
    i, j = 0, 0

    while i < len(merged_subtitles):
        j = i + 1

        while j < len(merged_subtitles) and merged_subtitles[i].text == merged_subtitles[j].text:
            j += 1

        if j - i >= delete_duplicates:
            # More than delete_duplicates subtitles are same. Something must be wrong.
            # Throw away all of them.
            _logger.info("%d subtitles are same. Deleted: %s", j - i, merged_subtitles[i].text)
        else:
            merged_subtitles_wo_duplicates.extend(merged_subtitles[i:j])
        i = j

    subs = pysubs2.SSAFile()
    subs.events = merged_subtitles_wo_duplicates
    subs.sort()
    subs.save(output_path)
