import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone

class time(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name="al", description="alias to alert command")
	async def al(self, ctx):
		await self.alert(ctx)
		
	@commands.command(name="alert", description="creates an alert")
	async def alert(self, ctx):
		syntaxError = bool(False)
		gotTime = bool() #flag used to denote the finding of a time value
		role = str("everyone")
		tokens = list() #command when separated by spaces
		data = str() #message that will be sent as response to command
		hour = int(0)
		minute = int(0)
		minOP = bool(False) #makes single value time minutes
		hourOP = bool(False) #makes single value time hours
		singleTimeValue = int() #stores time value if it is in the short format
		#alert messages
		meeting = bool(False) #sets message type to meeting (Default)
		delay = bool(True) #sets message type to delayed meeting
		
		
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
		#parse tokens, setting flags or values declared above
		if len(tokens) > 1:
			for idx, token in enumerate(tokens):
				if "min" in token.lower() or token.lower() == "m":
					minOP = True
						
				if "hour" in token.lower() or token.lower() == "h":
					hourOP = True
				
				if token.isdigit() == True and gotTime == False:
					singleTimeValue = int(token)
					gotTime = True
				
				if "meet" in token.lower() or "meeting" in token.lower():
					delay = False
					meeting = True
				
				if "$" in token:
					role = token.replace("$", "")
		else:
			data = "Sorry, I could not fullfill your command. Use the '!how' command for help."
			await ctx.send(data)
			return
		
		#Generate current time object
		now = datetime.datetime.now()
		
		
		if hourOP == True:
			hour = singleTimeValue
			future = now + datetime.timedelta(hours=hour)
		elif minOP == True:
			minute = singleTimeValue
			future = now + datetime.timedelta(minutes=minute)	
		else:
			data = "Sorry, I could not identify if the time is in hours or minutes.\nUse '!how' for help.\n"
			data = data + "Command example: !alert minute 5"
			await ctx.send(data)
			return
		
		#Generate discord timestamp useing new timedelta created above
		unix_timestamp = int(future.timestamp())
		discord_timestamp = f"<t:{unix_timestamp}:f>"
		
		#Construct data message for meeting mode
		#Meeting message is used in else clause as it is the default case
		if delay == True and meeting != True:
			data = data + "@" + role + " There has been a technical delay, our meeting will be starting at "
		else:
			data = data + "@" + role + " Meeting will be starting at "	
		
		#Add timestamp to data message
		data = data + discord_timestamp

		#check for syntax errors before sending message
		if syntaxError == False and gotTime == True:
			await ctx.send(data)
		elif syntaxError == True:
			await ctx.send("Improper syntax, command example: !alert min 5\nEnter !h for more help.")
		elif gotTime == False:
			await ctx.send("I did not detect that a time value was given.\nCommand example: !alert min 5\nEnter '!how' for help.")
		else:
			await ctx.send("I was unable to find a specified time or syntax is incorrect,\nCommand example: !alert min 5\nEnter '!how' for help.")


async def setup(bot):
	await bot.add_cog(time(bot))


