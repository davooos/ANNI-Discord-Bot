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
		leaderTokens = ["leader","chief","officer","manager"]
		
		#flag variables
		isLeader = bool(False)
		inTeam = bool(False)

		for member in members:
			if member.bot == False:
				memData["ID"] = member.id
				memData["Name"] = member.global_name
				memData["StartDate"] = member.joined_at
				memData["EndDate"] = None
				memData["Birthday"] = None
				memData["Team"] = None
				memData["Team Leader"] = None
			    #beginning of block contains for loops that search individual member roles to set default variables.
				for role in member.roles:
				#check for roles regarding position in organization
					if str(role).lower() == "intern" or str(role).lower() == "associate" or str(role).lower() == "volunteer":
						memData["Position"] = str(role).lower()
						if str(role).lower() == "intern":
							period = timedelta(weeks=16)    #time period of internship
							join_date = member.joined_at    #date that member joined the server
							end_date = join_date + period #overload operator for datetime that returns timedelta obj
							memData["EndDate"] = end_date
					else:
						memData["Position"] = None  #default if value is not recognized
					if "team" in str(role).lower():
						teamList = str(role).lower().split()
						memData["Team"] = teamList[1] #Team name without the preceding 'team'
				
				#Block to find additional information based on above results
				if memData["Team"] != None:	#If the member has been assigned a team role
					for m in members:
						for r in m.roles:
							if r.lower() in leaderTokens:
								isLeader = True
							if memData["Team"].lower() in r.lower():
								inTeam = True
						
						if isLeader == True and inTeam == True:
							memData["Team Leader"] = m.global_name
							break;
							
						isLeader = False
						inTeam = False
			    
			    #Add member dictionary to log dictionary
				log[member.id] = memData #set memdata to an element in the log dict()
				memData = dict() #reset memdata for next iteration in loop

		helpers.saveCache("members","MemberData", log)

	@commands.command()
	async def writecache(self, ctx):
		try:
			await self.createLog(ctx)
			await ctx.send("I created and saved cache of server members.")
		except:
			print("Error, unable to create log file [view::writecache]")
			await ctx.send("Sorry, I was unable to write the cache file.")

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
		trueTokens = ["yes", "true", "sure", "positive", "correct", "go", "on"]
		falseTokens = ["no", "false", "nope", "negative", "wrong", "stop", "off"]
		#split message to tokens
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
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
		setDefEndDate = bool(False)
		authorized = bool(False)
		
		#check authorization
		authorized = helpers.checkAuth(ctx.author)
		
		if authorized == True:
			#get log from yaml config file
			log = helpers.loadCache("members","MemberData")
			if bool(log) == False: #check to see if the log is empty -- meaning it could not be loaded
				await self.createLog(ctx) #create new log
				log = helpers.loadConfig("members")
				if bool(log) == False:
					stop = True #set stop flag so output will not be sent to user.

			#if block for finding member id
			if len(tokens) <= 2:
				if tokens[1].lower() in helpTokens:
					data = "Enter !memberconfig member field data"

			elif len(tokens) > 2:
				if tokens[1].isdigit():
					for i,member in enumerate(log.keys()):
						if int(tokens[1]) == int(member) or int(tokens[1]) == i:
							memberid = member
							memberFound = True
							print("[v] -> Member found in config as " + str(member) + " [view::memberConfig]")
				else:
					for member in log:
						if tokens[1].lower() == log[member]["Name"].lower():
							memberid = member
							memberFound = True
							print("[v] -> Member found in config as " + str(member) + " [view::memberConfig]")
				#if block for validating field argument
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
			#if block to interpret field and make new data
			if newValue is not None and validField == True and memberFound == True: #checks to see if a new value and valid field were given
				if field == "Position":
					if newValue in internTokens:
						newValue = "Intern"
						setDefEndDate = True
					elif newValue in volunteerTokens:
						newValue = "Volunteer"
					else:
						print("Error: invalid value given for intern status [view::memberconfig]")
						stop = True
				elif field == "StartDate" or field == "EndDate":
					cur_date = datetime.datetime.now(timezone.utc)
					if newValue in dateTokens:	
						newValue = cur_date
					elif "/" in newValue or "-" in newValue:
						newValue = helpers.convertTime(newValue)
					else:
						print("Error: invalid token for start date argument [view::memberconfig]")
						stop = True
				elif field == "Birthday":
					if newValue in dateTokens:
						newValue = datetime.datetime.now(timezone.utc)
					elif "/" in newValue or "-" in newValue:
						newValue = helpers.convertTime(newValue)
					else:
						print("Error: invalid token for birthday argument [view::memberconfig]")
						stop = True
				elif field == "Name":
					newValue = newValue #no change as name stays an unmanipulated string
				elif field == "School":
					newValue = newValue #no change as name stays an unmanipulated string
				elif field == "Citizen":
					if newValue in trueTokens:
						newValue = True
					elif newValue in falseTokens:
						newValue = False
					else:
						print("Error: invalid token for citizen argument [view::memberconfig]")
						stop = True
			else:
				stop = True 
				print("Error: memberconfig command arguments are not valid [view::memberconfig]")
				data = "Sorry, it looks like your command has some arguments that I do not recognize or cannot find, use the !how command for help."

			if stop == False and len(tokens) > 2:
				print("[v] -> MEMBER: " + str(memberid) + " FIELD: " + str(field) + "NEWVALUE: " + str(newValue) + " [view::memberconfig]")
				log[memberid][field] = newValue #update log if parameters are valid
				if setDefEndDate == True:
					period = timedelta(weeks=16)
					join_date = log[memberid]["StartDate"]
					end_date = join_date + period #overload operator for datetime that returns timedelta obj
					log[memberid]["EndDate"] = end_date
					
				try:
					helpers.saveCache("members", "MemberData", log) #save modified config file
					print("Successfully saved config file [view::memberconfig]")
					data = "I successfully updated the member data!"
				except:
					print("Error: could not save new config [view::memberconfig]")
					data = "Sorry, I could not save this data change."
		else:
			data = "Sorry, It appears that your role does not have access to this command."
			
		await ctx.send(data) #send end message at end of function

	@commands.command(name="view", description="View server member data")
	async def view(self, ctx) -> None:
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split()
		data = str()
		memberid = int()
		memberFound = bool(False)
		fullList = bool(False)
		keyList = list()
		authorized = helpers.checkAuth(ctx.author) #check authorization

		if authorized == True:
			#get log from yaml config file
			log = helpers.loadCache("members","MemberData")
			if bool(log) == False: #check to see if the log is empty -- meaning it could not be loaded
				await self.createLog(ctx) #create new log
				log = helpers.loadCache("members","MemberData")
				if bool(log) == False:
					stop = True #set stop flag so output will not be sent to user.

			if len(tokens) == 2:
				if tokens[1].isdigit():
					keyList = list(log.keys())
					if len(keyList) >= int(tokens[1]):
						memberid = keyList[int(tokens[1])]
						memberFound = True
				else:
					for member in log:
						if log[member]["Name"].lower() == tokens[1].lower():
							memberid = member
							memberFound = True
			elif len(tokens) == 1:
				fullList = True
			else:
				print("Error: Invalid arguments given [view::view]")
				

			if fullList == True and memberFound == False:
				for i,member in enumerate(log):
					data = data + "**Member " + str(i) + ":**\n"
					for field in log[member].keys():
						data = data + "  " + str(field) + "  :  " + str(log[member][field]) + "\n"
					data = data + "\n\n"
			elif fullList == False and memberFound == True:
				data = data + "**Member " + str(tokens[1]) + ":**\n"
				for field in log[memberid].keys():
					data = data + "  " + str(field) + "  :  " + str(log[memberid][field]) + "\n"
			else:
				data = "Sorry, I am not able to fullfill your command, use the !how command for help."
		else:
			data = "Sorry, it appears that your role does not have access to this command."	
		
		await ctx.send(data)
		
		
async def setup(bot):
	await bot.add_cog(view(bot))
