import json
import openai

# Set up OpenAI API key
openai.api_key = "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"  
# Preprocess text to handle special characters and long inputs
def preprocess_text(text):
    """
    Clean and preprocess the input text:
    - Remove unsupported characters.
    - Trim excessive length if necessary.
    """
    # Clean and remove unsupported characters
    clean_text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore').strip()
    # Truncate text if it's too long (OpenAI recommends < 2000 characters for good performance)
    return clean_text[:2000]

# Function to analyze sentiment and aspects using OpenAI API
def analyze_text(text, is_reply=False):
    """
    Call OpenAI API with a tailored prompt for sentiment analysis and summarization.
    """
    prompt = f"""
    You are an expert in text analysis and sentiment classification. Your task is to analyze YouTube comments and their replies. For each comment or reply, perform the following tasks:
    
    1. **Summarize** the comment.
    2. Identify the **overall sentiment** of the comment text as "Positive," "Negative," or "Neutral."
    3. For reply text, extract **key aspects** or main ideas (e.g., keywords reply text).
    4. Identify the **sentiment** of the reply text as "Positive," "Negative," or "Neutral."

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
        print("API Response:", response)  # Debugging: Print raw API response
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Error during API call:", e)  # Debugging: Print exception details
        # Return a placeholder error in the expected format
        return "- Comment-summary: error\n- Overall-sentiment: error" if not is_reply else "- Reply-aspects: error\n- Reply-sentiment: error"

# Load the input JSON file with UTF-8 encoding
with open("demo.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Process the JSON structure
output_data = []
for video in data:
    video_result = {
        "videoTitle": video["title"],
        "videoID": video["videoID"],
        "comments": []
    }
    for comment in video["comments"]:
        # Preprocess and analyze the main comment
        comment_response = analyze_text(preprocess_text(comment["text"]))
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
        # Preprocess and analyze each reply
        reply_response = analyze_text(preprocess_text(reply["text"]), is_reply=True)
        reply_result = {
            "author": reply["author"],
            "text": reply["text"],
            "reply-aspects": "",
            "sentiments": ""
        }

        # Debugging: Print raw reply response
        print(f"Reply Response for '{reply['text']}': {reply_response}")

        # Parse AI response for the reply
        for line in reply_response.split("\n"):
            if "Reply-aspects:" in line:
                reply_result["reply-aspects"] = line.split(":")[1].strip() if ":" in line else "N/A"
            elif "Reply-sentiment:" in line:
                reply_result["sentiments"] = line.split(":")[1].strip() if ":" in line else "N/A"

        # Handle missing or blank results
        if not reply_result["reply-aspects"]:
            reply_result["reply-aspects"] = "No key aspects identified"
        if not reply_result["sentiments"]:
            reply_result["sentiments"] = "No sentiment identified"

        # Log issues for problematic replies
        if not reply_result["reply-aspects"] or not reply_result["sentiments"]:
            print(f"Issue with reply: {reply['text']}")

        comment_result["replies"].append(reply_result)


        video_result["comments"].append(comment_result)
    output_data.append(video_result)

# Save the processed data to a new JSON file
with open("processed_vaccine_comments1.json", "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

print("Processing complete. Results saved to 'processed_vaccine_comments1.json'.")
