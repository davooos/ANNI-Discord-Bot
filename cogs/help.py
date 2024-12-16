import utils.helpers as helpers
import utils.documentation as document
import discord
from discord.ext import commands

class help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	def createMessage(self, authorize: bool(), option: int() = None) -> str():
		data = str()
		#general messages
		commandInstruction = "\nCopy the below command and replace values in [] with chosen values.\n\n"
		generalInstruction = "\nEnter !how followed by the number corresponding to an action above.\n"
	    
		#flag variables


		#options for display
		basic = {
			"Get a detailed explanation for a command" : "!how explain [index]\nGet index with: !how explain",
			"Make an alert that a meeting will be late" : "!alert minute [number of minutes]",
			"Change/add my birthday to Anni" : "!memberconfig [Your Name] birthday [YYYY-MM-DD]",
			"Ask Anni a question about the organization or job" : "!ask"
		}
		restricted = {
			"Change intern/associate start date" : "!memberconfig [Name or ID] startDate [YYYY-MM-DD]",
			"Change intern/associate end date" : "!memberconfig [Name or ID] endDate [YYYY-MM-DD]",
			"Change member position(role in company)" : "!memberconfig [Name or ID] position [intern/volunteer/alumni]",
			"Schedule a day and time for Anni to remind interns to post updates (EST)" : "!schedule [day] [hour:minute]\n\nHour and minute using the 24-hour clock.",
			"Remove scheduled time for Anni to remind interns" : "!schedule remove [Job ID]\n\nGet Job ID from:\n!schedulecheck"
		}

		#check authorization
		if authorize == False:
			if option == None:
				for idx,i in enumerate(basic): #iterate through a range of numbers the length of the question list
					data = data + str(idx) + ": " + i + "\n"
				data = data + generalInstruction
			else:
				if option < len(basic):
					for idx,op in enumerate(basic): #iterate through basic dictionary to find searched value
						if option == idx:
							data = commandInstruction + basic[op]
				else:
					data = "Sorry, It appears that I do not have a question for that number."
					print("Error, invalid index given to createMessage [help::createMessage]")

		elif authorize == True:
			if option == None:
				for idx,i in enumerate(basic):
					data = data + str(idx) + ": " + i + "\n"
				for idx,r in enumerate(restricted): 
					#start counting at the length of basic for index
					data = data + str(idx + len(basic)) + ": " + r + "\n"
				data = data + generalInstruction
			else:
				if option < len(basic) + len(restricted):
					if option < len(basic):
						for idx,op in enumerate(basic): #iterate through basic dictionary to find searched value
							if option == idx:
								data = commandInstruction + basic[op]
					else:
						for idx,op in enumerate(restricted): #iterate through restricted dictionary to find searched value
							if option - len(basic) == idx:
								data = commandInstruction + restricted[op]
				else:
					data = "Sorry, It appears that I do not have a question for that number."
					print("Error, invalid index given to createMessage [help::createMessage]")

		else:
			data = "Sorry, something went wrong. I was unable to process the command."
			print("Error, authorization has invalid value [help::createMessage]")

		return data
	            
	            
	            
		
	@commands.command(name="how", description="Gives examples of how to use commands")
	async def how(self, ctx) -> None:
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split() #split discord message into words and remove spaces
		authorized = helpers.checkAuth(ctx.author) #get authorization status
		data = str()

		#flag variables
		stop = bool(False)

		if len(tokens) == 1:
			data = self.createMessage(authorized)
		elif len(tokens) == 2:
			if tokens[1].isdigit():
				data = self.createMessage(authorized, int(tokens[1]))
			elif tokens[1] == "explain":
				data = document.getdoc(None) #returns a list of commands with indexes
			else:
				stop = True
				print("Error, Invalid index given for command example [help::how]")
		elif len(tokens) == 3:
			if tokens[2].isdigit() == True:
				data = document.getdoc(tokens[2])
		else:
			stop = True
        
		if stop == False:
			await ctx.send(data)
		else:
			print("Error, Too many or invalid arguments sent to how command [help::how]")
			data = "Sorry, I was not able to interpret your command"
			await ctx.send(data)
	    
	    
async def setup(bot):
	await bot.add_cog(help(bot))