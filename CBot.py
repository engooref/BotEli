from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
import requests
import os

##Reaction role
#Function utils
def getKeys(dict, index):
    l = list(dict.keys())
    if index < len(l):
        return l[index]
    else:
        return None

#Variable
emojiDict = {"📢" : 972851340181114891, "📚" : 972846976813133875, "🎥" : 972847038263877653, "😋" : 972847039417319485}

##Twitch
# Authentication with Twitch API.
client_id = "ncmx4zvcrmthjkg4o0nzvwbqn5gmlf"
client_secret = "mn1tdd9shsezcc3j4m48hewpi5hamv"
twitch = Twitch(client_id, client_secret)
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?user_login={}"

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

#data output
keys = r.json()

API_HEADERS = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}

# Returns true if online, false if not.
def checkuser(user):
    try:
        url = TWITCH_STREAM_API_ENDPOINT_V5.format(user)
        try:
            req = requests.get(url, headers=API_HEADERS)
            jsondata = req.json()
            print(jsondata)
            if jsondata["data"]:
                return True
            else:
                return False
        except Exception as e:
            print("Error checking user: ", e)
            return False
    except IndexError:
        return False


class CBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix="*", intents=intents)
        self.messageRole = None

    async def on_ready(self):
        await self.ConfigMessageRole()
        await self.ConfigTwitchStream()
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

    async def ConfigTwitchStream(self):
        usersStream = dict()
        #Key: Username (User.name) = #Value {class User, class Channel, MessDejaEnvoye} 
        usersStream["eli_shouille"] = \
        {"user" : self.get_user(int(os.getenv("ID_ELI"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ELI"))), "alreadySent" : False, "roleChannel" : "🎥"}
        
        usersStream["Zwoumm"] = \
        {"user" : self.get_user(int(os.getenv("ID_ZWOUM"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ZWEY"))), "alreadySent" : False, "roleChannel" : "😋"}
        

        usersStream["dreeeyyy_"] = \
        {"user" : self.get_user(int(os.getenv("ID_DREY"))), "channel" : self.get_channel(int(os.getenv("CHANNEL_TWITCH_ZWEY"))), "alreadySent" : False, "roleChannel" : "😋"}

        @tasks.loop(seconds=10)
        async def live_notifs_loop():
            for keyStream in usersStream:
                userStream = usersStream[keyStream]

                status = checkuser(keyStream)
                print(status)
                if status is True and not userStream["alreadySent"]:
                    await userStream["channel"].send(f"Hey <@&{emojiDict[userStream['roleChannel']]}>, {keyStream} est en live sur https://twitch.tv/{keyStream} ! Hésite pas à passer une tête !")
                userStream["alreadySent"] = status
                
        live_notifs_loop.start()