import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone
from datetime import timedelta

class checkup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def 




async def setup(bot):
	await bot.add_cog(checkup(bot))
