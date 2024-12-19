import discord
from discord.ext import commands
import logging
import os
from pathlib import Path
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create bot instance
intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True
intents.dm_messages = True
intents.message_content = True
intents.guilds = True

#Only respond to messages in a specific channel:
#channel = discord.utils.get(ctx.guild.channels, name="channel name")

bot = commands.Bot(command_prefix='!', intents=intents)



#get token
def getToken(path: str()) -> str():
	path = Path(path) #convert path to OOP path
	data = dict() #variable to store token -> access with data["token"]
	if path.exists():
		with open(path, "r") as file:
			data = yaml.safe_load(file) #load dictionary from token yaml file
			token = str(data["token"]) #global variable to store token
			print("Data loaded from config for " + str(path) + " successfully [main::getToken]")
			return token
	else:
		print("Error: config file could not be found [main::getToken]")
		return ""
		

# Load cog
async def load_cogs() -> None:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]  # Strip the .py extension
            try:
                await bot.load_extension(f'cogs.{cog}')
                print(f'Loaded cog: {cog}')
            except Exception as e:
                print(f'Failed to load cog {cog}: {e}')

@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await load_cogs()

@bot.before_invoke #run before any called command is executed
async def check(ctx):
	if not ctx.guild: #check to see if command was sent in a guild (server)
		await ctx.send("Sorry, Anni must only be used from within the Adventure Ted Discord Server.")
		raise commands.CheckFailure #Raise error that stops command execution


# get bot token
token = getToken(".bot.yaml") #FULL PATH TO TOKEN YAML GOES HERE AS STRING
# Run the bot
if token != "":
	bot.run(token)
else:
	print("Error: token not given to bot.run() [main]")

