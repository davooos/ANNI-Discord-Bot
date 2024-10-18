import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone
#import discord-timestamps



class time(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	def getTime(self, h: int(), m: int(), s: int()) -> dict():
		config = helpers.loadConfig("time")
		zone = config["timezone"]
		zoneMod = helpers.timeMod(zone) #conversion value from UTC to timezone in config file
		now = datetime.datetime.now(timezone.utc)
		print("Current Time: " + str(now) + " [remind::getTime]")
		dayHalf = str()
		hour = now.hour + h + zoneMod
		minute = now.minute + m
		second = now.second + s
		days = int()
		
		#Convert 24H time to 12H AM/PM
		if hour > 12:
			dayHalf = "PM"
			hour = hour - 12
		else:
			dayHalf = "AM"
		
		#add function arguments to current time
		if second > 59:
			minute = minute + int(second / 59)
			second = second % 59
		if minute > 59:
			hour = hour + int(minute / 59)
			minute = minute % 59
		if hour == 12:
			if dayHalf == "AM":
				dayHalf = "PM"
			elif dayHalf == "PM":
				dayHalf = "AM"
		if hour > 12:
			days = int(hour/12)
			if days % 2 != 0:
				if dayHalf == "AM":
					dayHalf = "PM"
				elif dayHalf == "PM":
					dayHalf = "AM"
			hour = hour % 12
				
		#Create time dictionary
		time = {"hour": int(), "minute": int(), "second": int(), "dayHalf": str()}
		#Add time fields to time dictionary
		time["hour"] = hour
		time["minute"] = minute
		time["second"] = second
		time["dayHalf"] = dayHalf
		
		return time
	@commands.command(name="tc", description="alias to timeconf")
	async def tc(self, ctx):
		await self.timeconf(ctx)
	
	@commands.command(name="timeconf", description="Set variables to config")
	async def timeconf(self, ctx):
		data = str()
		operationSuccess = bool(False)
		currentData = helpers.loadConfig("time")
		configData = {"timezone": "EDT"}
		configFields = ["timezone"]
		tokens = ctx.message.content.split()
		
		if len(tokens) > 2:
			if tokens[1] in configFields:
				for i, field in enumerate(configFields):
					print(i)
					if tokens[1] == configFields[i]:
						configData[configFields[i]] = tokens[2]
						helpers.saveConfig("time", configData)
						await ctx.send("Saved Config")
						operationSuccess = True
				if operationSuccess == False:
					await ctx.send("Failed to save config")
		elif len(tokens) == 2:	
			if tokens[1] == "options" or tokens[1] == "help" or tokens[1] == "h":
				data = data + "Available fields: \n"
				for field in configFields:
					data = data + " - " + field + ":  CURRENT VALUE -> [" + currentData[field] + "]" + "\n"
				await ctx.send(data)
		else:
			await ctx.send("Invalid options, try: !timeconf help") 
		
	@commands.command(name="h", description="sends instructional message")
	async def h(self, ctx):
		data = str()
		data = data + "Command examples:\n"
		data = data + "		!alert minute 5\n"
		data = data + "Or short hand:\n"
		data = data + "		!a m 5\n"
		data = data + "Long format(Enter specific time)(AM and PM will default to current):\n"
		data = data + "		!a 7:45 AM\n"
		await ctx.send(data)
	
	@commands.command(name="a", description="alias to alert command")
	async def a(self, ctx):
		await self.alert(ctx)
		
	@commands.command(name="alert", description="creates an alert")
	async def alert(self, ctx):
		config = helpers.loadConfig("time")
		zone = config["timezone"].upper()
	
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
		
		
		tokens = ctx.message.content.split()
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
					

		if shortFormat == True:
			if hourOP == True:
				hour = singleTimeValue
			elif minOP == True:
				minute = singleTimeValue
			elif secOP == True:
				second = singleTimeValue
			else:
				print("ERROR: single time value used without value option [remind::alert]")
				
			futureTime = self.getTime(hour, minute, second)
		elif longFormat == True:
			pass #WORK IN PROGRESS
			#futureTime = self.diffTime(hour,minute,second,dayHalf)
		else:
			print("ERROR: format option was not set [remind::alert]")
			syntaxError = True
			
		print("Time sent to getTime: " + str(hour) + " " + str(minute) + " " + str(second) + " [remind::alert]")
		
		#Construct data message for meeting mode
		#Meeting message is used in else clause as it is the default case
		if delay == True and meeting != True:
			data = data + "@" + role + " Oops, there has been a technical delay, our meeting will be starting "
		else:
			data = data + "@" + role + " Meeting will be starting "	
		
		if shortFormat == True:
			if hour != 0:
				data = data + "in " + str(hour) + " Hours at "
			if minute != 0:
				data = data + "in " + str(minute) + " Minutes at "
			#WORK IN PROGRESS: TEMPORARY
			if futureTime["hour"] <= 9:
				data = data + "0" + str(futureTime["hour"]) + ":"
			else:
				data = data + str(futureTime["hour"]) + ":"
			if futureTime["minute"] <= 9:
				data = data + "0" + str(futureTime["minute"]) + " "
			else:
				data = data + str(futureTime["minute"]) + " "
			data = data + str(futureTime["dayHalf"]) + " " + zone
			
		elif longFormat == True:
			data = data + "at " + str(hour) + ":" + str(minute) + " " + str(dayHalf) + " " + zone
			#WORK IN PROGRESS
			#data = data + str(futureTime["hour"]) + ":" + str(futureTime["minute"]) + " " + str(futureTime["dayHalf"])

	
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


