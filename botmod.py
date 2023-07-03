import discord
from discord.ext import commands
import responses
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from profanity import profanity
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

#Add bot key here
load_dotenv()
key = os.environ.get('API_KEY')


# Define anti spam rules
anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
MUTE_ROLE_NAME = "Muted"
MUTE_TIME = 30

Pericles = "Pericles"

# Initialize merit dictionary
merit = {}

with open ("merit.json", "r") as f:
    merit = json.load(f)


temp_mute = {}

# Launch Pericles
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    for guild in client.guilds:
        for member in guild.members:
            merit[member.name] = 0

    # When a user sends a message, Pericles will handle necessary actions
    @client.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            if username not in merit:
                merit[username] = 0

            # Sentiment Analysis
            sentiment = sia.polarity_scores(user_message)["compound"]
            print(f"Sentiment Score: {sentiment}")

            # Automatic profanity filter
            if(profanity.contains_profanity(user_message)):
                await message.delete()
                if user_message[0] == "?":
                    try:
                        await message.author.send("You are not allowed to say that!")
                    except Exception as e:
                        print(e)
                else:
                    await message.channel.send(f"{message.author.mention} you are not allowed to say that!")

                if username in temp_mute:
                    print('in temp_mute')
                else:
                    merit[username] = merit[username] + sentiment
                    merit[username] = round(merit[username],2)
            else:
                if username in temp_mute:
                    print('in temp_mute')
                    await message.delete()
                else:
                    merit[username] = merit[username] + sentiment
                    merit[username] = round(merit[username],2)

            # Commands
            # !merit: view your merit score
            if user_message.startswith("!merit"):
                merit[username] = merit[username] - sentiment
                merit[username] = round(merit[username],2)
                if username in temp_mute:
                    merit[username] = merit[username] + sentiment
                    merit[username] = round(merit[username],2)
                    print('Merit deleted. This user is temp muted.')
                else:
                    user = user_message.split()[1] if len(user_message.split()) > 1 else username
                    await message.channel.send(f"{user}'s merit: {merit[user]}")

            # !leaderboard: view the merit leaderboard
            if user_message == "!leaderboard":
                merit[username] = merit[username] - sentiment
                merit[username] = round(merit[username],2)
                if username in temp_mute:
                    print('Leaderboard deleted. This user is temp muted.')
                else:
                    sorted_merit = sorted(merit.items(), key=lambda x: x[1], reverse=True)
                    sorted_merit = [(user, score) for user, score in sorted_merit if user != "Pericles"]
                    leaderboard = "\n".join([f"{i+1}. {user} - {score}" for i, (user, score) in enumerate(sorted_merit)])
                    await message.channel.send(f"Merit Leaderboard:\n{leaderboard}")

            # !reset_merit: reset the merit leaderboard
            if user_message == "!reset_merit" and discord.utils.get(message.author.roles, name = "Moderator"): #USE: !reset_merit
                for key in merit:
                    merit[key] = 0
                merit[username] = merit[username] - sentiment
                merit[username] = round(merit[username],2)

            # @Pericles: Pericles will respond to mentions
            if client.user in message.mentions:
                await message.channel.send(f"Hello, {message.author.mention}! Send a message to other users! \n\nCommands: \n!merit: view your merit score \n!leaderboard: view the merit leaderboard \n!reset_merit: reset the merit leaderboard (Moderators Only) \n\nRemember, positive messages will be rewarded with an increase to merit, while negative messages will detract from your merit score.")
                merit[username] = merit[username] - sentiment
                merit[username] = round(merit[username],2)

            print(f"Message sent by {username}: {user_message}")
            with open('merit.json', 'w') as f:
                json.dump(merit, f)

            bucket = anti_spam.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after and (username not in temp_mute):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, don't spam!", delete_after=10)
                print(f"{username} was spamming. Their merit decrease by 1 ")
                merit[username] = merit[username] - 1
                now = datetime.now()
                futuredate = datetime.now() + timedelta(minutes=1)

                current_time = now.strftime("%H:%M:%S")
                print(current_time)
                temp_mute[username] = futuredate

            if username in temp_mute:
                now = datetime.now()
                curr_time = now.strftime("%H:%M:%S")
                print(temp_mute[username])
                print(curr_time)
                print(now.minute)
                if now > temp_mute[username]:
                    del temp_mute[username]

# When a message receives a reaction, add/deduct a merit point to the user who sent the message
@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    author = message.author
    username = str(author)
    reactor = await client.fetch_user(payload.user_id)
    reactorname = str(reactor)
    if username not in merit:
        merit[username] = 0
    # Increase merit
    if reactorname != username and payload.emoji.name == "👍":
        merit[username] += 1
        print(f"{reactorname} reacted to {username}'s message with a thumbs up. {username}'s merit is now {merit[username]}")
    # Decrease merit
    elif reactorname !=  username and payload.emoji.name == "👎":
        merit[username] -= 1
        print(f"{reactorname} reacted to {username}'s message with a thumbs down. {username}'s merit is now {merit[username]}")
    else:
        print(f"{reactorname} reacted to their own message. No merit change.")
    with open('merit.json', 'w') as f:
        json.dump(merit, f)



# Share a welcome message when user joins the server
@client.event
async def on_member_join(member):
    print(member.name + " has joined!")
    try:
        await member.send("Welcome to the server!")
        print("Sent message to " + member.name + "!")
    except Exception as e:
        print("Message not sent!")

#Delete message if moderator reacts with 😡 and reduce merit score
@client.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return

    if reaction.emoji == "😡":
        # Check if the user is a moderator
        if discord.utils.get(user.roles, name = "Moderator"):
            await reaction.message.delete()
            await user.send(f"The following message sent by {reaction.message.author.name} has been deleted: {reaction.message.content}")
            merit[reaction.message.author.name] -=1
        else:
            await reaction.remove(user)
            await user.send("You don't have permission delete this message")

client.run(key)
