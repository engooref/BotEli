from dotenv import load_dotenv
from time import sleep
import CBot, Git, Listeners, Log
import asyncio, discord, os, threading

load_dotenv("config")

Log.Start()



class App():
    def __init__(self):
        Log.PrintLog("Lancement de l'App")
        self.threadBot = None
        self.bot = None
        self.loop = None
        self.threadGit = Git.ThreadGit()

        self.LaunchBot()
        self.threadGit.start()
        self.Run()

    def LaunchBot(self):
        Log.PrintLog("Lancement du Bot")
        intents = discord.Intents.default()
        intents.members = True

        self.bot = CBot.CBot(intents)
        self.bot.remove_command('help')
        self.bot.add_cog(Listeners.Listeners(self.bot))

        self.loop = asyncio.get_event_loop()
        print(self.loop)
        self.loop.create_task(self.bot.start(os.getenv("TOKEN")))
        self.threadBot = threading.Thread(target=self.loop.run_forever)
        self.threadBot.start()

    async def StopBot(self):
        await self.bot.Stop()
        self.loop.stop()
        self.threadBot.join()
        Log.PrintLog("Arret du bot")

    def Run(self):     
        while 1:
            if Git.gitUpdateVal:
                asyncio.run_coroutine_threadsafe(coro=self.StopBot(), loop=asyncio.get_event_loop())
                sleep(25)
                self.LaunchBot()
                Git.gitUpdateVal = False

app = App()



