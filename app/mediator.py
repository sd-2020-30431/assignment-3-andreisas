import dbHandler as db
from dbHandler import UserInfoHandler, AddItemHandler, AddListHandler, getHelpHandler, UserItemsHandler
from decorators import report

class Mediator:
	handlerMap = {
		'help' : getHelpHandler,
		'get info' : UserInfoHandler,
		'add list' : AddListHandler,
		'add item' : AddItemHandler,
		'get items' : UserItemsHandler
	}

	def handle(self, request):
		if len(request.split()) > 2:
			action = request.split()[1] + " " + request.split()[2]
		elif len(request.split()) == 2:
			action = request.split()[1]
		#Verify if the action is in handlerMap
		print(action)
		if action in self.handlerMap:
			handlerType = self.handlerMap[action]
			handler = handlerType()

			return action, handler.handle(request)
		else:
			return None, None
	
	def handleData(self, data):
		if "help" in data:
			print("Commands:\nget info\nget items\nadd list [list_name]\nadd item [item_name] [item_calories] [item_date] in [list_name]\n")
		elif "add list" in data or "get info" in data or "add item" in data:
			print(data[9:])
		elif "get items" in data:
			items = data[10:].split("\n")
			@report
			def print_item(item):
				print(f'{item[3]:<10}: calories {item[5]} expires {item[7]}\n')
			for i in items:
				if len(i)>1:
					it = i.split()
					print_item(it)



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
