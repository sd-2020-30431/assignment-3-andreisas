import pickle
import sqlite3

conn = sqlite3.connect('Wasteapp.db')
conn.row_factory = sqlite3.Row


class UserInfoHandler:
	def handle(self, request):
		return self.getUserInfo(request.split()[0])

	def getUserInfo(self, username):
		text = ""
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM User WHERE name=?', (username, ))
		result = cursor.fetchone()
		text += "Id: " + str(result['id']) + "    Name: " + result['name'] + "    Password: " + result['password']

		return text

class AddItemHandler:
	def handle(self, request):
		return self.addItem(self.getGListId(request.split()[0], request.split()[7]), request.split()[3], request.split()[4], request.split()[5])

	def addItem(self, glistid, name, cals, exp_date):
		if glistid is not None:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO Item(glistid, name, cals, exp_date) VALUES(?, ?, ?, ?)', (glistid, name, int(cals), str(exp_date)))
			conn.commit()
			return "Success"
		return "Fail"

	def getGListId(self, username, listname):
		cursor = conn.cursor()
		userid = getUserId(username)
		cursor.execute('SELECT id FROM GList WHERE name=? AND userid=?', (listname, userid, ))
		result = cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return None

class AddListHandler:
	def handle(self, request):
		return self.addGList(self.getUserId(request.split()[0]), request.split()[3])

	def addGList(self, userid, name):
		if userid is not None:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO GList(userid, name) VALUES(?, ?)', (userid, name, ))
			conn.commit()
			return "Success"
		return "Fail"

	def getUserId(self, name):
		cursor = conn.cursor()
		cursor.execute('SELECT id FROM User WHERE name=?', (name, ))
		result = cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return None

class getHelpHandler:
	def handle(self, request):
		return "help"

class UserItemsHandler:
	def handle(self, request):
		return self.getUserItems(request.split()[0])

	def getUserItems(self, username):
		text = ""
		userid = getUserId(username)
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM Item INNER JOIN GList ON GList.id = Item.glistid WHERE userid=?', (userid, ))
		rows = cursor.fetchall()
		for row in rows:
			text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
		return text

	def getUserId(self, name):
		cursor = conn.cursor()
		cursor.execute('SELECT id FROM User WHERE name=?', (name, ))
		result = cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return None


#The following functions were made before the mediator and were used for making it
def getUserInfo(username):
	text = ""
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM User WHERE name=?', (username, ))
	result = cursor.fetchone()
	text += "Id: " + str(result['id']) + "    Name: " + result['name'] + "    Password: " + result['password']

	return text

def getUserItems(username):
	text = ""
	userid = getUserId(conn, username)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item INNER JOIN GList ON GList.id = Item.glistid WHERE userid=?', (userid, ))
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text

def insertItem(glistid, name, cals, exp_date):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO Item(glistid, name, cals, exp_date) VALUES(?, ?, ?, ?)', (glistid, name, int(cals), str(exp_date)))
	conn.commit()
	return "Success"

def insertGList(userid, name):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO GList(userid, name) VALUES(?, ?)', (userid, name, ))
	conn.commit()
	return "Success"

def insertUser(name, password):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO User(name, password) VALUES(?, ?)', (name, password, ))
	conn.commit()

def getGListsOfUser(userid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM GList WHERE userid=?', (userid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "\n"
	return text
	
	#return cursor.fetchall()

def getUserId(name):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM User WHERE name=?', (name, ))
	result = cursor.fetchone()
	if result is not None:
		return result[0]
	else:
		return None

def getUserName(id):
	cursor = conn.cursor()
	cursor.execute('SELECT name FROM User WHERE id=?', (id, ))
	return cursor.fetchone()[0]

def userExists(name, password):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM User WHERE name=? AND password=?', (name, password, ))
	return cursor.fetchone()

def getItemsOfUser(userid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item INNER JOIN GList ON GList.id = Item.glistid WHERE userid=?', (userid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text
	
	#return cursor.fetchall()

def getUserPassword(id):
	cursor = conn.cursor()
	cursor.execute('SELECT password FROM User WHERE id=?', (id, ))
	return cursor.fetchone()[0]

def getItemsOfGList(glistid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item WHERE glistid=?', (glistid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text
	
	#return cursor.fetchall()

def getGListId(username, listname):
	cursor = conn.cursor()
	userid = getUserId(conn, username)
	cursor.execute('SELECT id FROM GList WHERE name=? AND userid=?', (listname, userid, ))
	result = cursor.fetchone()
	if result is not None:
		return result[0]
	else:
		return None


def getItemId(name):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM Item WHERE name=?', (name, ))
	return cursor.fetchone()[0]







