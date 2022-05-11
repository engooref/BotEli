
##Reaction role
#Function utils
def getKeys(dict, index):
    l = list(dict.keys())
    if index < len(l):
        return l[index]
    else:
        return None
  
async def ConfigMessageRole(channelRole, emojiDict):
    contentMessRole = f"Ｎｏｔｉｆｉｃａｔｉｏｎｓ :\n\n{getKeys(emojiDict, 0)} : 𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗𝚜 \
    \n\n{getKeys(emojiDict, 1)} : 𝙰𝚟𝚊𝚗𝚌𝚎𝚖𝚎𝚗𝚝 𝚍𝚞 𝚙𝚛𝚘𝚓𝚎𝚝\n\n{getKeys(emojiDict, 2)} : 𝚃𝚠𝚒𝚝𝚌𝚑\n\n{getKeys(emojiDict, 3)} : 𝚉𝚠𝚎𝚢"

    messagesChannel = await channelRole.history().flatten()

    for message in messagesChannel:
        if message.content == contentMessRole:
            await message.delete()

    messageRole = await channelRole.send(contentMessRole)
    for emoji in emojiDict:
        await messageRole.add_reaction(emoji)

    return messageRole
