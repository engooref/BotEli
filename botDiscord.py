from CBot import CBot
from Listeners import Listeners
from dotenv import load_dotenv
import discord, os

load_dotenv("config")

intents = discord.Intents.default()
intents.members = True

bot = CBot(intents)
bot.remove_command('help')
bot.add_cog(Listeners(bot))

bot.run(os.getenv("TOKEN"))
