# -*- coding: utf-8 -*-
# Author Name: Cassius Estrada
# Author Email: cassiusrde@gmail.com
# Author GitHub username: cassiusrde

import argparse
from pathlib import Path

from src.utils import init_logger
from src.transcribe import transcribe_media

def main():
    init_logger()

    parser = argparse.ArgumentParser("Gerate srt subtitles from movies files.")
    parser.add_argument("input", type=str, help="Path to movie file to be processed.")
    parser.add_argument("--output", "-o", type=str, default="outputs", help="Path to output directory.")
    parser.add_argument("--segment", "-s", type=int, default=600, help="Length of each segments in seconds.")
    parser.add_argument("--overlap", "-lap", type=int, default=60, help="Length of overlap between segments in seconds.")
    parser.add_argument("--delete-duplicates", type=int, default=3,
                        help="Number of consecutive duplicate subtitles to delete. "
                             "Useful for removing false positive of silence. Setting to 0 to disable.")
    parser.add_argument("--reuse", default=False, action="store_true", help="Whether to reuse existing files.")
    parser.add_argument("--translate", default="pt", type=str, help="Translation to language")
    args = parser.parse_args()

    movie_path = args.input
    if not Path(movie_path).exists():
        raise ValueError(f"Input file {movie_path} does not exist.")
    if args.segment < 10:
        raise ValueError("segment must be at least 10 seconds.")
    if args.overlap < 0 or args.overlap >= args.segment:
        raise ValueError("overlap must be at least 0 and less than segment.")
    if args.delete_duplicates <= 1:
        raise ValueError("delete_duplicates must be at least 2 or zero.")
    
    main_directory = args.output
    Path(main_directory).mkdir(parents=True, exist_ok=True)

    transcribe_media(movie_path, main_directory,
                    args.segment, args.overlap, 
                    args.delete_duplicates, args.reuse,
                    args.translate)


if __name__ == "__main__":
   main()