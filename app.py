print('APP.PY LOADED')

from utils.youtube_loader import (
    get_video_id,
    get_transcript
)

from utils.text_splitter import (
    split_text
)

from chains.summary_chain import (
    generate_summary
)

url = input(
    "Enter YouTube URL: "
)

video_id = get_video_id(url)

transcript = get_transcript(
    video_id
)

docs = split_text(transcript)

full_text = ""

for doc in docs:
    full_text += doc.page_content

summary = generate_summary(
    docs
)

print("\nSUMMARY\n")

print(summary)