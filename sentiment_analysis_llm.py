from pydantic import BaseModel
from openai import OpenAI
import json
from pprint import pprint
client = OpenAI(api_key=constants.LLM_KEY)
import constants

prompt = """
You are a helpful aspect-based sentiment analyzer assistant. You will given a comment taken from videos about vaccination. 
Your task for a given text is to:
- label the aspects.
- label the sentiment as Positive, Negative or Neutral
- label the emotions as Happiness, Sadness, Fear, Anger, Surprise and Disgust. If emotion is unclear, please mention Unclear.
- label the comments as pro-vaccine or anti-vaccine. If unclear, mention Unclear

Here is an example: 
Swelling in the brain is a lot worse than 2 weeks of a 'bad cold'
Aspect: vaccine side effects
Sentiment: Negative
Emotion: Fear
VaccinationView: anti-vaccine
"""

class sentimentDict(BaseModel):
    aspect: str
    sentiments: str
    emotions: str
    vaccinationView: str

def analyse_sentiment(text):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content":text},
        ],
        temperature=0,
        response_format=sentimentDict,
    )
    return completion.choices[0].message.parsed

def load_json_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        # Load the entire JSON file as a single object
        data = json.load(f)
        return data

data = load_json_file('comments/small-json.json')
for comment in data['comments']:
    data["sentiment"] = dict(analyse_sentiment(comment['text']))
    
    for reply in comment['replies']:
        reply["sentiment"] = dict(analyse_sentiment(reply['text']))

pprint(data)