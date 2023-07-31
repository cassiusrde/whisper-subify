# Whisper-Subify

Generate subtitles for long movies with OpenAI Whisper Model.

This tool is built upon OpenAI Whisper. Although Whisper is a powerful speech-to-text tool, it don't support long files (>25MB), which is a problem for transcription of movies, TV shows, podcasts, and anything longer than a couple of minutes.

## Whisper

Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. Trained on 680k hours of labelled data, Whisper models demonstrate a strong ability to generalise to many datasets and domains without the need for fine-tuning.

Whisper was proposed in the paper [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) by Alec Radford et al from OpenAI. The original code repository can be found [here](https://github.com/openai/whisper).

## Features and TODOs

- [x] Support transcription very long / large media files.
- [x] Support pure transcription (without translation).
- [x] Auto-translate to other languages with Google translate.
- [ ] Improve synchrony.
- [ ] Multi-thread process.
- [ ] Suport OpenAI translator.
- [ ] Docker format.

## Requirements

* Python 3.10+

## Install

Clone this repository and run:

```
pip install -r requirements.txt
```

You can upgrade whisper model to the latest version with:

```
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```

After upgrading, calling whisper.load_model("large") will load the new [large-v2 model](https://github.com/openai/whisper/discussions/661).

## Run the code

```
python run.py <path_to_video> -o <path_to_output> --translate <language>
```

Languages are given in format [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

## Exemple
```
python run.py /path/to/movie.mp4 -o ./output/ --translate pt
```

See `python run.py -h` for more command line options.
