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

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id,languages=['en','hi'])

        text = " ".join(
            [chunk.text for chunk in transcript]
        )

        return text

    except Exception as e:
        raise Exception(
            f"Transcript could not be retrieved.\n{str(e)}"
        )