import os
import json
# a = {"username":"mmd", "password":"hunter2"}

a = os.getenv('a')
if a:
    try:
        username = json.loads(a)['username']
    except Exception as e:
        print('Error parsing JSON')

