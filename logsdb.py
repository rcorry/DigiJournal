import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class LogsDB:
	
	def __init__(self):
		self.connection = sqlite3.connect('logs.db')
		self.connection.row_factory = dict_factory
		self.cursor = self.connection.cursor()

	#write
	def insertLog(self, heading, rating, entry, date, place):
		data = [heading, rating, entry, date, place]
		self.cursor.execute("INSERT INTO logs (heading, rating, entry, date, place) VALUES (?, ?, ?, ?, ?)", data)
		self.connection.commit()

	def insertUser(self, fname, lname, email, password):
		data = [fname, lname, email, password]
		self.cursor.execute("INSERT INTO users (f_name, l_name, email, password) VALUES (?, ?, ?, ?)", data)
		self.connection.commit()

	def getPassword(self, email):
		data = [email]
		self.cursor.execute("SELECT password FROM users WHERE email = ?", data)
		password = self.cursor.fetchone()
		return password

	#read
	def getAllLogs(self):
		self.cursor.execute("SELECT * FROM logs")
		logs = self.cursor.fetchall()
		return logs

	def getUserLogs(self, userId):
		data = [userId]
		self.cursor.execute("SELECT * FROM logs WHERE id = ?", data)
		logs = self.cursor.fetchall()
		return logs

	def getOneLog(self, member_id):
		data = [member_id]
		self.cursor.execute("SELECT * FROM logs WHERE id = ?", data)
		log = self.cursor.fetchone()
		return log

	def getOneUser(self, email):
		data = [email]
		self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
		user = self.cursor.fetchone()
		return user



	def deleteOneLog(self, member_id):
		data = [member_id]
		self.cursor.execute("DELETE FROM logs WHERE id = ?", data)
		self.connection.commit()		

	def editOneLog(self, member_id, heading, rating, entry, date, place):
		data = [heading, rating, entry, date, place, member_id]
		logId = [member_id]
		self.cursor.execute('UPDATE logs SET heading = ?, rating = ?, entry = ?, date = ?, place = ? WHERE id = ?', data)
		self.connection.commit()
		self.cursor.execute('SELECT * FROM logs WHERE id = ?', logId)
		log = self.cursor.fetchone()
		return log


#DELETE FROM logs WHERE id = ?

#UPDATE restaurants SET name ?, rating = ?, hours = ?, city = ?, WHERE id = ?
		




