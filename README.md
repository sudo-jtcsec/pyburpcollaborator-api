# pyburpcollaborator-api
Burp Extension that creates basic API for use with the pyburpcollaborator module

Leverages Burp Collaborator settings so you can use private server

## Basic Example
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
