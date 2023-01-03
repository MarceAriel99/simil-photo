from datetime import datetime

CURRENT_DIRECTORY = 'E:/Mis_Archivos/Proyects/Programs/SimilPhoto/Program/'
LOGS_PATH = 'logs.txt'

def log(message):
	
	with open (CURRENT_DIRECTORY+LOGS_PATH, "a+") as file:
		file.write(datetime.today().strftime("%d/%m/%Y-%X") + " - " + message + "\n")