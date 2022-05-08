from email import message
from discord.ext import commands
from twitchAPI.twitch import Twitch
import os

#Function utils
def getKeys(dict, index):
    l = list(dict.keys())
    if index < len(l):
        return l[index]
    else:
        return None

#Variable
emojiDict = {"📢" : 972638507006820452, "📚" : 972638546592677888, "🎥" : 972602143150321674, "😋" : 972602353154949170}

class CBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="*", intents=intents)
        self.messageRole = None

    async def on_ready(self):
        self.configMessageRole()
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

    async def ConfigMessageRole(self):
        channelRole = self.get_channel(int(os.getenv("CHANNEL_ROLE")))


        contentMessRole = f"Ｎｏｔｉｆｉｃａｔｉｏｎｓ :\n\n{getKeys(emojiDict, 0)} : 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗𝚜 \
        \n\n{getKeys(emojiDict, 1)} : 𝙰𝚟𝚊𝚗𝚌𝚎𝚖𝚎𝚗𝚝 𝚍𝚞 𝚙𝚛𝚘𝚓𝚎𝚝\n\n{getKeys(emojiDict, 2)} : 𝚃𝚠𝚒𝚝𝚌𝚑\n\n{getKeys(emojiDict, 3)} : 𝚉𝚠𝚎𝚢"

        messagesChannel = await channelRole.history().flatten()
        
        for message in messagesChannel:
            if message.content == contentMessRole:
                await message.delete()

        self.messageRole = await channelRole.send(contentMessRole)
        for emoji in emojiDict:
            await self.messageRole.add_reaction(emoji)