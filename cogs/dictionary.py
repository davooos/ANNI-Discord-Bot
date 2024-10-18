from utils.dictionary_API_Interphase import *
import discord
from discord.ext import commands
import os

class dictionary(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="d", description="short hand for define function")
	async def d(self, ctx): #alias to define function
		await self.define(ctx) #call function
		
	@commands.command(name="e", description="short hand for example function")
	async def e(self, ctx): #alias to example function
		await self.example(ctx)
	
	@commands.command(name="s", description="short hand for synonym function")
	async def s(self, ctx): #alias to synonym function
		await self.synonym(ctx)
		
	@commands.command(name="c", description="short hand for cache function")
	async def c(self, ctx): #alias to cache function
		await self.cache(ctx)
	
	@commands.command(name="define", description="Returns definitions for a given word")
	async def define(self, ctx):
		tokens = ctx.message.content.split() #splits message body into a list of words
		word = tokens[1] #word to define will be the second word in the list
		limitOutput = True #flag to limit the output to 5. Default is true which is changed by the command option [all]
		index = False #flag to tell function to find word based on it's index in cache
		
		if tokens[1].isdigit():
			index = True 
			word = int(word)
		else:
			word = word.lower() #convert word to lowercase for API
		
		if len(tokens) > 2:
			if tokens[2] == "all":
				limitOutput = False
		
		data = queary(word, "define", limitOutput, index) #queary is a function in words.py that will return data requested by the second arg
		await ctx.send(str(data))
		
	@commands.command(name="synonym", description="Returns synonyms for a given word")
	async def synonym(self, ctx):
		tokens = ctx.message.content.split()
		word = tokens[1]
		limitOutput = True
		index = False
		
		if tokens[1].isdigit():
			index = True
			word = int(word)
		else:
			word = word.lower()
			
		if len(tokens) > 2:
			if tokens[2] == "all":
				limitOutput = False
		
		data = queary(word, "synonym", limitOutput, index)
		await ctx.send(str(data))
		
        
	@commands.command(name="example", description="Returns examples for a given word")
	async def example(self, ctx):
		tokens = ctx.message.content.split()
		word = tokens[1]
		limitOutput = True
		index = False

		if tokens[1].isdigit():
			index = True
			word = int(word)
		else:
			word = word.lower()
			
		if len(tokens) > 2:
			if tokens[2] == "all":
				limitOutput = False
		
		data = queary(word, "example", limitOutput, index)
		await ctx.send(str(data))
		
	@commands.command(name="cache", description="Returns current cache")
	async def cache(self, ctx):
		data = str() #str that will be sent as a discord message
		tokens = ctx.message.content.split()
		if len(tokens) == 1: #if no args are given
			data = "Cache command options:\n  'show' -> show cached words\n  'clear' -> clear cache\n"
		else:
			if len(tokens) == 2:
				if tokens[1] == "show":
					data = show() #function if words.py that returns a str that lists the cached words
				elif tokens[1] == "clear":
					clear() #function that deletes all word cache files
					data = "Word cache cleared"
				else:
					data = "Unknown option used"
			else:
				data = "Too many options"
			
		await ctx.send(str(data))

async def setup(bot):
	await bot.add_cog(dictionary(bot))
