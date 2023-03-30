# pyburpcollaborator-api
Burp Extension that creates basic API for use with the pyburpcollaborator module

Leverages Burp Collaborator settings so you can use private server

## Basic Example
```
import pycollaborator, time, requests

collab = pycollaborator.Collaborator("localhost","9876")
print(collab.status())
payload = collab.payload()
resp = requests.get("http://"+payload)
time.sleep(2)
print(collab.poll())
```
