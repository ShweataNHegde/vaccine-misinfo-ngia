import json
from pprint import pprint
with open('vaccine_01.json', 'r') as file:
    data = json.load(file)

for item in data:
    for comment in item['comments']:
        print(comment['likeCount'])