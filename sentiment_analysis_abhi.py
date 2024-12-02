from openai import OpenAI
import openai
import json
import pandas as pd
# Set your OpenAI API key
openai.api_key = ""  # Replace with your actual API key
client = OpenAI(api_key=openai.api_key) 

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text using OpenAI's GPT models.

    Args:
        text: The text to analyze.

    Returns:
        The sentiment of the text, either "Positive", "Negative", or "Neutral".
    """

    prompt = f"What is the sentiment of this text: {text}"
    print(prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that performs sentiment analysis."},
                {"role": "user", "content": prompt}
            ]
        )

        sentiment_analysis = response.choices[0].message.content
        return sentiment_analysis.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"

def process_json_file(file_path):
    """
    Reads a JSON file, analyzes the sentiment of each text entry, and writes the results to a new file.

    Args:
        file_path: The path to the JSON file.
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding to handle potential character encoding issues
            data = json.load(file)
            comment1=data[0]["comments"][0]
            comment_text=comment1['text']
            sentiment_comment=analyze_sentiment(comment_text)
            data[0]["comments"][0]["comment_summary"]=sentiment_comment
            print(data)
        results = []
        for reply in comment1[0]['replies']:
            text1=reply['text']
            sentiment_reply = analyze_sentiment(text1)
            results.append({
                "id": entry['id'],
                "text": entry['text'],
                "sentiment": sentiment
            })

        output_file = "sentiment_results.json"
        with open(output_file, 'w', encoding='utf-8') as file:  # Specify encoding for output file
            json.dump(results, file, indent=4)

        print(f"Sentiment analysis completed. Results saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    input_file = "demo.json"  # Replace with your actual file path
    process_json_file(input_file)