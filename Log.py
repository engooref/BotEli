import sys
from datetime import date

def PrintLog(str):
    with open('LogEli_' + date.today().strftime("%d_%m_%Y"), 'a') as f:
        f.write(str + '\n')