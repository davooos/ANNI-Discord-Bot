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
		#config = helpers.loadConfig("time")
		#zone = config["timezone"].upper()
	
		syntaxError = bool(False)
		gotTime = bool() #flag used to denote the finding of a time value
		role = str("everyone")
		shortFormat = bool(False) # single time value format
		longFormat = bool(False) # 00:00 format
		tokens = list() #command when separated by spaces
		fields = list() #the values in time format 00:00
		data = str() #message that will be sent as response to command
		hour = int(0)
		minute = int(0)
		second = int(0)
		minOP = bool(False) #makes single value time minutes
		secOP = bool(False) #makes single value time seconds
		hourOP = bool(False) #makes single value time hours
		singleTimeValue = int() #stores time value if it is in the short format
		dayHalf = str() #AM/PM
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
					shortFormat = True
						
				if "hour" in token.lower() or token.lower() == "h":
					hourOP = True
					shortFormat = True
						
				if ":" in token and gotTime == False:
					fields = token.split(":")
					gotTime = True
					longFormat = True
					if fields[0] and fields[0].isdigit():
						hour = int(fields[0])
					if fields[1] and fields[1].isdigit():
						minute = int(fields[1])
				
				if token.isdigit() == True and gotTime == False:
					singleTimeValue = int(token)
					gotTime = True
				
				if "meet" in token.lower() or "meeting" in token.lower():
					delay = False
					meeting = True
				
				if "$" in token:
					role = token.replace("$", "")
					
				if token.upper() == "AM":
					dayHalf = "AM"
				
				if token.upper() == "PM":
					dayHalf = "PM"
		
		#Generate current time object
		now = datetime.datetime.now()
		
		

		if shortFormat == True:
			if hourOP == True:
				hour = singleTimeValue
				future = now + datetime.timedelta(hours=hour)
			elif minOP == True:
				minute = singleTimeValue
				future = now + datetime.timedelta(minutes=minute)
			elif secOP == True:
				second = singleTimeValue
				future = now + datetime.timedelta(seconds=second)
			else:
				print("ERROR: single time value used without value option [remind::alert]")
				
			unix_timestamp = int(future.timestamp())
			discord_timestamp = f"<t:{unix_timestamp}:f>"
			
		elif longFormat == True:
			pass #WORK IN PROGRESS
			#futureTime = self.diffTime(hour,minute,second,dayHalf)
		else:
			print("ERROR: format option was not set [remind::alert]")
			syntaxError = True
		
		#Construct data message for meeting mode
		#Meeting message is used in else clause as it is the default case
		if delay == True and meeting != True:
			data = data + "@" + role + " Oops, there has been a technical delay, our meeting will be starting at "
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
			await ctx.send("I did not detect that a time value was given. Command example: !alert min 5\nEnter !h for more help.")
		else:
			await ctx.send("I was unable to find a specified time or syntax is incorrect, command example: !alert min 5\nEnter !h for more help.")


async def setup(bot):
	await bot.add_cog(time(bot))


