import datetime
from datetime import timezone
import yaml
from pathlib import Path

def saveConfig(fileName: str(), data: dict()) -> None:
	formattedPath = Path("config/" + fileName) #Converts file path to OOP path
	if formattedPath.exists():
		formattedPath.unlink()
		print("Config file has been deleted for replacement [saveConfig]")
	
	with open(formattedPath, "w") as file:
		yaml.dump(data,file)
		print("Written config file [saveConfig]")
		
def loadConfig(fileName: str()) -> dict():
	data = dict() #variable used to store config from file
	formattedPath = Path("config/" + fileName)	#Converts file path to OOP path
	if formattedPath.exists():
		with open(formattedPath, "r") as file:
			data = yaml.safe_load(file)
			print("Data loaded from config for " + fileName + " successfully [loadConfig]")
	else:
		print("Config file does not exist [loadConfig]")
		
	return data
	
def timeMod(zone: str()) -> int():
	zones = {"EST": -5,"EDT": -4,"CST": -6,"CDT": -5,"MST": -7,"MDT": -6,"PST": -8,"PDT": -7}
	return zones[zone.upper()]
	
	
