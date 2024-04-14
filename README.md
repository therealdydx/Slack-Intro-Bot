# Slack Intro Bot

Very useful guide here:

https://github.com/MaayanLab/slackbot-tutorial

https://github.com/stevengill/slack-python-oauth-example/blob/master/app.py



### What this is:

A bot that automatically sends a templated message when someone new joins the Slack Channel



### How to setup:

1. Go to api.slack.com > create a new app
2. Go to OAuth and Permissions
   - Go to Scopes
   - Add:
     - channels:history
     - chat:write
     - chat:commands
     - im:history
   - In Bot Token Scopes
3. Go back to Basic Information
   - Copy
     - Client ID
     - Client Secret
     - Signing Secret
   - You will need these to update the .env
4. Go to .env file in the repo
   - Update with the three keys you just copied
5. If you are using ngrok or have a link or something
   - Go to OAuth and Permissions
     - Go to Redirect URLs
     - Add your URL into there
     - Remember! When you want to add the bot, you have to use link/begin_auth, not just link
       - You will see a button Add to Slack where you can click on it and it will add the bot to your system
6. There is a dockerfile which you can just upload the whole thing to your deployment server, or if you are using localhost you can just run using docker compose up
7. Enjoy! Your bot will now trigger a message for every new joiner to the channel!