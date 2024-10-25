import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone

class people(object):
	def __init__(self):

	def createLog(self) -> None:


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
				memData["name"] = member.global_name
				memData["intern"] = False
				memData["startDate"] = join_date
				memData["endDate"] = end_date

				log[member.id] = memberData
				memData = dict()

		helpers.saveConfig("members", log)

	@commands.command()
	async def memc(self, ctx):
		await memberconfig(ctx)

	@commands.command()
	async def memberconfig(self, ctx):
		log = helpers.loadConfig("members")
		helpTokens = ["all", "print", "show", "questions", "quest", "help"]
		internTrueTokens = ["yes", "true","in"]
		internFalseTokens = ["no", "false", "end","over","out"]
		dateTokens = ["makedate", "date", "this", "thisdate", "now"]

		tokens = ctx.message.content.split()
		data = str()

		#temp variables
		memberid = int()
		memberName = str()
		memberidx = int()
		newValue = None
		field = str()

		#flag variables
		memberFound = bool(False)
		validField = bool(False)
		stop = bool(False)


		if len(tokens) < 2 or tokens[1].lower() in helpTokens:
			data = "Enter !memberconfig member field data"
		elif len(tokens) > 1:
			if tokens[1].isdigit():
				for i,member in enumerate(log.keys()):
					if int(tokens[1]) == int(member) or int(tokens[1]-1) == i:
						memberid = member
						memberFound = True
						print("Member found in config as " + member + " [view::memberConfig]")
			else:
				for member in log:
					if tokens[1] == member["name"]:
						memberid = member
						memberFound = True
						print("Member found in config as " + member + " [view::memberConfig]")

			if len(tokens) > 2:
				for f in log[0]:
					if tokens[2] == f:
						field = tokens[2]
						validField = True

				if validField == True:
					if len(tokens) > 3:
						newValue == tokens[3]
		else:
			print("Error: insufficient arguments given [view::memberconfig]")

		if newValue not None and validField == True: #checks to see if a new value and valid field were given
			if field == "intern":
				if newValue in internTrueTokens:
					newValue = bool(True)
				elif newValue in internFalseTokens:
					newValue = bool(False)
				else:
					print("Error: invalid value given for intern status [view::memberconfig]")
					stop = True
			elif field == "startDate" or field == "endDate":
				cur_date = datetime.now(timezone.utc)
				if newValue in dateTokens:	
					newValue = cur_date
				else:
					print("Error: invalid token for start date argument [view::memberconfig]")
					stop = True

		if stop != True:
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
		guild = ctx.guild
		members = guild.members
		
		for i,member in enumerate(members):
			if member.bot == False:
				data = data + str(i+1) + "  :  " + str(member.id) + "  :  " + str(member.global_name) + "\n"
		
		await ctx.send(data)
		
		
async def setup(bot):
	await bot.add_cog(view(bot))
