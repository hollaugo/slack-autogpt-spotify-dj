# Slack Spotify AutoGPT Bot
This repository contains the code for a Slack bot that interacts with the Spotify API, the bot is able to take prompts and perform various Spotify related tasks such as, suggesting music, creating playlists, answering questions of about music.


## Prerequisites
- Python 3.6+
- A Slack account with bot permissions
- OpenAI API key
- Spotify Credentials: Spotify Client ID, Spotify Client Secret and Redirect URI


### Installation 
- Clone file 
`git clone https://github.com/hollaugo/slack-autogpt-spotify-dj`
- Install the required packages.
`pip install -r requirements.txt`
- Set up Oauth for Spotify: https://developer.spotify.com/documentation/web-api/tutorials/code-flow

- Run the Slack bot
`python slack_bot.py`

## Features 
- Use bot to perform a combination of tasks through Spotify API requests 
- Ask questions about songs 
- Create playlists 
- Add songs to playlists 
- Search for songs by popularity and other characteristics 
