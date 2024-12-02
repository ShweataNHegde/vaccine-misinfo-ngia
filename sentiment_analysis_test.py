from openai import OpenAI
import json
import openai

# Set up OpenAI API key
#openai.api_key = ""

# Load the input JSON file with explicit UTF-8 encoding
with open("demo.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Function to analyze sentiment and aspects using the given prompt
def analyze_text(text, is_reply=False):
    prompt = f"""
    You are an expert in text analysis and sentiment classification. Your task is to analyze YouTube comments and their replies. For each comment or reply, perform the following tasks:
    
    1. **Summarize** the comment in one concise sentence.
    2. Identify the **overall sentiment** of the text as "Positive," "Negative," or "Neutral."
    3. For replies, extract **key aspects** or main ideas (e.g., keywords or topics from the text).
    4. Identify the **sentiment** of the reply as "Positive," "Negative," or "Neutral."

    Here is the text to analyze:

    "{text}"

    Respond with the following format:
    - Comment-summary: "<summary>"
    - Overall-sentiment: "<Positive/Negative/Neutral>"
    - Reply-aspects (if applicable): "<comma-separated key aspects>"
    - Reply-sentiment (if applicable): "<Positive/Negative/Neutral>"
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for text analysis and sentiment classification."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Return an error response in the expected string format
        if is_reply:
            return "- Reply-aspects: error\n- Reply-sentiment: error"
        else:
            return "- Comment-summary: error\n- Overall-sentiment: error"

# Process the JSON structure
output_data = []
for video in data:
    video_result = {
        "videoTitle": video["title"],
        "videoID": video["videoID"],
        "comments": []
    }
    for comment in video["comments"]:
        # Analyze main comment
        comment_response = analyze_text(comment["text"])
        comment_result = {
            "commentID": comment["id"],
            "author": comment["author"],
            "text": comment["text"],
            "likeCount": comment.get("likeCount", 0),
            "comment-summary": "",
            "overall-sentiment": "",
            "replies": []
        }

        # Parse AI response for the main comment
        for line in comment_response.split("\n"):
            if "Comment-summary:" in line:
                comment_result["comment-summary"] = line.split(":")[1].strip()
            elif "Overall-sentiment:" in line:
                comment_result["overall-sentiment"] = line.split(":")[1].strip()

        # Process replies if they exist
        if "replies" in comment and isinstance(comment["replies"], list):
            for reply in comment["replies"]:
                reply_response = analyze_text(reply["text"], is_reply=True)
                reply_result = {
                    "author": reply["author"],
                    "text": reply["text"],
                    "reply-aspects": "",
                    "sentiments": ""
                }

                # Parse AI response for the reply
                for line in reply_response.split("\n"):
                    if "Reply-aspects:" in line:
                        reply_result["reply-aspects"] = line.split(":")[1].strip()
                    elif "Reply-sentiment:" in line:
                        reply_result["sentiments"] = line.split(":")[1].strip()

                comment_result["replies"].append(reply_result)

        video_result["comments"].append(comment_result)
    output_data.append(video_result)

# Save the processed data to a new JSON file
with open("processed_vaccine_comments.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print("Processing complete. Results saved to 'processed_vaccine_comments.json'.")
