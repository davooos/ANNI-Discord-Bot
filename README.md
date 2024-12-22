# NAME: Childhood Cancer Society Discord Bot
# BOT VERSION: 1.0

## ABOUT:
	This is a discord bot created for the Childhood Cancer Society non-profit.
	The purpose of this bot is to aid managers with managing team members.
	Some of these tasks may involve getting progress reports from members, or
	answering common questions for organization members.

## FILE STRUCTURE:
	./cache/ -> Directories holding data saved by bot.
	./cogs/ -> COG files. Each file in this directory is loaded at startup.
	./documentation/ -> text files that contain command documentation. Used by help COG.
	./main.py -> Bot setup file that is run to start bot.
	./utils/ -> Contains python helper scripts with functions for use in COGS.
	./utils/helpers.py -> Main helper file with functions to be used by any or all COGS.
	./.archived/ -> Depreciated code. 
	
## PROJECT SPECIFICATIONS:
	- The bot uses python 3.13
	- Bot currently uses YAML to save data to files.
		- Functions used by COGS to save and load files are found in ./utils/helpers.py

## Getting Started:
	The bot uses Python 3.13.
	Start setup by creating a Python virtual environment in the root of the project directory.
	Then, install the following dependancies: 
		- pyyaml
		- discord
		- httpx
		- audioop-lts
		- apscheduler
		
	A YAML file named '.bot.yaml' must also be created in the root directory with the line: 
		token: YOUR_BOT_TOKEN

	Now, you can start the bot by running the python interpreter with the main.py file.
	
## GENERAL USAGE:
	The command prefix for this bot is '!'.
	In your server with the bot installed; use the '!how' command to get general commands
	as well as full documentation for commands.

