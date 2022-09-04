import asyncio, requests, threading
import Log

class Twitch():
    def __init__(self):
        self.TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?user_login={}"
        self.thread = None

    def StopTwitch(self):
        self.thread.Stop()
        self.thread.join()
        
    async def ConfigTwitchStream(self, usersStream, emojiDict, client_id, client_secret):

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

        mainLoop = asyncio.get_event_loop()

        def checkuser(user): 
            try: 
                url = self.TWITCH_STREAM_API_ENDPOINT_V5.format(user) 
                try: 
                    req = requests.get(url, headers=API_HEADERS) 
                    jsondata = req.json() 
                    if jsondata["data"]:
                            return True 
                    else: 
                            return False 
                except Exception as e: 
                    Log.PrintLog("Error checking user: ", e) 
                    return False
            except IndexError:
                return False


        class threadTwitch(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.threadIsOn = True

            def run(self):
                Log.PrintLog("Thread Twitch Start")
                while self.threadIsOn:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.live_notifs_loop())
                    loop.close()
                Log.PrintLog("Thread Twitch Stop")

            async def live_notifs_loop(self):
                        try:
                            while self.threadIsOn:
                                for keyStream in usersStream:
                                    userStream = usersStream[keyStream]

                                    status = checkuser(keyStream)
                                    if status is True and not userStream["alreadySent"]:
                                        str = f"Hey <@&{emojiDict[userStream['roleChannel']]}>, {keyStream} est en live sur https://twitch.tv/{keyStream} ! Hésite pas à passer une tête !"
                                        asyncio.run_coroutine_threadsafe(self.SendMessage(str, userStream["channel"]), mainLoop)
                                    userStream["alreadySent"] = status
                                    Log.PrintLog(f'User: {keyStream}, status: {userStream["alreadySent"]}')
                                await asyncio.sleep(10)
                        except Exception as e:
                            Log.PrintLog(str(e))
            
            async def SendMessage(self, str, channel):
                await channel.send(str)

            def Stop(self):
                self.threadIsOn = False

        self.thread = threadTwitch()
        self.thread.start()

