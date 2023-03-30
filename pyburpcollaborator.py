import requests

class Collaborator:
    def __init__(self, ip, port):
        self.ip = str(ip)
        self.port = str(port)

    def status(self):
        resp = requests.get("http://"+self.ip+":"+self.port+"/ping")
        if resp.status_code != 200:
            return False
        if resp.status_code == 200 and resp.text.strip() == "pong":
            return True

    def payload(self):
        resp = requests.get("http://"+self.ip+":"+self.port+"/generate_payload")
        return resp.text.strip()

    def poll(self):
        resp = requests.get("http://"+self.ip+":"+self.port+"/get_interactions")
        return resp.json()

