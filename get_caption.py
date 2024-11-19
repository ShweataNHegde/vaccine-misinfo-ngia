from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_caption_as_text(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    text_formatted_transcript = formatter.format_transcript(transcript)
    return text_formatted_transcript

def write_to_text_file(text_formatted_transcript, name_of_file):
    with open(name_of_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_formatted_transcript)
        print(f"caption written to: {name_of_file}")

def main():
    text_formatted_transcript = get_caption_as_text('zBkVCpbNnkU')
    write_to_text_file(text_formatted_transcript, "example-caption.txt")
    
if __name__ == "__main__":
    main()