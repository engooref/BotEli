from ast import For
from re import S
from unicodedata import name
from discord.ext import commands, tasks
import discord, os, datetime
from youtube_dl import YoutubeDL
from time import sleep


def cmd(msg):
    
    return f"**{msg}**"

def argImp(msg):
    return f"*{msg}*"

def warning(msg):
    return f"__{msg}__" 

helpGeneralCmd = {}

authorizedRoles = []

class Listeners(commands.Cog, name='Listeners module'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Purge")
    async def purge(self, ctx):
        await ctx.channel.purge(bulk=False, limit=50000)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        userBot = ctx.message.guild.get_member(int(os.getenv("ID")))

        embedHelpGeneralCmd = discord.Embed(
            colour = discord.Colour.orange(),
            title = "Commandes Général"
        )

        embedHelpGeneralCmd.set_author(name="Help", icon_url=userBot.avatar_url)
        embedHelpGeneralCmd.add_field(name=f"Préfixe des commandes : {self.bot.command_prefix}" , value="\n----------------------------------------", inline=False)
        embedHelpGeneralCmd.add_field(name="Code couleur:" , value=cmd("Commande") + " " + argImp("Argument_obligatoire") + "\n----------------------------------------", inline=False)

        for each_commands in helpGeneralCmd:
            embedHelpGeneralCmd.add_field(name=f"{each_commands}", value=helpGeneralCmd[each_commands] + "\n----------------------------------------", inline=False)

        await ctx.channel.send(author, embed=embedHelpGeneralCmd)


