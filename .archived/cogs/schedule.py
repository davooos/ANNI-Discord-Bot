import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import tzinfo, timedelta, datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

#import commands that can be scheduled
from checkup import *


class scheduler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# Create an instance of the scheduler
		self.scheduler = AsyncIOScheduler()
		self.context = None
		self.tasknum = int(1) #start at 1 since task 0 is the setup update task
		self.scheduler.start()
		
	@commands.command(name = "mkschedule", description = "Schedules commands to run weekly")
	async def mkschedule(self, ctx) -> None:
		self.context = ctx #set member to current ctx
		data = str()
		error = str()
		authorized = helpers.checkAuth(ctx.author) #check authorization
		stripped = ctx.message.content.replace("[","").replace("]","") #remove brackets from command string
		tokens = stripped.split() #split command string into list of words
		
		#constant variables
		days = {
			"monday": "mon",
			"tuesday": "tue",
			"wednesday": "wed",
			"thursday": "thu",
			"friday": "fri",
			"saturday": "sat",
			"sunday": "sun"
		}
		
		commands = {
			"checkup": checkup.check
		}
		
		#temp variables
		d = str() #day
		h = int() #hour
		m = int() #minute
		fields = list()
		command = None
		
		#flag variables
		stop = bool(False)
		jobFail = bool(False)
		
		if authorized == True:
			if len(tokens) == 4:
				if tokens[1].lower() in commands:
					command = commands[tokens[1].lower()]
				else:
					stop = True
					
				if tokens[2].lower() in days:
					d = days[tokens[2].lower()]
				else:
					stop = True
				
				if ":" in tokens[3]:
					timeFields = tokens[3].split(":")
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
			self.scheduler.add_job(command, 
				CronTrigger(day_of_week = d, hour = h, minute = m, second = 0),
				id = str(self.taskNum),
				name = f"Scheduled job for {command}",
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
			
	@commands.command(name = "schedules", description = "View scheduled jobs")
	async def schedules(self, ctx) -> None:
		self.context = ctx #set member to current ctx
		data = str()
		jobs = self.scheduler.get_jobs()
		
		for job in jobs:
			data = data + f"Job ID: {job.id}\n"
			data = data + f"Job Name: {job.name}\n"
			data = data + f"Next Run Time: {job.next_run_time}\n"
			data = data + f"Trigger: {job.trigger}\n"
			data = data + "---\n"

		if len(data) > 1:
			await ctx.send(data)
		else:
			data = "Sorry, there are no jobs to view."
			await ctx.send(data)

################################# For updateing ctx across cogs #########################################################
	@commands.command(name = "setup", description = "Run this to set up the intern remind feature!")
	async def setup(self, ctx) -> None:
		self.context = ctx
		self.scheduler.add_job(self.update, 
				CronTrigger(day_of_week = "sat", hour = 1, minute = 0, second = 0),
				id = str(0),
				name = "Scheduled job for data updater",
				replace_existing = True
			)
		await ctx.send("Intern reminders have been set up!")
		
	async def update(self):
		await self.context.send("!updatecheckup") #command to update checkup ctx
		
		
		
async def setup(bot):
	await bot.add_cog(scheduler(bot))