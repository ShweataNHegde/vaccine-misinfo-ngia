import openai
# Set the API key as an environment variable or pass directly
openai.api_key = "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"  
# Instead of setting it globally, pass it directly to the OpenAI client
from openai import OpenAI
client = OpenAI(api_key=openai.api_key) # Pass the api_key here

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "give me 10 times word apple."
        }
    ]
)

print(completion.choices[0].message)