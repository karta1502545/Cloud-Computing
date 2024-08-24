# testing script

import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-lexv2-autograder"

payload = {
	"graphApi": "https://yw9ik5b3g5.execute-api.us-east-1.amazonaws.com/sts",
	"botId": "OEYXTLCJZN", 
	"botAliasId": "TSTALIASID",
	"identityPoolId": "us-east-1:c1f47b85-e0a2-4284-8f1b-a5eede2f0592",
	"accountId": "533267045615",
	"submitterEmail": "chunyil3@illinois.edu",
	"secret": "Vyh7FUdRAIm2Bg6R",
	"region": "us-east-1"
    }

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)