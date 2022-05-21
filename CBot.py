from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from ReactionRole import ConfigMessageRole
import TwitchStream as ts
import requests
import os

#Variable
emojiDict = {"📢" : 972851340181114891, "📚" : 972846976813133875, "🎥" : 972847038263877653, "😋" : 972847039417319485, "🕺" : 977695523563773962}

class CBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="*", intents=intents)
        self.messageRole = None

    async def on_ready(self):
        self.messageRole = await ConfigMessageRole(self.get_channel(int(os.getenv("CHANNEL_ROLE"))), emojiDict)
        usersStream = dict()
        #Key: Username (User.name) = #Value {class User, class Channel, MessDejaEnvoye} 
        usersStream["eli_shouille"] = \
        {"user" : self.get_user(int(os.getenv("ID_ELI"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ELI"))), "alreadySent" : False, "roleChannel" : "🎥"}

        usersStream["Zwoumm"] = \
        {"user" : self.get_user(int(os.getenv("ID_ZWOUM"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ZWEY"))), "alreadySent" : False, "roleChannel" : "😋"}

        usersStream["dreeeyyy_"] = \
        {"user" : self.get_user(int(os.getenv("ID_DREY"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ZWEY"))), "alreadySent" : False, "roleChannel" : "😋"}

        usersStream["lims984"] = \
        {"user" : self.get_user(int(os.getenv("ID_LIMS"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_LIMS"))), "alreadySent" : False, "roleChannel" : "🕺"}

        await ts.ConfigTwitchStream(usersStream, emojiDict, os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
        print("Le bot est prêt.", flush=True)

    async def on_reaction_add(self, reaction, user):
        if user.id == int(os.getenv("ID")) or reaction.message != self.messageRole:
            return

        role = reaction.message.guild.get_role(emojiDict[reaction.emoji])
        await user.add_roles(role)
        print(f'Ajout du role "{role}" à {user}')


    async def on_reaction_remove(self, reaction, user):
        if user.id == int(os.getenv("ID")) or reaction.message != self.messageRole:
            return

        role = reaction.message.guild.get_role(emojiDict[reaction.emoji])
        await user.remove_roles(role)
        print(f'Retrait du role "{role}" à {user}')

