## Research Project for The New Geography for Information Age Course
_Pravin Patil and Shweata Hegde_

We are interested in looking at discourse around vaccines on YouTube. YouTube has become a go-to place to get any information. We would like to examine the nature of videos on vaccines, the emotional response to the video in the Comments section, and the dynamics of the conversations in Comment Threads.

### Scripts

We use YouTube API v3 to fetch videos, comments and comment threads. To run, `get_comments.py`:
- Create YouTube API Key
- Store it in constants.py
- Feed the API key variable name to `get_comments.py`
- Give query, max results to `make_mega_dict` function

JSON output: 
```
[
    {
        "title": "How do vaccines work? - Kelwalin Dhanasarnsombut",
        "channelTitle": "TED-Ed",
        "publishedAt": "2015-01-12T16:05:47Z",
        "videoID": "rb7TVW77ZCs",
        "comments": [
            {
                "author": "@KikiCooking-plus",
                "text": "<a href=\"https://www.youtube.com/watch?v=rb7TVW77ZCs&amp;t=65\">1:05</a> FRENCH FRIES",
                "id": "UgyPPNH0vueTrEPZDxd4AaABAg",
                "replies": []
            },
            {
                "author": "@Zanemehgameyt",
                "text": "People watching this after getting vaccinated<br>\ud83d\udc47",
                "id": "Ugysnx-Gg19EKQNeNCp4AaABAg",
                "replies": []
            }

    }
]
```