## NAME: Childhood Cancer Society Discord Bot
## BOT VERSION: 1.0

#### GitHub Link: [CCS Bot Repository](https://github.com/ChildhoodCancerSociety/ANNI-Discord-Bot)

### ABOUT:
This is a Discord bot created for the Childhood Cancer Society non-profit organization.  
The purpose of this bot is to help managers manage team members.  
Some of these tasks may involve gathering progress reports from members or answering common questions from the organization's members.

### FILE STRUCTURE:
- `./cache/` -> Directories holding data saved by the bot. 
- `./cache/GoogleAPI/` -> Directory that houses API token and credentials for the Google API.
- `./cache/Links/` -> YAML files that store meeting links(URLs) for link COG.
- `./cache/MemberData/` -> File including server and member data(created by view COG).
- `./config/` -> Configuration files for the COGs. 
- `./cogs/` -> COG files. Each file in this directory is loaded at startup.  
- `./doc/` -> Text files that contain command documentation. These are used by the help COG.  
- `./utils/` -> Contains Python helper scripts with functions for use in COGS.  
- `./utils/helpers.py` -> Main helper file with functions to be used by any or all COGS.
- `./requirements.txt` -> File that specifies project dependancies.
- `./main.py` -> Bot setup file that is run to start the bot.    

### PROJECT SPECIFICATIONS:
- This project uses Python 3.11. 
- Project dependencies are specified in the `requirements.txt` file. 
- This project currently uses YAML to save data to files.
  - Functions used by COGS to save and load files are found in `./utils/helpers.py`.

### GETTING STARTED:
1. Start by cloning repository to your system:
   - `git clone https://github.com/ChildhoodCancerSociety/ANNI-Discord-Bot`
2. Create a Python virtual environment in the root of the project directory(BASH/UNIX):
   - `python -m venv .venv`
3. Activate the virtual environment(BASH/UNIX):
   - `. .venv/bin/activate`
4. Then, install the following dependencies within the virtual environment(BASH/UNIX):
   - `.venv/bin/pip install -r requirements.txt`
5. A file named `.env` must also be created in the root of the project directory with the following line inside:
   - `token=YOUR_BOT_TOKEN`
6. Now, you can start the bot by running the `main.py` file with the Python interpreter:
   - `.venv/bin/python main.py`

### GENERAL USAGE:
The command prefix for this bot is `!`.  
In your server with the bot installed, use the `!how` command to get general commands and full documentation for commands. You can also view the files in `./doc/` of the project for full command instructions.
