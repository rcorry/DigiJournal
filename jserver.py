from session_store import SessionStore
from passlib.hash import bcrypt
from logsdb import LogsDB
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
#parse_qs turns incoming data into a dictionary with arrays as its values
from urllib.parse import parse_qs
import json

SESSION_STORE = SessionStore()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def readCookie(self):
        if 'Cookie' in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers['Cookie'])
        else:
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header('Set-Cookie', morsel.OutputString())
    
    def loadSessionData(self):
        self.readCookie()
        #TODO: implement the algorithm
        if 'sessionId' in self.cookie:
            sessionId = self.cookie['sessionId'].value
            sessionData = SESSION_STORE.getSessionData(sessionId)

            if sessionData == None:
                #creates a new session with a new cookie value
                sessionId = SESSION_STORE.createSession()
                sessionData = SESSION_STORE.getSessionData(sessionId)
                self.cookie['sessionId'] = sessionId
                
        else:
            sessionId = SESSION_STORE.createSession()
            sessionData = SESSION_STORE.getSessionData(sessionId)
            self.cookie['sessionId'] = sessionId
        
        self.sessionData = sessionData

    def handleNotFound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def handle401(self):
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes("Not Logged In", "utf-8"))

    def handleGetLogs(self):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        db = LogsDB()
        logs = db.getAllLogs()
        self.wfile.write(bytes(json.dumps(logs), "utf-8"))

    def handleGetOneLog(self, member_id):
        if "userId" not in self.sessionData:
            handle401()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        db = LogsDB()
        log = db.getOneLog(member_id)
        self.wfile.write(bytes(json.dumps(log), "utf-8"))
 
    
    def handleCreateLog(self):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")

        parsed_body = parse_qs(body)

        heading = parsed_body["heading"][0]
        rating = parsed_body["rating"][0]
        entry = parsed_body["entry"][0]
        date = parsed_body["date"][0]
        place = parsed_body["place"][0]

        db = LogsDB()
        db.insertLog(heading, rating, entry, date, place)

        self.send_response(201)
        self.end_headers()

    def handleLogin(self):
        #if "userId" not in self.sessionData:
        #    self.handle401()
        #    return
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)

        email = parsed_body["email"][0]
        password = parsed_body["password"][0]
        db = LogsDB()
        user = db.getOneUser(email)

        if user == None:
            self.send_response(401)
            self.end_headers()
 
        else:
            if bcrypt.verify(password, user['password']):

                self.sessionData['userId'] = user['id']
                self.send_response(201)
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
    
    def handleCreateUser(self):
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")

        parsed_body = parse_qs(body)

        fname = parsed_body["f_name"][0]
        lname = parsed_body["l_name"][0]
        email = parsed_body["email"][0]
        p = parsed_body["password"][0]
        password = bcrypt.hash(p)

        db = LogsDB()
        user = db.getOneUser(email)
        if user == None:
            db.insertUser(fname, lname, email, password)
            self.send_response(201)

        else:
            self.send_response(422)

        self.end_headers()



    def handleDeleteOneLog(self, member_id):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        db = LogsDB()
        log = db.getOneLog(member_id)
        if log != None:
            db.deleteOneLog(member_id)
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()
 
    def handleEditOneLog(self, member_id):
        if "userId" not in self.sessionData:
            self.handle401()
            return
        db = LogsDB()
        log = db.getOneLog(member_id)
        if log != None:
            length = self.headers['Content-Length']
            body = self.rfile.read(int(length)).decode("utf-8")
            parsed_body = parse_qs(body)

            heading = parsed_body["heading"][0]
            rating = parsed_body["rating"][0]
            entry = parsed_body["entry"][0]
            date = parsed_body["date"][0]
            place = parsed_body["place"][0]
            db.editOneLog(member_id, heading, rating, entry, date, place)

            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()
 
    def do_OPTIONS(self):
        self.loadSessionData()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.loadSessionData()
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "logs":
            if member_id:
                self.handleGetOneLog(member_id)
            else:
                self.handleGetLogs()
        else:
            self.handleNotFound()
    
    def do_POST(self):
        self.loadSessionData()
        if self.path == "/logs":
            self.handleCreateLog()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleLogin()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSessionData()
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "logs" and member_id:
            self.handleDeleteOneLog(member_id)
        else:
            self.handleNotFound()
    
    def do_PUT(self):
        self.loadSessionData()
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None

        if collection == "logs" and member_id:
            self.handleEditOneLog(member_id)
        else:
            self.handleNotFound()
 

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyHTTPRequestHandler)

    print("Server is listening")
    server.serve_forever()

run()
