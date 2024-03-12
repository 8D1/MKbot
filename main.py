import discord
from discord.ext import commands
from discord import Option

# Your bot's token
TOKEN = 'MTE4Mzk2NDM0Nzk1ODA0NjgwMA.GN2Rs7.zkkYOztMKWgsjKBIV2erkGJrX1HcVsVdU8xt6k'

trigger_words = ['skibidi']
# List of blacklisted user IDs (use actual user IDs)
blacklisted_users = ['123456789012345678', '987654321098765432']  # Example user IDs

# Bot setup with intents
intents = discord.Intents.all()  # Using all intents
bot = commands.Bot(command_prefix="/", intents=intents)

counter = 0
user_trigger_counts = {}  # Dictionary to keep track of trigger word counts per user
role_to_assign_id = '1214740574306041917'  # The ID of the role you want to assign


@bot.event
async def on_ready():
    print(f'{bot.user} is connected and ready.')


@bot.event
async def on_message(message):
    global counter
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if any(word.lower() in message.content.lower() for word in trigger_words):
        counter += 1
        user_trigger_counts[user_id] = user_trigger_counts.get(user_id, 0) + 1

        if user_trigger_counts[user_id] == 5:
            await message.channel.send(f"{message.author.mention}, you're a sinner! May god have mercy on your soul.")
            user_trigger_counts[user_id] = 0  # Reset the count for the user
            role = message.guild.get_role(int(role_to_assign_id))
            if role:
                await message.author.add_roles(role)
                # await message.channel.send(f"Role {role.name} has been assigned to {message.author.mention}")
            return
        else:
            await message.channel.send(f"No. {message.author.mention} {counter}")
            return

    await bot.process_commands(message)


@bot.slash_command(description="Echoes back what you say.")
async def echo(ctx, message: Option(str, "Enter the message to echo")):
    if any(word.lower() in message.lower() for word in trigger_words):
        await ctx.respond(f"No. {ctx.author.mention} Bad dog.")
    else:
        await ctx.respond(message)


@bot.slash_command(description="Terminates the bot")
async def suicide(ctx):
    authorized_user_id = '265873249944993793'  # ID of the user allowed to use this command
    if str(ctx.author.id) == authorized_user_id:
        await ctx.respond("Goodbye cruel world.")
        await bot.close()
    else:
        await ctx.respond("You are not permitted to execute this command.")


# Run the bot
bot.run(TOKEN)
