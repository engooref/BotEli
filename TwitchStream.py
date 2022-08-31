import asyncio
import requests
from discord.ext import tasks
from datetime import datetime
import Log
from threading import Thread

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?user_login={}"

async def ConfigTwitchStream(usersStream, emojiDict, client_id, client_secret):

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


        def checkuser(user): 
            try: 
                url = TWITCH_STREAM_API_ENDPOINT_V5.format(user) 
                try: 
                    req = requests.get(url, headers=API_HEADERS) 
                    jsondata = req.json() 
                    if jsondata["data"]:
                            return True 
                    else: 
                            return False 
                except Exception as e: 
                    print("Error checking user: ", e) 
                    return False
            except IndexError:
                return False

        async def live_notifs_loop():
            try:
                while 1:
                    for keyStream in usersStream:
                        userStream = usersStream[keyStream]

                        status = checkuser(keyStream)
                        if status is True and not userStream["alreadySent"]:
                            await userStream["channel"].send(f"Hey <@&{emojiDict[userStream['roleChannel']]}>, {keyStream} est en live sur https://twitch.tv/{keyStream} ! Hésite pas à passer une tête !")
                        userStream["alreadySent"] = status
                        Log.PrintLog(f'{datetime.now()} - User: {keyStream}, status: {userStream["alreadySent"]}')
                    await asyncio.sleep(10)
            except:
                pass

        def launch_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(live_notifs_loop())
            loop.close()
        
        thread = Thread(target=launch_loop, args=())
        thread.start()