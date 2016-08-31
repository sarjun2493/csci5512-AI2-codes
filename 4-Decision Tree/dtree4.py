'''
Imports needed for this program below
Including the Tree data structure that we use to represent a decision tree by
'''
import sys
import math
import operator
import random
from Tree import *

'''
'''

'''
'Global' variables and useful definitions for the program
'''
records = []		# The training set (examples)
rules = []			# The decision tree when laid down as a set of rules (conjunctions of tests on the different literals at each level of the tree)

output = 'WillWait'	 # The target attribute we are required to predict from the training data
max_depth = 4        # Represents the maximum allowed depth of the decision tree

# This dictionary describes each categorical attribute by the different values they take
# This is useful while iterating over the different values that an attribute can take while calculating the entropy of an attribute
attribute_values_mapping = {'Alt' : ['T','F'],
							'Bar' : ['T','F'],
							'Fri' : ['T','F'],
							'Hun' : ['T','F'],
							'Pat' : ['Some', 'Full', 'None'],
							'Price' : ['$$$', '$', '$$'],
							'Rain' : ['T', 'F'],
							'Res' : ['T','F'],
							'Type' : ['French', 'Thai', 'Burger', 'Italian'],
							'Est' : ['0-10', '30-60', '10-30', '>60']}
'''
'''


'''
Method definitions begin here
'''

# This is a method which takes in the filename and prepares the training set in the desired format
# Format: Each line in the file is converted to a dictionary of <attribute,value> mapping.
# This format is convenient while checking for values of an attribute in a record, rather than having to specify indices or order of attributes in the file
def prepare_data(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()

		attributes = [attr.lstrip().rstrip() for attr in lines[0].rstrip().split(',')]

		for i in xrange(1, len(lines)):
			line = lines[i].rstrip()

			record = {}
			for key,val in zip(attributes,line.split(',')):
				record[key.lstrip().rstrip()] = val.lstrip().rstrip()
			records.append(record)

	# Return the set of attributes which happens to be the first line in the file
	return attributes
'''
'''

# This is a method which calculates the majority 'class' or output variable in the set of examples
# This method is used during a stage of decision tree construction when we cannot find examples of a particular combination of attributes
# In this case, we just give the label of the majority class, indicating a kind of default decision
# NOTE: In the event of a tie between the two classes here (we know 'WillWait' takes only the values {T,F}, we break the tie arbitrarily)

def majority_example(examples):
	if examples is not None:
		true_count,false_count = 0,0
		for record in examples:
			if record['WillWait'] == 'T':
				true_count += 1
			else:
				false_count += 1

		if (true_count > false_count):
			return 'T'
		elif (true_count < false_count):
			return 'F'
		else:
			if (random.choice((True, False))):
				return 'T'
			else:
				return 'F'

	else:
		return None

'''
'''

# This is a method which determines if the class of all the examples are the same
# This is used to prevent further branching in a given level.
# If all classes are the same, we return that class
# Else we return False
def same_classification(examples):
	start = examples[0]['WillWait']
	for i in xrange(1, len(examples)):
		if examples[i]['WillWait'] != start:
			return False
	return start
'''
'''

# This method calculates the entropy of a boolean variable
def B(q):
	temp = q * math.log(q,2)
	if (q != 1):
		temp += ((1-q) * (math.log((1-q),2)))
	return -1 * temp
'''
'''

# This method calculates the entropy of an attribute
# We invoke B() using the proportion of negative and positive examples in the examples
def entropy_attribute(a, examples):
	entropy = 0

	for v in attribute_values_mapping[a]:
		pk,nk = 0,0
		for example in examples:
			if example[a] == v :
				if example['WillWait'] == 'T':
					pk += 1
				else:
					nk += 1

		if (pk != 0):
			entropy -= (float(pk+nk)/len(examples) * B(float(pk)/(pk+nk)))

	return entropy
'''
'''

# This method determines the most important attribute from given attributes 'attrs' and the given examples
# The most important attribute can be defined as the attribute with the largest information gain
# Information gain of an attribute for a given dataset = Entropy(whole data set) - Entropy(attribute)
# Since Entropy(whole data set) is something constant for a given data set,
# we can now define most important attribute as the attribute with the smallest entropy
# This method is based on the above definition
# NOTE This does not break ties arbitrarily. We go for the earlier attribute visited for breaking ties
def most_important_attribute(attrs, examples):
	attr_entropies = []

	for attr in attrs[:-1]:
		x = entropy_attribute(attr, examples)
		attr_entropies.append((attr, x))

	best_attr = attr_entropies[0][0]
	e_value = attr_entropies[0][1]

	for i in xrange(1, len(attr_entropies)):
		if (attr_entropies[i][1] > e_value):
			e_value = attr_entropies[i][1]
			best_attr = attr_entropies[i][0]

	return best_attr
'''
'''

# This is the primary method to construct the decision tree recursively
# using the training set (examples), attributes set (attr), and parent_examples
# which is used only if no example from the training set satisfies a combination
# of attributes in the current level of the decision tree
def construct_decision_tree(examples, attr, parent_examples, level):

	# If we do not have data points, we can only guess
	# best guess is the majority elements
	if (len(examples) == 0):
		return TerminalNode(majority_example(parent_examples))

	# If the tree has reached the maximum allowed depth, then do not split further
	# Just return the best guess based on the majority
	if (level == max_depth):
	 	return TerminalNode(majority_example(examples))

	# Ideal case: when all examples have the same classification
	# Return that classification as a terminal node of the tree
	elif (same_classification(examples)):
		same = same_classification(examples)
		return TerminalNode(same)

	# No more attributes to compare with
	# return the majority case
	elif (len(attr) == 0):
		return TerminalNode(majority_example(examples))

	# The main case
	else:

		# Determine the attribute to split on
		A = most_important_attribute(attr, examples)

		# The number of subtrees would be equal to the number of values
		# that the particular attribute takes
		subnodes = []
		for v in attribute_values_mapping[A]:
			subnodes.append(None)

		# DecisionNode is one which is a test for an attribute is done
		root = DecisionNode(A, subnodes)

		# Increase the current depth of the tree
		level += 1

		# Now split examples into disjoint subsets, such that
		# each of them have the same value of the attribute being split on
		vals = attribute_values_mapping[A]

		for i in xrange(0, len(vals)):
			exs = []
			#print vals[i]
			for example in examples:
				if example[A] == vals[i]:
					exs.append(example)

			attr_copy = list(attr)
			attr_copy.remove(A)

			branch = Branch("{0} = {1}".format(A, vals[i]))

			# Determine each subtree recursively based on the test for attribute value
			subnodes[i] = (branch,construct_decision_tree(exs, attr_copy, examples, level))

		# Return the root
		return root

'''
'''

# This method creates rules based on the tree created
# This is useful when we want to predict the class of a new examples
# We check which rule it satisfies
def create_decision_rules(root, rule, rules):

	if type(root) is DecisionNode:
		for subnodes in root.subnodes_info:
			create_decision_rules(subnodes[1], rule + str(subnodes[0]) + ") ^ (", rules)

	else:
		rules.append(rule[:-3] + " ==> " + str(root))

'''
'''

# This method prints out the decision tree as a set of rules
# which are generated via the method create_decision_rules
def print_decision_tree(rules):

	for rule in rules:
		print rule

'''
'''

# The value predicted by the decision tree for a given example
# (based on the rules that the tree represents inherently)
def predicted_value(example, rules):

	success = False

	# Iterate over all the rules and see which is satisfied
	for rule in rules:
		temp = rule.split('==>')

		conditions = temp[0].rstrip().lstrip()
		result = temp[1].rstrip().lstrip()

		for condition in conditions.split('^'):
			condition = condition.rstrip().lstrip()[1:-1]

			attr,val = condition.split('=')
			attr = attr.rstrip().lstrip()
			val = val.rstrip().lstrip()

			if example[attr]==val:
				success = True
				continue

			else:
				success = False
				break

		if success:
			return result

'''
'''

# This method reports the error on the training set
# as the fraction of misclassified instances
def training_error():
	misclassified = 0
	for record in records:
		if (record[output] != predicted_value(record, rules)):
			misclassified += 1

	return float(misclassified) / len(records)

'''
'''

# This method computes the LOOCV (Leave one out cross validation)
# We create separate training instances leaving one example out
# Train a model on them, and use it to predict the value of the left out example
# Again, LOOCV is the fraction of misclassified instances
def LOOCV(attributes):

	misclassified = 0
	for i in xrange(0, len(records)):

		# Prepare the data points
		test = records[i]

		train = []
		for j in xrange(0,i):
			train.append(records[j])

		for j in xrange(i+1, len(records)):
			train.append(records[j])

		#train the model
		root_train = construct_decision_tree(train, attributes, None, 0)

		rules_train = []
		create_decision_rules(root_train, '(', rules_train)

		if (test[output] != predicted_value(test, rules_train)):
			misclassified += 1


	print 'LOOCV is : {0}\n'.format( float(misclassified) / len(records))

'''
'''

# Main function
# Input is the filename containing the data set
def dtree4(filename):
	attributes = prepare_data(filename)
	root = construct_decision_tree(records, attributes, None, 0)

	# Create rules for the decision tree
	create_decision_rules(root, '(', rules)

	# Print the decision tree
	print '\nThe decision tree for this training set is: '
	print_decision_tree(rules)

	# Print the training error
	print '\nThe training error is: {0}'.format(training_error())

	# Print the LOOCV for this data set
	LOOCV(attributes)



if __name__=='__main__':
	dtree4(sys.argv[1])
