import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import tzinfo, timedelta, datetime, timezone

class checkup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def msg(self, memberid: int(), leaderid: int() = None, ctx) -> None:
		pass
		
	@commands.command(name = "runcheck", description = "runs the checkup reminder for interns")
	async def runcheck(self, ctx) -> None:
        data = str()
        members = ctx.guild.members
        log = helpers.loadCache("members","MemberData")
        #check authorization
		authorized = helpers.checkAuth(ctx.author)
		
		#temp variables
		memberid = int(0)
		leaderid = int(0)
		
		#flag variables
		stop = bool(False)
		
		for m in log:
		    if log[m]["Position"] == "intern" and log[m]["EndDate"] > log[m]["StartDate"]:
		        data = "Hey there, I hope your week has been going well! Don't forget to submit your weekly report to your team leader!\n"
		        if log[m]["Team Leader"] != None:
					data = data + "Your team leader is " + log[m]["Team Leader"]
		        
		        for member in members:
					if member.id == m:
						await member.send(data)
		        



async def setup(bot):
	await bot.add_cog(checkup(bot))
