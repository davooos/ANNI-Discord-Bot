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
	    questions = dict(helpers.loadConfig("questions"))
	    data = str()
	    tokens = ctx.message.content.split()
	    
	    if len(tokens) < 2:
	        for key in questions:
	            data = data + str(key) + ": " + str(questions[key]) + "\n"
	        data = data + "Enter !ask + the number of the question you wish to ask me!"

	    elif len(tokens) < 3:
	    	if tokens[1].isdigit() == True:
	    		if tokens[1] == '1':
	    			period = timedelta(weeks=16)
	    			join_date = ctx.author.joined_at
	    			cur_date = datetime.now(timezone.utc)
	    			end_date = join_date + period #overload operator for datetime that returns timedelta obj
	    			time_till_end = end_date - cur_date
	    			joinStamp = helpers.getTimeStamp(join_date)
	    			endStamp = helpers.getTimeStamp(end_date)
	    			if time_till_end.seconds > 0:
	    				data = data + "You joined " + str(joinStamp) + " and your intership ends " + str(endStamp) + "." + "\n"
	    				data = data + "You have " + str(int(time_till_end.days / 7)) + " weeks and " + str(time_till_end.days % 7) + " days left."
	    			else:
	    				data = data + "Your internship ended " + str(end_date)

	    		elif tokens[1] == '2':
	    			data = data + "Your roles in this server include: \n"
	    			for role in ctx.author.roles:
	    				if role.name != "@everyone":
	    					data = data + role.name + "\n"
	    		else:
	    			print("Error: invalid question [chatbot::ask]")
	    			data = "Sorry, that number does not match any of my questions."
	    
	    await ctx.send(data)
	

async def setup(bot):
	await bot.add_cog(chatbot(bot))
