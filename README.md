## Research Project for The New Geography for Information Age Course
_Pravin Patel and Shweata Hegde_

We are interested in looking at discourse around vaccines on YouTube. YouTube has become a go-to place to get any information. We would like to examine the nature of videos on vaccines, the emotional response to the video in the Comments section, and the dynamics of the conversations in Comment Threads.

### Scripts

We use YouTube API v3 to fetch videos, comments and comment threads. To run, `get_comments.py`:
- Create YouTube API Key
- Store it in constants.py
- Feed the API key variable name to `get_comments.py`
- Give query, max results to `make_mega_dict` function