import datetime
import random  # For generating random numbers
import discord
from discord import Option
from discord.ext import commands
import json
with open('config.json', 'r') as file:
    config = json.load(file)
#fixed it so i dont expose the new token
TOKEN = config["token"]
trigger_words = ['skibidi']
# List of allowed channel IDs for specific replies
allowed_channels = ['1213328540586610701', '1213646258519150622', '1214684173189775370']
target = ['973296824137969744']
secondtarget = ['1184651914420428932', '265873249944993793', '1087192861734342746']

# Bot setup with intents
intents = discord.Intents.all()  # Using all intents
bot = commands.Bot(command_prefix="/", intents=intents)

counter = 0  # Global message counter for "skibidi"
user_trigger_counts = {}  # Dictionary to keep track of trigger word counts per user

@bot.event
async def on_ready():
    print(f'{bot.user} is connected and ready.')

@bot.event
async def on_message(message):
    global counter

    if message.author == bot.user:
        return

    if any(word.lower() in message.content.lower() for word in trigger_words):
        counter += 1
        user_id = str(message.author.id)
        user_trigger_counts[user_id] = user_trigger_counts.get(user_id, 0) + 1

        if user_trigger_counts[user_id] == 1:
            await message.reply(f"{message.author.mention}, May god have mercy on your corrupted soul.")
            user_trigger_counts[user_id] = 0
            if random.randint(1, 3) == 1:
                timeout_duration = datetime.timedelta(minutes=1)
                timeout_until = datetime.datetime.now(datetime.timezone.utc) + timeout_duration
                await message.author.edit(communication_disabled_until=timeout_until)
                await message.channel.send(f"But i dont. Goodbye {message.author.mention}")
        else:
            await message.reply(f"No. {counter}, bad dog {message.author.mention}.")

    await bot.process_commands(message)

@bot.slash_command(description="Echoes back what you say.")
async def echo(ctx, message: Option(str, "Enter the message to echo")):
    await ctx.respond(message)

@bot.slash_command(description="Terminates the bot")
async def suicide(ctx):
    authorized_user_id = '265873249944993793'  # ID of the user allowed to use this command
    if str(ctx.author.id) == authorized_user_id:
        await ctx.respond("Goodbye cruel world.")
        await bot.close()
    else:
        await ctx.respond("You are not permitted to execute this command.")

bot.run(TOKEN)
