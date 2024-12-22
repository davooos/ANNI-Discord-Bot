## NAME: Childhood Cancer Society Discord Bot
## BOT VERSION: 1.0

### ABOUT:
This is a Discord bot created for the Childhood Cancer Society non-profit organization.  
The purpose of this bot is to help managers manage team members.  
Some of these tasks may involve getting progress reports from members or answering common questions from the organizations' members.

### FILE STRUCTURE:
- `./cache/` -> Directories holding data saved by the bot.  
- `./cogs/` -> COG files. Each file in this directory is loaded at startup.  
- `./documentation/` -> Text files that contain command documentation. These are used by the help COG.  
- `./main.py` -> Bot setup file that is run to start the bot.  
- `./utils/` -> Contains Python helper scripts with functions for use in COGS.  
- `./utils/helpers.py` -> Main helper file with functions to be used by any or all COGS.  
- `./.archived/` -> Deprecated code.  

### PROJECT SPECIFICATIONS:
- The bot uses Python 3.13.  
- The bot currently uses YAML to save data to files.
  - Functions used by COGS to save and load files are found in `./utils/helpers.py`.

### GETTING STARTED:
1. Start setup by creating a Python virtual environment in the root of the project directory.
2. Then, install the following dependencies:
    - `pyyaml`
    - `discord`
    - `httpx`
    - `audioop-lts`
    - `apscheduler`
3. A YAML file named `.bot.yaml` must also be created in the root directory with the following line:  
   `token: YOUR_BOT_TOKEN`
4. Now, you can start the bot by running the `main.py` file with the Python interpreter.

### GENERAL USAGE:
The command prefix for this bot is `!`.  
In your server with the bot installed, use the `!how` command to get general commands and full documentation for commands.