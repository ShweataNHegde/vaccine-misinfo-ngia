import json
import matplotlib.pyplot as plt

def create_pie_chart(data, title, filename=None):
    """
    Creates a pie chart from the provided data. 
    Optionally saves it to a file if a filename is provided.
    """
    labels = data.keys()
    sizes = data.values()
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    if filename:
        plt.savefig(filename)  # Save the chart as an image file
        plt.close()  # Close the plot after saving
    else:
        plt.show()  # Display the chart if no filename is provided

# Load JSON file
file_path = 'sentiment.json'
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Initialize counters
emotions_count = {}
sentiments_count = {}
vaccination_views_count = {}

# Process JSON data
for item in json_data:
    if 'comments' in item:
        for comment in item['comments']:
            for reply in comment.get('replies', []):
                sentiment_data = reply.get("sentiment", {})
                emotion = sentiment_data.get("emotions", "Unclear")
                sentiment = sentiment_data.get("sentiments", "Unclear")
                vaccination_view = sentiment_data.get("vaccinationView", "Unclear")

                emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
                sentiments_count[sentiment] = sentiments_count.get(sentiment, 0) + 1
                vaccination_views_count[vaccination_view] = vaccination_views_count.get(vaccination_view, 0) + 1

# Create pie charts and save as images
create_pie_chart(emotions_count, "Distribution of Emotions", "emotions_chart.png")
create_pie_chart(sentiments_count, "Distribution of Sentiments", "sentiments_chart.png")
create_pie_chart(vaccination_views_count, "Distribution of Vaccination Views", "vaccination_views_chart.png")


#world cloud

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

def generate_wordcloud(text, title, filename=None):
    """Generates and displays or saves a word cloud from the provided text."""
    wordcloud = WordCloud(
        width=800, height=400, background_color='white', colormap='viridis'
    ).generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

# Load JSON file
file_path = 'Covaxin_sentiment.json'
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Collect all 'aspect' text for word cloud, excluding specific words
excluded_words = {"comment", "unclear","comment" "general"}
aspects_text = ""

for item in json_data:
    if 'comments' in item:
        for comment in item['comments']:
            for reply in comment.get('replies', []):
                sentiment_data = reply.get("sentiment", {})
                aspect = sentiment_data.get("aspect", "").lower()  # Normalize case
                if aspect and aspect not in excluded_words:  # Exclude specified words
                    aspects_text += f"{aspect} "

# Generate the word cloud for filtered aspects
generate_wordcloud(aspects_text, "Word Cloud of Aspects", "aspects_wordcloud_filtered.png")



#data table


import json
import pandas as pd

def create_table(data, title):
    """
    Creates a pandas DataFrame from the provided data and prints it.

    Args:
        data: A dictionary where keys are labels and values are counts.
        title: The title of the table.
    """
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Count'])
    df.index.name = 'Category'
    print(f"\n{title}\n")
    print(df)

# Load JSON file
file_path = 'sentiment.json'
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Initialize counters
emotions_count = {}
sentiments_count = {}
vaccination_views_count = {}

# Process JSON data
for item in json_data:
    if 'comments' in item:
        for comment in item['comments']:
            for reply in comment.get('replies', []):
                sentiment_data = reply.get("sentiment", {})
                emotion = sentiment_data.get("emotions", "Unclear")
                sentiment = sentiment_data.get("sentiments", "Unclear")
                vaccination_view = sentiment_data.get("vaccinationView", "Unclear")

                emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
                sentiments_count[sentiment] = sentiments_count.get(sentiment, 0) + 1
                vaccination_views_count[vaccination_view] = vaccination_views_count.get(vaccination_view, 0) + 1

# Create tables
create_table(emotions_count, "Distribution of Emotions")
create_table(sentiments_count, "Distribution of Sentiments")
create_table(vaccination_views_count, "Distribution of Vaccination Views")


import json
import csv

def create_table(data, filename):
    """
    Creates a CSV table from the provided data.

    Args:
        data: A dictionary where keys are labels and values are counts.
        filename: The name of the CSV file to save the table to.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Category', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for category, count in data.items():
            writer.writerow({'Category': category, 'Count': count})

# Load JSON file
file_path = 'sentiment.json'
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Initialize counters
emotions_count = {}
sentiments_count = {}
vaccination_views_count = {}

# Process JSON data
for item in json_data:
    if 'comments' in item:
        for comment in item['comments']:
            for reply in comment.get('replies', []):
                sentiment_data = reply.get("sentiment", {})
                emotion = sentiment_data.get("emotions", "Unclear")
                sentiment = sentiment_data.get("sentiments", "Unclear")
                vaccination_view = sentiment_data.get("vaccinationView", "Unclear")

                emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
                sentiments_count[sentiment] = sentiments_count.get(sentiment, 0) + 1
                vaccination_views_count[vaccination_view] = vaccination_views_count.get(vaccination_view, 0) + 1

# Create CSV tables
create_table(emotions_count, "emotions_table.csv")
create_table(sentiments_count, "sentiments_table.csv")
create_table(vaccination_views_count, "vaccination_views_table.csv")