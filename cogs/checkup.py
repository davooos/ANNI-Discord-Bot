#Imports
import utils.helpers as helpers
import os.path
import datetime
from datetime import tzinfo, timedelta, datetime, timezone

#Discord imports
import discord
from discord.ext import commands

#Scheduler imports
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

#Google imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class checkup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# Create an instance of the scheduler
		self.scheduler = AsyncIOScheduler()
		self.scheduled = bool(False)
		self.taskNum = int(0)
		self.context = None
		# Scheduler variables
		self.scheduler.start()
		# Google API variables
		self.creds = None
		self.reportLink = str()
	
	def getSignedMembers(self) -> list():
		# If modifying these scopes, delete the file token.json.
		SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
		# The ID and range of the spreadsheet.
		SPREADSHEET_ID = "" #Paste spreadsheet id from url (after /d/)
		RANGE_NAME = "" #Add range of !'first cell':'last cell'
		NAMEINDEX = int() #Add index of member name location as it is listed in the google sheet.

		signedMembers = list()

		if os.path.exists("cache/GoogleAPI/token.json"):
			self.creds = Credentials.from_authorized_user_file("cache/GoogleAPI/token.json", SCOPES)

		# If there are no (valid) credentials available, let the user log in.
		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
				"cache/GoogleAPI/credentials.json", SCOPES
				)
			self.creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("cache/GoogleAPI/token.json", "w") as token:
			token.write(self.creds.to_json())
		
		try:
			service = build("sheets", "v4", credentials=self.creds)

			# Call the Sheets API
			sheet = service.spreadsheets()
			result = (
				sheet.values()
				.get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
				.execute()
			)
			values = result.get("values", [])

			if not values:
				print("Error, could not retrieve data from Google Sheets.")
				return

			#Save names of members in report
			for row in values:
				signedMembers.append(row[NAMEINDEX])

		except HttpError as err:
			print(err)

		#Return list of member names from report
		return signedMembers


	async def check(self) -> None:
		data = str()
		members = self.context.guild.members
		log = helpers.loadCache("members","MemberData")
		signedMembers = self.getSignedMembers()

		
		for m in log:
			if log[m]["position"].lower() == "intern" and log[m]["enddate"] > log[m]["startdate"] and log[m]["name"] not in signedMembers:
				data = "Hey there, I hope your week has been going well! "
				data = data + "Don't forget to submit your weekly report for your team leader!\n"
				data = data + "Enter your weekly report here: " + self.reportLink + "\n"
			if log[m]["teamleader"] != None or log[m]["team leader"] != "na":
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

	@commands.command(name = "replink", description = "Update Google Form report link")
	async def replink(self, ctx) -> None:
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
		data = str()
		errors = list()

		if len(tokens) == 2:
			self.reportLink = tokens[1]
			data = "Done, saved " + tokens[1] + " as the new Google Form report link."
		else:
			errors.append("Invalid number of arguments used.")
		
		if len(data) < 1 or len(errors) > 0:
			data = "Sorry, I am not able to fullfill your command, use the !how command for help.\n"
			data = data + "Errors: \n"
			for e in errors:
				data = data + "[E] " + e + "\n"
			await ctx.send(data)
		else:
			await ctx.send(data)

async def setup(bot):
	await bot.add_cog(checkup(bot))
