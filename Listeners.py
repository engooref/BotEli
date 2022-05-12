from discord.ext import commands, tasks
import discord, os


def cmd(msg):
    
    return f"**{msg}**"

def argImp(msg):
    return f"*{msg}*"

def warning(msg):
    return f"__{msg}__" 

helpGeneralCmd = {cmd("Message") + " " + argImp("mess") : "Permet d'envoyer un message avec le bot"}

authorizedRoles = ["Mangaka"]

class Listeners(commands.Cog, name='Listeners module'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Message")
    async def message(self, ctx):
        
        message = ctx.message.content[len("*Message") : ]
        await ctx.channel.send(message)
        await ctx.message.delete()
        
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
