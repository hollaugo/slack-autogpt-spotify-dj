import os
from dotenv import load_dotenv
import yaml
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
import spotipy.util as util
from langchain.requests import RequestsWrapper
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits.openapi import planner
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

#Load Spotify OpenAPI Specs
with open("openai_openapi.yaml") as f:
    raw_openai_api_spec = yaml.load(f, Loader=yaml.Loader)
openai_api_spec = reduce_openapi_spec(raw_openai_api_spec)

with open("spotify_openapi.yaml") as f:
    raw_spotify_api_spec = yaml.load(f, Loader=yaml.Loader)
spotify_api_spec = reduce_openapi_spec(raw_spotify_api_spec)

# Spotipy Authentication
def construct_spotify_auth_headers(raw_spec: dict):
    scopes = list(raw_spec['components']['securitySchemes']['oauth_2_0']['flows']['authorizationCode']['scopes'].keys())
    access_token = util.prompt_for_user_token(scope=','.join(scopes))
    return {
        'Authorization': f'Bearer {access_token}'
    }

headers = construct_spotify_auth_headers(raw_spotify_api_spec)
requests_wrapper = RequestsWrapper(headers=headers)

# OpenAI Chat Model Initialization
llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)

# OpenAI Agent Initialization
spotify_agent = planner.create_openapi_agent(spotify_api_spec, requests_wrapper, llm)


# Slack App Initialization
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Slack App Event Handlers
@app.message("")
def handle_user_query(body, say, ack):
    ack()
    user_query = body['event']['text']
    
    say("I am working on your command, give me a few seconds...")

    # Get the response from the Spotify agent
    agent_response = spotify_agent.run(user_query)

    # Send the agent response back to the channel where the message was received
    say(agent_response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

