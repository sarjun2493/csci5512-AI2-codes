'''
Imports begin here
Includes the data structure for a decision list
'''
import sys
import operator
import random
from DecisionList import *
'''
End of imports
'''

'''
General purpose variables
Output represents the target variable that needs to be predicted
The mapping tells us which categorical attribute takes which values
'''
records = []
output = 'WillWait'
output_values = {}
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
Method definitions start here
'''

# Method that takes filename and converts the data in a specific format
# We represent each training example as a dictionary of <attribute,value> mapping
# This becomes easier while comparing values and doing literal test at each stage
# of the decision list
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

	return attributes

'''
'''

# Method to check if all the examples have the same value for target variable
def check_purity(eg):

	temp = eg[0][output]
	for i in xrange(1, len(eg)):
		if (eg[i][output] != temp):
			return None, False

	return temp, True

'''
'''

# Method that creates the decision list from the given attributes and examples
def create_decision_list(attrs, examples):

	# If no example to learn from, return default decision which is 'F'
	if len(examples) == 0:
		return TerminalNode('F')

	# Boolean variable that tells if there exists a test t which matches a nonempty subset
	# of the examples
	found = False

	# Represents the examples which satisfy a test t and will be removed
	to_remove = []
	# Represents the literal and value combination used at each decision node
	attr_val = []


	# Strategy is to make sure that the test chosen finally is the one that removes the maximum
	# number of examples at once. If there is a tie, then we prefer one literal tests to
	# two literal tests

	# Try for one literal test
	for attr in attrs[:-1]:
		for val in attribute_values_mapping[attr]:

			eg = []
			for ex in examples:
				if ex[attr] == val:
					eg.append(ex)

			if (len(eg) > 0):
				temp, result = check_purity(eg)

				if (result):
					if len(eg) > len(to_remove):
						to_remove = eg
						del attr_val[:]
						attr_val.append((attr, val))

					found = True


	# Now do for 2 literals
	for i in xrange(0, len(attrs) - 2):
		attr1 = attrs[i]
		vals1 = attribute_values_mapping[attr1]

		for j in xrange(i+1, len(attrs) - 1):
			attr2 = attrs[j]
			vals2 = attribute_values_mapping[attr2]

			for j in xrange(0, len(vals1)):
				for k in xrange(0, len(vals2)):

					eg = []
					for ex in examples:
						if ex[attr1] == vals1[j] and ex[attr2] == vals2[k]:
							eg.append(ex)

					if (len(eg) > 0):
						temp, result = check_purity(eg)

						if (result):
							if len(eg) > len(to_remove):
								to_remove = eg
								del attr_val[:]
								attr_val.append((attr1, vals1[j]))
								attr_val.append((attr2, vals2[k]))

							found = True


	# If no test matches, then we return None, to indicate failure
	if not found:
		return None

	# If test is found, build the list structure recursively
	else:

		# The string that represents the test at each decision node
		formatted_string = '('

		# If attr_val has more than one tuple, then the test involves multiple literals
		# else just the single literal
		if len(attr_val) > 1:
			formatted_string += str(attr_val[0][0]) + " = " + str(attr_val[0][1]) + ") ^ (" + str(attr_val[1][0]) + " = " + str(attr_val[1][1])

		else:
			formatted_string += str(attr_val[0][0]) + " = " + str(attr_val[0][1])

		formatted_string += ')'

		# Each node has a value corresponding to success of the test
		# else it points to the next decision to be tested
		sublist = []
		sublist.append(TerminalNode(to_remove[0][output]))
		sublist.append(None)

		list_head = DecisionNode(formatted_string, sublist)

		# Remove the subset of examples matching the test t
		copy = list(examples)
		for example in to_remove:
			copy.remove(example)

		# Recursive call
		sublist[1] = (create_decision_list(attrs, copy))

		# Return the decision node at this step
		return list_head

'''
'''

# Semantics and printing out decision list in a rule based format
def create_decision_rules(head, rules):

	rules.append(head.test_condition + ' ==> ' + str(head.sublist[0]))
	if type(head.sublist[1]) is DecisionNode:
		create_decision_rules(head.sublist[1], rules)
	else:
		rules.append('() ==> ' + str(head.sublist[1]))

'''
'''

# Method to print out the decision list in rule format
def print_decision_list(rules):
	print '\nThe decision list is: '
	counter = 1
	for rule in rules:
		print str(counter) + ' : ' + rule
		counter += 1

'''
'''

# Method to predict the output variable of an example based on the rules
def predict_example(example, rules):

	success = False

	# Check which rules it matches
	for rule in rules[:-1]:
		temp = rule.split('==>')

		conditions = temp[0].rstrip().lstrip()
		result = temp[1].rstrip().lstrip()

		for condition in conditions.split('^'):
			condition = condition.split('(')[1]
			condition = condition.split(')')[0]

			attr,val = condition.split(' = ')

			if (example[attr] == val):
				success = True
				continue

			else:
				success = False
				break

		if success:
			return result

    # Final rule is default decision = 'F'
	if not success:
		return 'F'

'''
'''

# Method that determines the training error on the examples based on the rules
# that the decision list represent. This is computed as the fraction of the
# misclassified instances
def training_error(examples, rules):
	misclassified = 0
	for example in examples:
		if example[output] != predict_example(example, rules):
			misclassified += 1

	return float(misclassified) / len(examples)

'''
'''

# Method that determines the Leave one out cross validation (LOOCV) error
# Build training sets leaving out one example each time and use the latter
# as the test example to determine misclassification. Again, erorr reported
# as the fraction of misclassified instances
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

		# Train the model
		train_head_list = create_decision_list(attributes, train)

		rules_train = []
		create_decision_rules(train_head_list, rules_train)

		if (test[output] != predict_example(test, rules_train)):
			misclassified += 1


	return ( float(misclassified) / len(records))

'''
'''

# Main function which builds a decision list based on the training examples
# Training examples is part of filename provided as input
def dlist2(filename):
	attributes = prepare_data(filename)
	head = create_decision_list(attributes, records)

	rules = []
	create_decision_rules(head, rules)
	print_decision_list(rules)

	print '\nTraining error : {0}'.format(training_error(records, rules))

	print 'LOOCV : {0}\n'.format(LOOCV(attributes))


if __name__=='__main__':
	dlist2(sys.argv[1])
