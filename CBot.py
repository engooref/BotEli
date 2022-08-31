
from email import message
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
import requests, os, ReactionRole, Log
import TwitchStream as ts

#Variable
emojiDict = {"📢" : 972851340181114891, "📚" : 972846976813133875, "🎥" : 972847038263877653, "😋" : 972847039417319485, "🕺" : 977695523563773962}

class CBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="*", intents=intents)
        self.messageRole = None

    async def on_ready(self):
        Log.PrintLog("\n-------------------------------------------------------\n")
        self.messageRole = await ReactionRole.ConfigMessageRole(self.get_channel(int(os.getenv("CHANNEL_ROLE"))), emojiDict)
        Log.PrintLog(str(self.messageRole))
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

        #await ts.ConfigTwitchStream(usersStream, emojiDict, os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
        Log.PrintLog("Le bot est pret.")

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        user = channel.guild.get_member(payload.user_id)
        emoji = payload.emoji
        message = await channel.fetch_message(payload.message_id)
        if user.id == int(os.getenv("ID")) or message != self.messageRole:
            return

        role = message.guild.get_role(emojiDict[str(emoji)])
        await user.add_roles(role)
        Log.PrintLog(f'Ajout du role "{role}" à {user}')


    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        user = channel.guild.get_member(payload.user_id)
        emoji = payload.emoji
        message = await channel.fetch_message(payload.message_id)

        if user.id == int(os.getenv("ID")) or message != self.messageRole:
            return

        role = message.guild.get_role(emojiDict[str(emoji)])
        await user.remove_roles(role)
        Log.PrintLog(f'Retrait du role "{role}" à {user}')

