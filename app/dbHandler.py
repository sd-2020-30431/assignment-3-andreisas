import pickle
import sqlite3

conntest = sqlite3.connect('Wasteapp.db')
conntest.row_factory = sqlite3.Row

def getUserInfo(conn, username):
	text = ""
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM User WHERE name=?', (username, ))
	result = cursor.fetchone()
	text += "Id: " + str(result['id']) + "    Name: " + result['name'] + "    Password: " + result['password']

	return text

def getUserItems(conn, username):
	text = ""
	userid = getUserId(conn, username)
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item INNER JOIN GList ON GList.id = Item.glistid WHERE userid=?', (userid, ))
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text

	return text

def insertUser(conn, name, password):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO User(name, password) VALUES(?, ?)', (name, password, ))
	conn.commit()

def getGListsOfUser(conn, userid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM GList WHERE userid=?', (userid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "\n"
	return text
	
	#return cursor.fetchall()

def getUserId(conn, name):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM User WHERE name=?', (name, ))
	result = cursor.fetchone()
	if result is not None:
		return result[0]
	else:
		return None

def getUserName(conn, id):
	cursor = conn.cursor()
	cursor.execute('SELECT name FROM User WHERE id=?', (id, ))
	return cursor.fetchone()[0]

def userExists(conn, name, password):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM User WHERE name=? AND password=?', (name, password, ))
	return cursor.fetchone()

def getItemsOfUser(conn, userid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item INNER JOIN GList ON GList.id = Item.glistid WHERE userid=?', (userid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text
	
	#return cursor.fetchall()

def getUserPassword(conn, id):
	cursor = conn.cursor()
	cursor.execute('SELECT password FROM User WHERE id=?', (id, ))
	return cursor.fetchone()[0]


def insertGList(conn, userid, name):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO GList(userid, name) VALUES(?, ?)', (userid, name, ))
	conn.commit()
	return "Success"

def getItemsOfGList(conn, glistid):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM Item WHERE glistid=?', (glistid, ))
	
	text = ""
	rows = cursor.fetchall()
	for row in rows:
		text += "id: " + str(row['id']) + "    name: " + row['name'] + "    cals: " + str(row['cals']) + "    exp_date: " + str(row['exp_date']) + "\n"
	return text
	
	#return cursor.fetchall()

def getGListId(conn, username, listname):
	cursor = conn.cursor()
	userid = getUserId(conn, username)
	cursor.execute('SELECT id FROM GList WHERE name=? AND userid=?', (listname, userid, ))
	result = cursor.fetchone()
	if result is not None:
		return result[0]
	else:
		return None

def insertItem(conn, glistid, name, cals, exp_date):
	cursor = conn.cursor()
	cursor.execute('INSERT INTO Item(glistid, name, cals, exp_date) VALUES(?, ?, ?, ?)', (glistid, name, int(cals), str(exp_date)))
	conn.commit()
	return "Success"

def getItemId(conn, name):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM Item WHERE name=?', (name, ))
	return cursor.fetchone()[0]







