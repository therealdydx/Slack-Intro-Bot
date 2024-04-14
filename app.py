import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'  # denote where it goes to
load_dotenv(dotenv_path=env_path)  # loading env file

# get the relevant information needed for API
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
signing_secret = os.environ["SLACK_SIGNING_SECRET"]
state = str(uuid4())

# get the scopes needed for this app
oauth_scope = ", ".join(["chat:write", "channels:read", "groups:read"])

# create a dictionary to represent a database to store our token + initialise the app
token_database = {}
global_token = ""
app = Flask(__name__)

# route to kick off Oauth flow
@app.route("/begin_auth", methods=["GET"])
def pre_install():
    return f'<a href="https://slack.com/oauth/v2/authorize?scope={ oauth_scope }&client_id={ client_id }&state={state}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'

# route for OAuth flow to redirect to after user accepts scopes
@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():   
    # retrieve the auth code and state from the request params
    auth_code = request.args["code"]
    received_state = request.args["state"]

    # Token is not required to call the oauth.v2.access method
    client = slack.WebClient()
    # verify state received in params matches state we originally sent in auth request
    if received_state == state:
        # Exchange the authorization code for an access token with Slack
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )
    else:
        return "Invalid State"

    # save the bot token and teamID - aka workspace ID - to a database
    teamID = response["team"]["id"]
    token_database[teamID] = response["access_token"]

    # Also save the bot token in a global variable so don't need lookup on each WebClient call
    global global_token
    global_token = response["access_token"]
    return "Auth complete!"

# now checking for the event - aka member joined channel
slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", app)

# create an event listener for "member_joined_channel" events and sends message
@slack_events_adapter.on("member_joined_channel")
def member_joined_channel(payload):

    user = payload["event"]["user"]
    channelID = payload["event"]["channel"]
    teamID = payload["team_id"]

    # look up token in database
    token = token_database[teamID]

    # if the app doesn't actually have access to the OAuth token
    if token is None:
        print("ERROR: Authenticate the App!")
        return
    else:
        client = slack.WebClient(token=token)    
        # now print out the message
        client.chat_postMessage(channel=channelID, 
        text="Please give a warm welcome to <@" + user + ">! Would you mind also introducing yourself? We would love to get to know you! :tada::wave:")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

