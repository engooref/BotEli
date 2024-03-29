
from discord.ext import commands
import os, ReactionRole, Log
from TwitchStream import Twitch as ts

#Variable
emojiDict = {"📢" : 972851340181114891, "📚" : 972846976813133875, "🎥" : 972847038263877653, "😋" : 972847039417319485, "🕺" : 977695523563773962, "-1" : "None"}

class CBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="*", intents=intents)
        self.messageRole = None
        self.ts = ts()

    async def on_ready(self):
        self.messageRole = await ReactionRole.ConfigMessageRole(self.get_channel(int(os.getenv("CHANNEL_ROLE"))), emojiDict)
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

        usersStream["engooref"] = \
        {"user" : self.get_user(int(os.getenv("ID_ENGOOREF"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TEST"))), "alreadySent" : False, "roleChannel" : "-1"}

        await self.ts.ConfigTwitchStream(usersStream, emojiDict, os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
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

    async def Stop(self):
        self.ts.StopTwitch()
        Log.PrintLog("Arret du bot")