from datetime import date, datetime
from discord.ext import tasks
import os

dirLog = "./Log"
nbLogFile = 5
nameFile = f'{dirLog}/LogEli_{str(date.today())}'

@tasks.loop(hours=24)
async def LogFile():
    listFile = os.listdir(dirLog)
    while  len(listFile) > nbLogFile:
        PrintLog(f"Delete {listFile[0]}")
        os.remove(f'{dirLog}/{listFile[0]}')
        listFile = os.listdir(dirLog)

LogFile.start()

def Start():
    with open(nameFile, 'a') as f:
            f.write(f"\n---------------------------------------------------\n\n")   


def PrintLog(str):
    with open(nameFile, 'a') as f:
        f.write(f"{datetime.now()} - {str} \n")

