import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone
from datetime import timedelta


class view(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def createLog(self, ctx) -> None:
		log = dict() #dictionary for members
		memData = dict() #dictionary for individual member data
		members = ctx.guild.members #THIS MAY BE ONLY FOR CACHED MEMBERS IN SERVER --- PLEASE CHECK LATER

		period = timedelta(weeks=16)
		join_date = ctx.author.joined_at
		end_date = join_date + period #overload operator for datetime that returns timedelta obj

		for member in members:
			if member.bot == False:
				memData["ID"] = member.id
				memData["Name"] = member.global_name
				memData["Position"] = None
				memData["StartDate"] = join_date
				memData["EndDate"] = end_date
				memData["Birthday"] = None

				log[member.id] = memData
				memData = dict()

		helpers.saveConfig("members", log)

	@commands.command()
	async def memc(self, ctx):
		await self.memberconfig(ctx)

	@commands.command()
	async def memberconfig(self, ctx):
		#list acceptable token forms in order to interpret commands
		helpTokens = ["all", "print", "show", "questions", "quest", "help"]
		internTokens = ["intern", "internship","in"]
		volunteerTokens = ["vol", "volunteer", "worker", "employee"]
		dateTokens = ["makedate", "date", "this", "thisdate", "now"]
		#split message to tokens
		tokens = ctx.message.content.split()
		data = str()

		#temp variables
		memberid = int()
		memberName = str()
		memberidx = int()
		newValue = None
		field = str()
		keyList = list()

		#flag variables
		memberFound = bool(False)
		validField = bool(False)
		stop = bool(False)

		#get log from yaml config file
		log = helpers.loadConfig("members")
		if bool(log) == False: #check to see if the log is empty -- meaning it could not be loaded
			await self.createLog(ctx) #create new log
			log = helpers.loadConfig("members")
			if bool(log) == False:
				stop = True #set stop flag so output will not be sent to user.


		if len(tokens) < 2 or tokens[1].lower() in helpTokens:
			data = "Enter !memberconfig member field data"
		elif len(tokens) > 2:
			if tokens[1].isdigit():
				for i,member in enumerate(log.keys()):
					if int(tokens[1]) == int(member) or int(tokens[1]) == i:
						memberid = member
						memberFound = True
						print("Member found in config as " + str(member) + " [view::memberConfig]")
			else:
				for member in log:
					if tokens[1].lower() == log[member]["Name"].lower():
						memberid = member
						memberFound = True
						print("Member found in config as " + str(member) + " [view::memberConfig]")
			
			if len(tokens) > 3 and memberFound == True:
				keyList = list(log.keys()) #convert dictionary view to list of keys
				if len(keyList) > 0:
					for f in log[keyList[0]].keys(): #iterate through member fields
						if tokens[2].lower() == f.lower():
							field = f #check if the given field argument is valid
							validField = True

					if validField == True:
						if len(tokens) > 3:
							newValue = tokens[3]
			
		else:
			print("Error: insufficient arguments given [view::memberconfig]")

		print("[v] -> MEMBERFOUND: " + str(memberFound) + " , VALIDFIELD: " + str(validField) + " , NEWVALUE: " + str(newValue) + " [veiw::memberconfig]")
		if newValue is not None and validField == True and memberFound == True: #checks to see if a new value and valid field were given
			if field == "Position":
				if newValue in internTokens:
					newValue = "Intern"
				elif newValue in volunteerTokens:
					newValue = "Volunteer"
				else:
					print("Error: invalid value given for intern status [view::memberconfig]")
					stop = True
			elif field == "StartDate" or field == "EndDate":
				cur_date = datetime.now(timezone.utc)
				if newValue in dateTokens:	
					newValue = cur_date
				else:
					print("Error: invalid token for start date argument [view::memberconfig]")
					stop = True
			elif field == "Name":
				newValue = newValue #no change as name stays an unmanipulated string
		else:
			stop = True 
			print("Error: memberconfig command arguments are not valid [view::memberconfig]")
			data = "Sorry, it looks like your command has some arguments that I do not recognize or cannot find, use the !how command for help."

		if stop == False and len(tokens) > 2:
			print("[v] -> MEMBER: " + str(memberid) + " FIELD: " + str(field) + "NEWVALUE: " + str(newValue) + " [view::memberconfig]")
			log[memberid][field] = newValue #update log if parameters are valid
			try:
				helpers.saveConfig("members", log) #save modified config file
				print("Successfully saved config file [view::memberconfig]")
				data = "I successfully updated the member data!"
			except:
				print("Error: could not save new config [view::memberconfig]")
				data = "Sorry, I could not save this data change."

		await ctx.send(data) #send end message at end of function

	
	@commands.command()
	async def getData(self, ctx, member: discord.Member = None) -> None:
		members = ctx.guild.members
		memberData = dict()
		roleData = dict()
	
		
		for member in members:
			roleData[member.id] = member.roles
			memberData[member.id] = member
		
		print(roleData)
		print()
		print(members)
		
		
	@commands.command(name="view", description="View server member data")
	async def view(self, ctx) -> None:
		data = str()
		#guild = ctx.guild
		#members = guild.members

		#get log from yaml config file
		log = helpers.loadConfig("members")
		if bool(log) == False: #check to see if the log is empty -- meaning it could not be loaded
			await self.createLog(ctx) #create new log
			log = helpers.loadConfig("members")
			if bool(log) == False:
				stop = True #set stop flag so output will not be sent to user.
		
		for i,member in enumerate(log):
			data = data + "**Member " + str(i) + ":**\n"
			for field in log[member].keys():
				data = data + "  " + str(field) + "  :  " + str(log[member][field]) + "\n"
			data = data + "\n\n"
		
		await ctx.send(data)
		
		
async def setup(bot):
	await bot.add_cog(view(bot))
