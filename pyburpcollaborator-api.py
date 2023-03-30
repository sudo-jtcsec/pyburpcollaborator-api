from burp import IBurpExtender, IBurpCollaboratorClientContext, IExtensionStateListener, ITab, IScannerCheck
from java.io import PrintWriter
from java.lang import RuntimeException
from javax.swing import JButton, JFrame, JLabel, JPanel, JTextField
from java.awt import Component, GridBagLayout, GridBagConstraints, TextField, Label, Button
from java.awt.event import ActionListener, ActionEvent
import BaseHTTPServer
import threading
import json
import traceback

server = None # The HTTP API Server running in a different thread
collab = None

class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('pong')
        elif self.path == '/generate_payload':
            global collab
            payload = collab.generatePayload(True)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(payload)
        elif self.path == '/get_interactions':
            global collab
            interactions = collab.fetchAllCollaboratorInteractions()
            inters = []
            for i in interactions:
                iss = {}
                for k in i.getProperties().keySet():
                    iss[str(k)] = str(i.getProperty(str(k)))
                inters.append(iss)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(inters))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('404 Not Found')

def run_server(callbacks):
    global server
    HandlerClass = SimpleHTTPRequestHandler
    server = BaseHTTPServer.HTTPServer( ('localhost',9876),HandlerClass)
    server.serve_forever()

class BurpExtender(IBurpExtender, IBurpCollaboratorClientContext, IExtensionStateListener):
    
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        # set our extension name
        callbacks.setExtensionName("pycollaborator-api")
        callbacks.registerExtensionStateListener(self)
        
        # obtain our output and error streams
        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)
        
        global collab
        collab = callbacks.createBurpCollaboratorClientContext()

        threading.Thread(target=run_server,args=[callbacks]).start()

    def extensionUnloaded(self):
        # Called when the extension is unloaded
        stderr = PrintWriter(self.callbacks.getStderr(), True)

        global server
        server.server_close()
