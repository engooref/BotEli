import requests

##Twitch
# Authentication with Twitch API.
client_id = os.getenv("CLIENT_ID") "ncmx4zvcrmthjkg4o0nzvwbqn5gmlf"
client_secret = os.getenv("CLIENT_SECRET") "mn1tdd9shsezcc3j4m48hewpi5hamv"

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?user_login={}"

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
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

async def ConfigTwitchStream(usersStream, emojiDict):
      r = requests.post('https://id.twitch.tv/oauth2/token', body)

      #data output
      keys = r.json()

      API_HEADERS = {
          'Client-ID': client_id,
          'Authorization': 'Bearer ' + keys['access_token']
      }
     
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
