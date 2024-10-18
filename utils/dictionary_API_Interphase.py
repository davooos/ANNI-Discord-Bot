#Definition object has members definition, example, or synonyms[].
#Word Object has members phonetics
#phonetics object has members Phonetic, audio


from freedictionaryapi.clients.sync_client import DictionaryApiClient
import yaml
import os

blockLocation = "cache/wordCache/"

def writeBlock(word: str()) -> dict():
	partOfSpeech = str()
	definitions = list()
	examples = list()
	synonyms = list()
	
	client = DictionaryApiClient()
	parser = client.fetch_parser(word)
	definit = parser.word
	
	partOfSpeech = definit.meanings[0].part_of_speech
	
	for definition in definit.meanings[0].definitions:
		definitions.append(definition.definition)
		if str(definition.example) != "None" and str(definition.example) != "none":
					examples.append(str(definition.example))
		for synonym in definition.synonyms:
			synonyms.append(synonym)
	#create block		
	#fix this, reads like shit
	block = {"word": word, "partOfSpeech": partOfSpeech, "definitions": definitions, "examples": examples, "synonyms": synonyms}
	
	#create yaml file for block
	file_path = blockLocation + block["word"]
	with open(file_path, 'w') as file:
		yaml.dump(block, file)
	print(f"Data saved to {file_path}")
	
	return block

def load_from_yaml(word: str()) -> dict():
    with open(blockLocation + word, 'r') as file:
        data = yaml.safe_load(file)
    print(f"Data loaded from blocks/{word}")
    return data

def getBlocks() -> list():
	words = list()
	for file in os.listdir(blockLocation):
		words.append(load_from_yaml(str(file)))
	return words

def help() -> str:
	data = str()
	data = data + "Commands: \n"
	data = data + " example [word]\n"
	data = data + " define [word]\n"
	data = data + " synonym [word]\n"

	return data
	
def show() -> str():
	data = "Cached words:\n"
	savedBlocks = getBlocks()
	
	for count, block in enumerate(savedBlocks):
		data = data + str(count) + " : " + block["word"] + "\n"
	
	if len(savedBlocks) == 0:
		data = "No words cached"
	return data
	
def clear() -> bool():
	savedBlocks = getBlocks()
	for block in savedBlocks:
		os.remove(blockLocation + block["word"])
		print("Deleted " + block["word"])

def queary(word: str() or int(), request: str(), limit: bool(), index: bool()) -> str():
	data = str()
	history = bool(False)
	currBlock = dict()
	savedBlocks = getBlocks()
	for count, block in enumerate(savedBlocks):
		if index == True:
			if count == word:
				currBlock = block
				history = True
		else:
			if block["word"] == word:
				currBlock = block
				history = True
			
	if history == False:
		currBlock = writeBlock(word)
		
	data = "Word: " + currBlock["word"] + "\n"
	
	if request == "define":
		for count, definition in enumerate(currBlock["definitions"]):
			if len(data + definition + "\n") < 2000:
				if count > 4 and limit == True:
					data = data + "More available - use 'all' option to view"
					return data
				data = data + definition + "\n"
	elif request == "synonym":
		for count, synonym in enumerate(currBlock["synonyms"]):
			if len(data + synonym + "\n") < 2000:
				if count > 4 and limit == True:
					data = data + "More available - use 'all' option to view"
					return data
				data = data + synonym + "\n"
	elif request == "example":
		for count, example in enumerate(currBlock["examples"]):
			if len(data + example + "\n") < 2000:
				if count > 4 and limit == True:
					data = data + "More available - use 'all' option to view"
					return data
				data = data + example + "\n"
	else:
		print("ERROR: invalid data request [words::queary]")
	
	if data == "Word: " + currBlock["word"] + "\n":
		data = data + "None found"
	return data
	


