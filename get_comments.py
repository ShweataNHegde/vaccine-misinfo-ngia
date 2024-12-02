import constants
import googleapiclient.discovery
import json
from pprint import pprint

API_KEY = constants.PRAVIN_API_KEY
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Get list of YouTube Videos
def get_videos(query, max_results=2):
    request = youtube.search().list(part="snippet", q=query,maxResults=max_results).execute()
    video_data = []
    for item in request['items']:
        each_video_info = {
            'title': item['snippet']['title'],
            'channelTitle': item['snippet']['channelTitle'],
            'publishedAt': item['snippet']['publishedAt'],
            'videoID': item['id']['videoId']
        }
        video_data.append(each_video_info)
    print("fetched videos")
    return video_data

# Get comments for a specific video
def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Adjust as needed
    )

    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
# Include the comment ID in the dictionary
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'id': item['snippet']['topLevelComment']['id'],
                'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount'] # Add this line to store the comment ID
            })

        request = youtube.commentThreads().list_next(request, response)
    comments.sort(key=lambda x: x['likeCount'], reverse=True)
    pprint("fetched comments")
    return comments

# Get replies to a comment
def get_replies(comment_id):
    replies = []
    request = youtube.comments().list(
        part='snippet',
        parentId=comment_id,
        textFormat='plainText',
        maxResults=100  # Adjust as needed
    )

    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']
            replies.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay']
            })

        request = youtube.comments().list_next(request, response)
    print("fetched replies")

    return replies


def make_mega_dict(query):

  video_list = get_videos(query)
  for video in video_list: 
    video['comments']= get_comments(video['videoID'])
    for comment in video['comments'][:100]:
      comment['replies'] = get_replies(comment['id'])  # Pass comment ID directly
  return video_list

def main():
    video_list = make_mega_dict("rare side effects of covishield")
    with open("rare_side_effects_covishield.json", "w") as outfile:
        json.dump(video_list, outfile, indent=4, sort_keys=False)

if __name__ == "__main__":
    main()
