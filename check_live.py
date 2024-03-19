import requests
def check_live(channelName):
    contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')

    if 'isLiveBroadcast' in contents: 
        return channelName + ' is live'
    else:
        return channelName + ' is not live'