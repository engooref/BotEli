import CBot
import Listeners
from dotenv import load_dotenv
from datetime import date
import discord, os, sys


load_dotenv("config")

intents = discord.Intents.default()
intents.members = True

bot = CBot.CBot(intents)
bot.remove_command('help')
bot.add_cog(Listeners.Listeners(bot))

bot.run(os.getenv("TOKEN"))
