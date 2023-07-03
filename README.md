## Requirements
Ensure you have the following:
- Python (add any packages using pip install packagename)
- Discord
  - Access to our server (link provided in Canvas)
  - Our application key (reach out if you need access)
- Cloned code from this repository

## Running the Bot
Ensure you have done the following:
- Include the application key in line 22.
- Compiled/Run the python code.
  - python3 botmod.py
  - You should see a message in your terminal that lets you know if the connection was successful.
- Enter into the Discord App.
- Go to the channel and use the commands below.

## Interacting with Pericles
- @Pericles: Will cause Pericles to respond with a list of commands.
- !merit: Will display the current user's merit score.
- !leaderboard: Will display the merit leaders for the server.
- !reset_merit: Will reset the global merit scores (Moderator Only)
- ANY message containing profanity will be blocked by the bot.
- Block spamming and punish repeated offenders.

## Running the bot on your own server!
- Sign-in to Discord on https://discord.com/developers/applications
- Click 'New Application' at the Top Right
- Name it whatever you would like and click 'Create'
- Click 'OAuth2' then under 'Authorization Method' choose 'In-app Application'
- Then click 'bot' from the scopes menu that appears below
- The permissions that appear below are up to the user, but we had all Text Permissions Checked, as well as a 'Moderate Members', 'View Server Insights', 'Mute Members' selected as well.
- Save all changes then under 'URL Generator' choose 'bot' in the Scopes menu
- Choose the same permissions as above again.
- Copy the invite link and save it to file. We will come back to this link later. This link invites the bot to the server.
- Go to 'Bot' menu. Click 'Reset Token' and 'Yes, do it!'
- Copy this token to the same file as before and make sure to mention that this is the bots token so the two do not get mixed up.
- Create a Folder in your Desktop called 'Discord_Bot'
- In your browser, paste the link from earlier to invite your bot. Choose a Server that you have persmission to grant it access. (It would be best to create your own server to test your bot on!)
- Create a file called 'botmod.py'inside the directory 'Discord_Bot'
- In your terminal run 'ip install discord'
- Experiment with the lines of code from our 'botmod.py' file. Simply include line 1 and lines 44-46 from botmod.py in your created file. run python3 botmod.py from your created folder and you will see your bot is online! From there, the rest is entirely up to the user on what they want to include!
