import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import tzinfo, timedelta, datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class checkup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# Create an instance of the scheduler
		self.scheduler = AsyncIOScheduler()
		self.scheduled = bool(False)
		self.taskNum = int(0)
		
		self.scheduler.start()
		
	def check(self, ctx) -> None:
		data = str()
		members = ctx.guild.members
		log = helpers.loadCache("members","MemberData")
		#check authorization
		authorized = helpers.checkAuth(ctx.author)

		#temp variables
		memberid = int(0)
		leaderid = int(0)

		#flag variables
		stop = bool(False)
		
		for m in log:
			if log[m]["Position"].lower() == "intern" and log[m]["EndDate"] > log[m]["StartDate"]:
				data = "Hey there, I hope your week has been going well! "
				data = data + "Don't forget to submit your weekly report to your team leader!\n"
			if log[m]["Team Leader"] != None:
				data = data + "Your team leader is " + log[m]["Team Leader"]
				
			for member in members:
				if member.id == m:
					member.send(data)

		
	@commands.command(name = "runcheck", description = "runs the checkup reminder for interns")
	async def runcheck(self, ctx) -> None:
		data = str()
		#check authorization
		authorized = helpers.checkAuth(ctx.author)

		if authorized == True:
			data = "Sent progress update reminders to interns!"
			self.check(ctx)
		else:
			data = "Sorry, you do not have authorization to run this command."
			
		await ctx.send(data)
		
	@commands.command(name = "schedulecheck", description = "Schedules intern reminders for a specific time and date")
	async def schedulecheck(self, ctx) -> None:
		data = str()
		error = str()
		authorized = helpers.checkAuth(ctx.author) #check authorization
		stripped = ctx.message.content.replace("[","").replace("]","") #remove brackets from command string
		tokens = stripped.split() #split command string into list of words
		
		#constant variables
		days = {"monday": "mon",
			"teusday": "teu",
			"wednesday": "wed",
			"thursday": "thu",
			"friday": "fri",
			"saturday": "sat",
			"sunday": "sun"
		}
		
		#temp variables
		d = str() #day
		h = int() #hour
		m = int() #minute
		fields = list()
		
		#flag variables
		stop = bool(False)
		jobFail = bool(False)
		
		if authorized == True:
			if len(tokens) == 3:
				if tokens[1].lower() in days:
					d = days[tokens[1].lower()]
				else:
					stop = True
				
				if ":" in tokens[2]:
					timeFields = tokens[2].split(":")
					if len(timeFields) == 2:
						h = int(timeFields[0])
						m = int(timeFields[1])
					else:
						stop = True
				else:
					stop = True
					
			else:
				stop = True
				print("Error, Invalid number of tokens in command [checkup::schedulecheck]")
				
		else:
			stop = True
			error = "Sorry, you do not have authorization to run this command."
			
		if stop == False:
			self.taskNum = self.taskNum + 1
			#try:
			self.scheduler.add_job(checkup.check(self, ctx), 
				CronTrigger(day_of_week = d, hour = h, minute = m, second = 0),
				id = str(self.taskNum),
				name = "Scheduled job for checkup.check",
				replace_existing = True
			)
			#except:
				#print("Error, unable to schedule task [checkup:schedulecheck]")
				#jobFail = True
			
			if jobFail == True:
				data = "Sorry, I was unable to schedule this command."
			else:
				data = "Done!"
				
			await ctx.send(data)
		
		else:
			if len(error) < 1:
				error = "Sorry, I was enable to process your command. Use the !how command for help."
			
			await ctx.send(error)
				




async def setup(bot):
	await bot.add_cog(checkup(bot))
