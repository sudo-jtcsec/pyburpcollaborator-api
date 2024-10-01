# pyburpcollaborator-api
Burp Extension that creates basic API for use with the pyburpcollaborator module

Install the extension pyburpcollaborator-api.py in Burp, which then hosts a mini API on localhost. The pyburpcollaborator python module will then use this API to create new payloads and poll for interactions, allowing for access from custom scripts outside of Burp

Leverages Burp Collaborator settings so you can use a private server configured in your project settings.

## Basic Script Example
```
import pyburpcollaborator, time, requests

collab = pyburpcollaborator.Collaborator("localhost","9876")
print(collab.status())
payload = collab.payload()

print(payload)
while True:
    # pol the URL. If theres data, print it
    ints = collab.poll()
    if len(ints) != 0:
        print(ints)

    time.sleep(1)
```
