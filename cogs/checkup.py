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
		self.context = None
		
		self.scheduler.start()
		
	async def check(self) -> None:
		data = str()
		members = self.context.guild.members
		log = helpers.loadCache("members","MemberData")

		#temp variables
		memberid = int(0)
		leaderid = int(0)

		#flag variables
		stop = bool(False)
		
		for m in log:
			if log[m]["position"].lower() == "intern" and log[m]["enddate"] > log[m]["startdate"]:
				data = "Hey there, I hope your week has been going well! "
				data = data + "Don't forget to submit your weekly report to your team leader!\n"
			if log[m]["teamleader"] != None:
				data = data + "Your team leader is " + log[m]["teamleader"]
				
			for member in members:
				if member.id == m:
					await member.send(data)

		
	@commands.command(name = "runcheck", description = "runs the checkup reminder for interns")
	async def runcheck(self, ctx) -> None:
		self.context = ctx #set member to current ctx
		data = str()
		#check authorization
		authorized = helpers.checkAuth(ctx.author)

		if authorized == True:
			data = "Sent progress update reminders to interns!"
			await self.check()
		else:
			data = "Sorry, you do not have authorization to run this command."
			
		await ctx.send(data)

	@commands.command(name = "schedule", description = "Schedules intern reminders for a specific time and date")
	async def schedule(self, ctx) -> None:
		self.context = ctx #update member to current ctx
		data = str()
		error = str()
		authorized = helpers.checkAuth(ctx.author) #check authorization
		stripped = ctx.message.content.replace("[","").replace("]","") #remove brackets from command string
		tokens = stripped.split() #split command string into list of words
		jobs = self.scheduler.get_jobs()
		
		#constant keywords
		days = {
			"monday": "mon",
			"tuesday": "tue",
			"wednesday": "wed",
			"thursday": "thu",
			"friday": "fri",
			"saturday": "sat",
			"sunday": "sun"
		}
		remove = ["rm", "remove", "r"]
		show = ["all", "show", "help", "list"]
		
		#temp variables
		d = str() #day
		h = int() #hour
		m = int() #minute
		fields = list()
		
		#flag variables
		mkschedule = bool(False)
		removeSchedule = bool(False)
		showAll = bool(False)
		
		if authorized == True:
			if len(tokens) > 1:
				if tokens[1].lower() in days:
					d = days[tokens[1].lower()]
					mkschedule = True
				elif tokens[1].lower() in remove:
					removeSchedule = True
				elif tokens[1].lower() in show:
					showAll = True
			else:
				showAll = True
				
			if len(tokens) > 2 and showAll == False: #showall command would not be longer than 2 tokens
				if ":" in tokens[2] and mkschedule == True:
					timeFields = tokens[2].split(":")
					if len(timeFields) == 2:
						h = int(timeFields[0])
						m = int(timeFields[1])
						self.taskNum = self.taskNum + 1
						try:
							self.scheduler.add_job(self.check, 
								CronTrigger(day_of_week = d, hour = h, minute = m, second = 0),
								id = str(self.taskNum),
								name = "Scheduled job for checkup.check",
								replace_existing = True
							)
							data = "Done!"
						except:
							print("Error, unable to schedule task [checkup:schedulecheck]")
							error = "Sorry, I was not able to schedule the task."
							
				elif tokens[2].isdigit() and removeSchedule == True:
					try:
						self.scheduler.remove_job(tokens[2])
						data = "Done!"
					except:
						error = "Sorry, I was unable to remove this job."
						print("Error, unable to remove job from scheduler [checkup::schedule]")
				else:
					print("Error, Invalid or too many tokens [checkup::schedule]")
					error = "Sorry, I was unable to interpret this command. Use !how for help."
					
			elif showAll == True:
				for job in jobs:
					data = data + f"Job ID: {job.id}\n"
					data = data + f"Job Name: {job.name}\n"
					data = data + f"Next Run Time: {job.next_run_time}\n"
					data = data + f"Trigger: {job.trigger}\n"
					data = data + "---\n"

				if len(data) < 1:
					data = "It looks like there are no jobs to view."
				
			else:
				print("Error, Invalid or too many tokens [checkup::schedule]")
				error = "Sorry, I was unable to interpret this command. Use !how for help."	
		else:
			error = "Sorry, you do not have authorization to run this command."
			
		if len(data) > 1:
			await ctx.send(data)
		else:
			await ctx.send(error)


	@commands.command(name = "updatecheckup", description = "Update ctx member")
	async def updatecheckup(self, ctx) -> None:
		self.context = ctx


async def setup(bot):
	await bot.add_cog(checkup(bot))
