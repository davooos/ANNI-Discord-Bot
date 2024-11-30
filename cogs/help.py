import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone
from datetime import timedelta

class help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	def createMessage(self, authorize: bool(), option: int() = None) -> str():
	    data = str()
	    commandInstruction = "\nCopy the below command and replace values in [] with chosen values.\n\n"
	    generalInstruction = "\nEnter !how followed by the number corresponding to an action above.\n"
	    
	    #flag variables
	    stop = bool(False)
	
	    #options for display
	    basic = {
	        1: "Make an alert that a meeting will be late",
	        2: "Change/add my birthday to Anni"
	    }
	    basicCommands = {
	        1: "!alert minute [number of minutes]",
	        2: "!memberconfig [Your Name] birthday [YYYY-MM-DD]"
	    }
	    restricted = {
	        3: "Change intern/associate start date",
	        4: "Change intern/associate end date",
	        5: "Change member position(role in company)",
	        6: "Schedule a day and time for Anni to remind interns to post updates (EST)",
	        7: "Remove scheduled time for Anni to remind interns"
	    }
	    restrictedCommands = {
	        3: "!memberconfig [Name or ID] startDate [YYYY-MM-DD]",
	        4: "!memberconfig [Name or ID] endDate [YYYY-MM-DD]",
	        5: "!memberconfig [Name or ID] position [intern/volunteer/alumni]",
	        6: "!schedule [day] [hour:minute]\n\nHour and minute using the 24-hour clock.",
	        7: "!schedule remove [Job ID]\n\nGet Job ID from:\n!schedulecheck"
	    }
	    
	    if authorize == False:
	        if option == None:
	            for i in basic:
	                data = data + str(i) + ": " +  basic[i] + "\n"
	            data = data + generalInstruction
	        else:
	            if option <= len(basic):
	                data = commandInstruction + basicCommands[option-1] #Add minus one to accomodate for index initial value of 0
	            else:
	                stop = True
	                print("Error, invalid index given to createMessage [help::createMessage]")
	                
	    elif authorize == True:
	        if option == None:
	            for i in basic:
	                data = data + str(i) + ": " + basic[i] + "\n"
	            for i in restricted:
	                data = data + str(i) + ": " + restricted[i] + "\n"
	            data = data + generalInstruction
	        else:
	            if option <= len(basic) + len(restricted):
	                if option <= len(basic):
	                    data = commandInstruction + basicCommands[option]
	                else:
	                    data = commandInstruction + restrictedCommands[option]
	                    
	    else:
	        stop = True
	        print("Error, authorization has invalid value [help::createMessage]")
	        
	    if stop == True:
	        data = "Sorry, something went wrong"
	    
	    return data
	            
	            
	            
		
	@commands.command(name="how", description="Gives examples of how to use commands")
	async def how(self, ctx) -> None:
		stripped = ctx.message.content.replace("[","").replace("]","")
		tokens = stripped.split() #split discord message into words and remove spaces
		authorized = helpers.checkAuth(ctx.author) #check authorization
		data = str()

		#flag variables
		stop = bool(False)

		if len(tokens) == 1:
			data = self.createMessage(authorized)
		elif len(tokens) == 2:
			if tokens[1].isdigit():
				data = self.createMessage(authorized, int(tokens[1]))
			else:
				stop = True
				print("Error, Invalid index given for command example [help::how]")
		else:
			stop = True
        
		if stop == False:
			await ctx.send(data)
		else:
			print("Error, Too many arguments sent to how command [help::how]")
			data = "Sorry, I was not able to interpret your command"
			await ctx.send(data)
	    
	    
async def setup(bot):
	await bot.add_cog(help(bot))