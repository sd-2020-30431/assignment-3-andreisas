import dbHandler as db
from dbHandler import UserInfoHandler, AddItemHandler, AddListHandler, getHelpHandler, UserItemsHandler
from decorators import MyDecorator

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
			@MyDecorator
			def function(item):
				print(f'{item[3]:<10}: calories {item[5]} expires {item[7]}\n')
			for i in items:
				if len(i)>1:
					it = i.split()
					function(it)
