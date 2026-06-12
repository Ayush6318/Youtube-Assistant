from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def get_video_id(url):
    parsed_url = urlparse(url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path[1:]

    if "youtube.com" in parsed_url.netloc:
        query = parse_qs(parsed_url.query)

        if "v" in query:
            return query["v"][0]

    raise ValueError("Invalid YouTube URL")


def get_transcript(video_id):

    languages_to_try = [
        ['en'],
        ['hi'],
        ['en', 'hi']
    ]

    last_error = None

    for langs in languages_to_try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=langs
            )

            text = " ".join(
                chunk["text"]
                for chunk in transcript
            )

            if text.strip():
                return text

        except Exception as e:
            last_error = e

    raise Exception(
        f"Transcript unavailable for this video.\n{str(last_error)}"
    )