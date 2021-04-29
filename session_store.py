
import base64, os

class SessionStore:

    def __init__(self):
        self.sessions = {}

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode('utf-8')
        return rstr

    def createSession(self):
        # Generate a new session id
        sessionId = self.generateSessionId()
        # Create a new session dictionary inside the sessions dictionary
        self.sessions[sessionId] = {}
        return sessionId

    def getSessionData(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None