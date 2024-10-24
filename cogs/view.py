import utils.helpers as helpers
import discord
from discord.ext import commands
import datetime
from datetime import timezone

class view(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
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
