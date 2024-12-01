import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import tzinfo, timedelta, datetime, timezone


class chatbot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="ask", description="ask the bot a question")
	async def ask(self, ctx) -> None:
		authorStats = dict()
		data = str()
		
		#flag variables
		stop = bool(False)

		#get log from yaml config file
		log = helpers.loadCache("members", "MemberData")
		if bool(log) == False: #check to see if the log is empty -- meaning it could not be loaded
			print("Error: Could not get log [chatbot::ask]")
			stop = True #set stop flag so output will not be sent to user.
		
		if stop == False:
			for member in log:
				if member == ctx.author.id:
					authorStats = log[member]

			#Token bank to decifer commands
			getQuestions = ["all", "print", "show", "questions", "quest", "help"] #command tokens for showing quesitons
			positions = ["moderator","graphic designer", "animator", "software engineer", "communications"]
			leaders = ["chief", "officer", "manager"]
			questions = ["When does my internship end?", "What team am I part of?", "Who are the moderators?", "Who are my team leaders?"]
			data = str()
			stripped = ctx.message.content.replace("[","").replace("]","")
			tokens = stripped.split()
			
			#command interpretation per token(word)
			if len(tokens) < 2 or tokens[1] in getQuestions:
				for i,quest in enumerate(questions):
					data = data + str(i+1) + ": " + str(quest) + "\n"
				data = data + "Enter !ask + the number repreasenting the question you wish to ask me!"

			elif len(tokens) < 3:
				if tokens[1].isdigit() == True:
					if tokens[1] == '1':
						if authorStats["Position"].lower() == "intern":
							join_date = authorStats["StartDate"]
							cur_date = datetime.now(timezone.utc)
							end_date = authorStats["EndDate"]
							joinStamp = helpers.getTimeStamp(join_date)
							endStamp = helpers.getTimeStamp(end_date)
							time_till_end = end_date - cur_date
							if cur_date < end_date:
								data = data + "You joined " + str(joinStamp) + " and your intership ends " + str(endStamp) + "." + "\n"
								data = data + "You have " + str(int(time_till_end.days / 7)) + " weeks and " + str(time_till_end.days % 7) + " days left."
							else:
								data = data + "Your internship ended " + str(endStamp)
						else:
							data = "It appears that you do not have an end date as you are not an intern."

					elif tokens[1] == '2':
						teamfound = bool(False)
						data = data + "Your team in this server: \n"
						for role in ctx.author.roles:
							if "team" in role.name.lower():
								data = data + role.name + "\n"
								teamfound = True
						if teamfound == False:
							data = "Sorry, I was not able to determine your team."

					elif tokens[1] == '3':
						modfound = bool(False)
						data = data + "The server moderators are: \n"
						members = ctx.guild.members
						for member in members:
							for role in member.roles:
								if "moderat" in role.name.lower():
									data = date + member.global_name + "\n"
									modfound = True
						if modfound == False:
							data = "Sorry, I was unable to find the moderators."

					elif tokens[1] == '4':
						authorTeams = list()
						leadersFound = bool(False)
						data = "Your team leaders are: \n"

						for role in ctx.author.roles:
							if "team" in role.name.lower():
								authorTeams.append(role.name.lower())

						for member in ctx.guild.members:
							for role in member.roles:
								for team in authorTeams:
									if team in role.name:
										data = data + member.global_name + "\n"
										leadersFound = True

						if len(authorTeams) < 1 or leadersFound == False:
							data = "Sorry, I was unable to find your team leaders."

					else:
						print("Error: invalid question [chatbot::ask]")
						data = "Sorry, that number does not match any of my questions."
						
		#if stop is true		
		else:
			data = "Sorry, something went wrong. I could not retrieve member data."
	    
		await ctx.send(data)
	

async def setup(bot):
	await bot.add_cog(chatbot(bot))
