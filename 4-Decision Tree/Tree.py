'''
This class represents a decision node in the decision tree
Each decision node has a test for a single attribute. This is captured in the attribute_name variable
Each decision node then branches into d subtrees, where d is the number of unique values for the attribute
When the decision node object is being created inside create_decision_tree, then we insert the resulting subtrees (through recursion)
into a list subnodes_info.
'''
class DecisionNode(object):

	def __init__(self, attribute_name, subnodes_info):
		self.attribute_name = attribute_name
		self.subnodes_info = subnodes_info

	# Used for testing purposes, nowhere invoked
	def __str__(self):
		return "Decision on {0} with subtrees as {1}".format(self.attribute_name, self.subnodes_info)



'''
This class represents a terminal node in the decision tree
Terminal nodes are those that contain the value of the output variable that the tree is trying to predict at each stage
This output is captured as the variable classification
'''
class TerminalNode(object):

	def __init__(self, classification):
		self.classification = classification


	def __str__(self):
		return self.classification


'''
This class represents a branch in the tree between a decision node and it's subtrees
Each branch has a value associated with it and these values are those that the attribute being split on takes
'''
class Branch(object):

	def __init__(self, value):
		self.value = value


	def __str__(self):
		return self.value
