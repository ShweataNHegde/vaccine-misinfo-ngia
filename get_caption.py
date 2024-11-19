from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

transcript = YouTubeTranscriptApi.get_transcript('zBkVCpbNnkU')

formatter = TextFormatter()

# .format_transcript(transcript) turns the transcript into a JSON string.
text_formatted_transcript = formatter.format_transcript(transcript)

with open('example-transcript.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(text_formatted_transcript)