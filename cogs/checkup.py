import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
<<<<<<< HEAD
from datetime import timezone
from datetime import timedelta
=======
from datetime import tzinfo, timedelta, datetime, timezone

>>>>>>> 07344c8 (Make createLog function set endDate if intern role is found)

class checkup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
<<<<<<< HEAD
		
	@commands.command()
	async def 
=======

	async def msg(self) -> None:
		pass
		
	async def runCheck(self, ctx) -> None:
		



>>>>>>> 07344c8 (Make createLog function set endDate if intern role is found)




async def setup(bot):
<<<<<<< HEAD
	await bot.add_cog(checkup(bot))
=======
	await bot.add_cog(chatbot(bot))
>>>>>>> 07344c8 (Make createLog function set endDate if intern role is found)
