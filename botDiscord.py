import CBot, Listeners, Log
from dotenv import load_dotenv
import discord, os

Log.Start()

load_dotenv("config")

intents = discord.Intents.default()
intents.members = True

bot = CBot.CBot(intents)
bot.remove_command('help')
bot.add_cog(Listeners.Listeners(bot))

bot.run(os.getenv("TOKEN"))
