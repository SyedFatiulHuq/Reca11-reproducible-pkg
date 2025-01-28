import re
import webvtt


class SpeechSegment:
    def __init__(self, start_time, end_time, speaker, text):
        self.start_time = start_time  # String representing the start time
        self.end_time = end_time  # String representing the end time
        self.speaker = speaker  # String representing the speaker's name
        self.text = text  # String representing the spoken text

    def __str__(self):
        return f"{self.start_time} --> {self.end_time} {self.speaker}: {self.text}\n"


def get_bulk_text(segments):
    bulk_text = ""
    for segment in segments:
        bulk_text += str(segment)

    return bulk_text


def extract_segments_from_transcript(filepath):
    segments = []
    last_speaker = ""

    for caption in webvtt.read(filepath):

        # Separate the captions into a start and end time
        start_time = caption.start
        end_time = caption.end

        # Remove any content within < > tags (YouTube formatting)
        raw_text = caption.raw_text
        pattern = re.compile(r'<.*?>')
        raw_text = re.sub(pattern, '', raw_text)

        # Pull the speaker out of the caption text
        if raw_text and ":" in raw_text:
            speaker_text = raw_text.split(":", 1)
            current_text = speaker_text[1]
            last_speaker = speaker_text[0]
        else:
            current_text = raw_text

        segment = SpeechSegment(start_time, end_time, last_speaker, current_text.strip())
        segments.append(segment)

    return segments
