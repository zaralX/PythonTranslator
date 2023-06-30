from colorama import Fore, Back
import os
import math
import re
from googletrans import Translator
from time import sleep

def get_all_files(path):
	folder_data = next(os.walk(path), (None, None, []))
	export = []
	for f in folder_data[2]:
		export.append(path+"\\"+f)
	for f in folder_data[1]:
		export += get_all_files(path=path+"\\"+f)
	return export

onlyfiles = get_all_files(input("Folder [some_folder]: "))
print("\nLoaded files in current directory\n------------------------------\n"+str(onlyfiles)+"\n------------------------------\n")

file_type = input("File format [php]: ")
translate_in = input("Translate IN [=> ']: ")
translate_out = input("Translate OUT [']: ")

translate_lang_src = input("Translate LANG from [en]: ")
translate_lang_dest = input("Translate LANG to [ru]: ")

filtered_files = []

for f in onlyfiles:
	if f.split(".")[-1] == file_type:
		filtered_files.append(f)


print("\nSelected files\n------------------------------\n"+str(filtered_files)+"\n------------------------------\n")

while True:
	print("Start editing? [y]")
	if input() == "y":
		break

os.system('cls')

print("Initializing...")

translator = Translator()

# Example: progressbar(90, 100, [10, 74, 83, 85])
prog_size = 50
def progressbar(current, maxx, errors):
	draw_size = math.ceil(current/(maxx/prog_size))
	print(Fore.WHITE+"[", end='')

	for x in range(prog_size):
		print(Fore.GREEN, end='')
		if x <= draw_size:
			error = False
			for i in errors:
				if i == x*(maxx/prog_size):
					print(Fore.RED+"█", end='')
					error=True
					break
				elif i == math.floor(x*(maxx/prog_size)):
					print(Fore.RED+"█", end='')
					error=True
					break
			if error == False:
				print("█", end='')
		else:
			print(Fore.BLACK+"█", end='')

	print(Fore.WHITE+"]", end=' ')
	print(Fore.YELLOW+str(current)+" / "+str(maxx)+Fore.WHITE)

edit_errors = []
edit_errors_full = []

# Проверка содержимого перевода
for i in range(len(filtered_files)):
	finded = False
	if translate_in in open(filtered_files[i], "r", encoding='utf-8').read() and translate_out in open(filtered_files[i], "r", encoding='utf-8').read():
		finded = True
		break
	else:
		finded = False
	if finded == False:
		edit_errors.append(i)
		edit_errors_full.append({"Error_position": i, "Error_file": filtered_files[i], "Error_name": "The file does not contain a translation points"})

	os.system('cls')
	print(Fore.BLUE+"Finding bugs..")
	progressbar(i+1, len(filtered_files), edit_errors)

if edit_errors != []:
	while True:
		print("Были найдены не значительные ошибки [y - skip / n - stop and get debug]")
		d = input()
		if d == "y":
			edit_errors = []
			break
		elif d == "n":
			break

if edit_errors == []:
	input(Fore.YELLOW+"Нажмите ENTER для Начала редактирования..."+Fore.WHITE)
	for x in range(len(filtered_files)):
		os.system('cls')
		print(Fore.BLUE+"Editing files...")
		progressbar(x+1, len(filtered_files), edit_errors)
		try:
			text = open(filtered_files[x], "r", encoding="utf-8").read()
			parts = re.findall(translate_in+'([\s\S]+?)'+translate_out, text)

			translated_parts = []
			for part in parts:
				part.replace('\\\'', '\'')
				translated_part = translator.translate(part, src=translate_lang_src, dest=translate_lang_dest).text
				os.system('cls')
				print(Fore.BLUE+"Editing files...")
				progressbar(x+1, len(filtered_files), edit_errors)
				print(part+" -> "+translated_part)
				translated_parts.append(translated_part)
			
			for i in range(len(parts)):
				translated_parts[i].replace('\'', '\\\'')
				text = text.replace(str(parts[i]), str(translated_parts[i]), 2)

			open(filtered_files[x], "w", encoding="utf-8").write(text)
		 

		 
		# If there is any permission issue
		except PermissionError:
			print(Fore.RED+"Permission denied."+Fore.WHITE)
		 
		# For other errors
		except Exception as e:
			print(Fore.RED+"Error occurred while editing file."+Fore.WHITE)
			print(e)
else:
	print(Fore.RED+"\n\n!!!FINDED CRITICAL ERRORS!!!")
	s = 0
	for error in edit_errors_full:
		s+=1
		print("\n")
		print(f"     <---  ERROR {s}  --->     \n")
		print(f" <!> POSITION: {error['Error_position']}")
		print(f" <!> FILE: {error['Error_file']}")
		print(f" <!> NAME: {error['Error_name']}")
input(Fore.YELLOW+"Нажмите ENTER для завершения..."+Fore.WHITE)