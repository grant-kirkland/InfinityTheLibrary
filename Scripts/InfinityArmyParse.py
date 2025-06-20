import json
import re

# Convert Ammo type id to descriptive text
def AmmoType(value):
	if (value == "0"):
		return "*"
	elif (value == 0):
		return ""
	elif (value == 2):
		return "N"
	elif (value == 3):
		return "AP"
	elif (value == 5):
		return "N+E/M"
	elif (value == 6):
		return "Exp"
	elif (value == 8):
		return "Shock"
	elif (value == 9):
		return "DA"
	elif (value == 10):
		return "AP+DA"
	elif (value == 13):
		return "AP+Exp"
	elif (value == 14):
		return "E/M"
	elif (value == 18):
		return "T2"
	elif (value == 21):
		return "Smoke"
	elif (value == 22):
		return "Eclipse"
	elif (value == 29):
		return "Stun"
	elif (value == 30):
		return "AP+Shock"
	elif (value == 37):
		return "PARA"
	elif (value == 40):
		return "AP+T2"
	else:
		print(value)
		return value
	
# Formats weapon traits as string
def WeaponTraits(value):
	traits = ""
	for entry in value:
		traits = traits + f"{entry}, "

	return traits[:-2]

# Convert range bands to needed format for TeX macro
def RangeBands(value):
	if (type(value) is dict):
		s = ""
		position = 0
		if ("short" in value.keys()):
			if (type(value["short"]) is dict):
				dist = value["short"]
				iterations = dist["max"] 
				if (iterations > 140):
					iterations = 140
				iterations = iterations // 20
				for i in range(iterations):
					position = position + 1
					s = s + dist["mod"] + " "
		if ("med" in value.keys()):
			if (type(value["med"]) is dict):
				dist = value["med"]
				iterations = dist["max"] 
				if (iterations > 140):
					iterations = 140
				iterations = iterations // 20
				for i in range(iterations - position):
					position = position + 1
					s = s + dist["mod"] + " "
		if ("long" in value.keys()):
			if (type(value["long"]) is dict):
				dist = value["long"]
				iterations = dist["max"] 
				if (iterations > 140):
					iterations = 140
				iterations = iterations // 20
				for i in range(iterations - position):
					position = position + 1
					s = s + dist["mod"] + " "
		if ("max" in value.keys()):
			if (type(value["max"]) is dict):
				dist = value["max"]
				iterations = dist["max"] 
				if (iterations > 140):
					iterations = 140
				iterations = iterations // 20
				for i in range(iterations - position):
					position = position + 1
					s = s + dist["mod"] + " "
		return s[:-1]
	else:
		return " "

# Create LaTeX macro for each weapon given json data
def CreateWeaponMacro(data, file):
	if (type(data) is list):
		# Replace special characters
		name = data[0]["name"].replace("12", "Twelve").replace("2", "Two")
		name = re.sub('[^a-zA-Z]', '', name)
		# Define new latex command
		print(f"\\newcommand{{\\{name}}}[0] {{" , file=file)
		for item in data:
			# Check if profile needs to be printed
			if ("profile" in item.keys()):
				functionContents = (
							f"\t\\InfWeaponWithStatblock{{{item["name"]}}}"
							f"{{{item["profile"]}}}" # Range
							f"{{{item["damage"]}}}" # PS
							f"{{{item["burst"]}}}" # burst
							f"{{{AmmoType(item["ammunition"])}}}" # Ammo
							f"{{{item["saving"]}}}" # attribute
							f"{{{item["savingNum"]}}}" # SR
							f"{{{WeaponTraits(item["properties"])}}}" # Traits
							)
				# Add profile to macro contents
				print(functionContents , file=file)
			functionContents = (
						f"\t\\InfWeaponProfile{{{item["name"]} ({item["mode"]})}}"
						f"{{{RangeBands(item["distance"])}}}" # Range
						f"{{{item["damage"]}}}" # PS
						f"{{{item["burst"]}}}" # burst
						f"{{{AmmoType(item["ammunition"])}}}" # Ammo
						f"{{{item["saving"]}}}" # attribute
						f"{{{item["savingNum"]}}}" # SR
						f"{{{WeaponTraits(item["properties"])}}}" # Traits
						)
			# Add mode to macro contents
			print(functionContents , file=file)
		# close command
		print(f"}}\n" , file=file)

	elif (type(data) is dict):
		# Replace special characters and numbers with usable values
		name = data["name"].replace("12", "Twelve").replace("2", "Two")
		name = re.sub('[^a-zA-Z]', '', name)
		# define new command name
		print(f"\\newcommand{{\\{name}}}[0] {{" , file=file)
		# Setup function macro call, checking if it needs profile printed or range printed
		if ("profile" in data.keys()):
			functionContents = (
						f"\t\\InfWeaponWithStatblock{{{data["name"]}}}"
						f"{{{data["profile"]}}}" # Range
						f"{{{data["damage"]}}}" # PS
						f"{{{data["burst"]}}}" # burst
						f"{{{AmmoType(data["ammunition"])}}}" # Ammo
						f"{{{data["saving"]}}}" # attribute
						f"{{{data["savingNum"]}}}" # SR
						f"{{{WeaponTraits(data["properties"])}}}" # Traits
						)
		else:
			functionContents = (
						f"\t\\InfWeaponProfile{{{data["name"]}}}"
						f"{{{RangeBands(data["distance"])}}}" # Range
						f"{{{data["damage"]}}}" # PS
						f"{{{data["burst"]}}}" # burst
						f"{{{AmmoType(data["ammunition"])}}}" # Ammo
						f"{{{data["saving"]}}}" # attribute
						f"{{{data["savingNum"]}}}" # SR
						f"{{{WeaponTraits(data["properties"])}}}" # Traits
						)
		# Add macro to contents of new command and close command
		print(functionContents , file=file)
		print(f"}}\n" , file=file)

	


# load army data
with open("ArmyData.json", "r") as file:
	data = json.load(file)

# open weapon file to write to
with open("InfinityWeapons.sty", "w") as file:
	previous = data["weapons"][0]
	sequential = 0

	# For every weapon in army data create macro for the weapon
	for index, entry in enumerate(data["weapons"]):
		if (index == 0):
			previous = entry
		elif (previous["name"] == entry["name"]):
			previous.update(entry)
			sequential = sequential + 1
		else:
			if (sequential > 0):
				CreateWeaponMacro(data["weapons"][index-sequential-1:index-1], file)
			else:
				CreateWeaponMacro(data["weapons"][index-1], file)
			sequential=0
			previous = entry

