import requests, time, json
from random import randint

temperature=0

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

for x in range(5):
    temperature = randint(0, 30)
    # value = randint(0, 30)
    print("The temperature is %s celsius" % temperature)
    time.sleep(3)

    payload = {'sensor': str("temperature"), 'value': int(temperature) }

    r = requests.post('http://localhost:3000/messages', data=json.dumps(payload), headers=headers)

    print(r.text)
