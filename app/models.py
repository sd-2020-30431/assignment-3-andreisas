class User:

	def __init__(self ,id ,name, password):
		self.id = id
		self.name = name
		self.password = password

	def __repr__(self):
		return "User(name:'{}', password:'{}')".format(self.name, self.password)


class GList:

	def __init__(self, id, userid, name):
		self.id = id
		self.userid = userid
		self.name = name

	def __repr__(self):
		return "List(userid:'{}', name:'{}')".format(self.userid, self.name)

class Item:

	def __init__(self, id, glistid, name, cals, exp_date):
		self.id = id
		self.glistid = glistid
		self.name = name
		self.cals = cals
		self.exp_date = exp_date

	def __repr__(self):
		return "Item(glistid:'{}', name:'{}', cals:'{}', exp_date:'{}')".format(self.glistid, self.name, str(self.cals), str(self.exp_date))

