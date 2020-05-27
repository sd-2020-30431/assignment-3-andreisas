import dbHandler as db

def processCMD(conn, username, text):
	if text == "help":
		return "Commands:\nget info\nget items\nadd list [list_name]\nadd item [item_name] [item_calories] [item_date] in [list_name]\n"
	if "add" in text:
		if "list" in text:
			return db.insertGList(conn, db.getUserId(conn, username), text.split()[2])
		if "item" in text:
			return db.insertItem(conn, db.getGListId(conn, username, text.split()[6]), text.split()[2], text.split()[3], text.split()[4])
		else:
			pass
	elif "get" in text:
		if "info" in text:
			return db.getUserInfo(conn, username)
		elif "items" in text:
			return db.getUserItems(conn, username)
		else:
			pass
	else:
		pass
