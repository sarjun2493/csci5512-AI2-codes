class DecisionNode(object):

	def __init__(self, test_condition, sublist):
		self.test_condition = test_condition
		self.sublist = sublist


	# def __str__(self):
	# 	return "Test on {0} with sublist as {1}".format(self.test_condition, self.sublist_info)



class TerminalNode(object):

	def __init__(self, classification):
		self.classification = classification


	def __str__(self):
		#return "Terminal node {0}".format(self.classification)
		return self.classification


class Branch(object):

	def __init__(self, value):
		self.value = value


	def __str__(self):
		#return "Value :  {0}".format(self.value)
		return self.value