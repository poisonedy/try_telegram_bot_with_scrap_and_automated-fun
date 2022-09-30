import urllib.request
import json


def getPrice():
    with urllib.request.urlopen("http://candybot.siliconsocket.com/pricing/b84a53ebd6f33c08de2e74e90b987fcf") as url:
        data = json.loads(url.read().decode())
        return data

