#!/usr/bin/env python

# a scheme interpreter which can handle SICP through section 1.1.4.

import sys
import pprint

def main():
	for statement in tokenize_statements(read_source_file(), 0):
		result = evaluate_combination(statement)
		if result is not None:
			print result

def read_source_file():
	source_fname = sys.argv[1]	
	with open(source_fname, "r") as fd:
		return fd.read()

def tokenize_statements(text, index):
	statements = []
	while index < len(text):
		ch = text[index]
		if ch in [" ", "\n"]:
			pass
		elif ch == "(":
			(combination, new_index) = tokenize_combination(text, index)
			statements.append(combination)
			index = new_index
			assert text[index] == ")"
		else:
			(literal, new_index) = tokenize_word(text, index)
			statements.append(literal)
			index = new_index
		index += 1
	return statements

def tokenize_combination(text, index):
	assert text[index] == "("
	index += 1
	tokens = []
	while index < len(text):
		ch = text[index]
		if ch == ")":
			break
		elif ch in [" ", "\n"]:
			index += 1
		elif ch == "(":
			(combination, new_index) = tokenize_combination(text, index)
			tokens.append(combination)
			index = new_index + 1
		else:
			(word, new_index) = tokenize_word(text, index)
			if len(word) > 0:
				tokens.append(word)
			index = new_index
	assert len(tokens) > 0
	return (tokens, index)

def tokenize_word(text, index):
	word = ""
	while index < len(text):
		ch = text[index]
		if ch in [" ", "\n", ")"]:
			break
		word += ch
		index += 1
	return (word, index)

def substitute_combination(existing_combination, procedure):
	substituted_combination = []
	substituted_operator = procedure.body[0]
	substituted_combination.append(substituted_operator)
	for token in procedure.body[1:]:
		if type(token) is list:
			sub_procedure = Procedure(procedure.name, procedure.parameter_names, token)
			substituted_combination.append(substitute_combination(existing_combination, sub_procedure))
		elif token in environment:
			substituted_combination = environment[token]
			if type(substituted_combination) is not Procedure:
				return substituted_combination
			else:
				assert False
		else:
			index = None
			for i in range(0, len(procedure.parameter_names)):
				if procedure.parameter_names[i] == token:
					index = i
					substituted_combination.append(existing_combination[index+1])
					break
			if index is None:
				substituted_combination.append(token)				
	return substituted_combination

def evaluate_combination(combination):
	if type(combination) is list:
		operator_name = combination[0]
		if operator_name == "define":
			define(combination[1:])
			return None
		elif operator_name in environment and type(environment[operator_name]) == Procedure:
			procedure = environment[operator_name]
			combination = substitute_combination(combination, procedure)
			return evaluate_combination(combination)
		else:
			combination = [evaluate_token(token) for token in combination]
		operator = combination[0]
		operands = combination[1:]
		return operator(operands)
	else:
		return evaluate_token(combination)

def evaluate_token(token):
	if type(token) is list:
		return evaluate_combination(token)
	elif token in environment:
		if type(environment[token]) is not Procedure:
			token = environment[token]
			if type(token) is str:
				if token_in_charset(token, "1234567890"):
					return int(token)
				elif token_in_charset(token, "1234567890."):
					return float(token)
				else:
					return token
			elif type(token) is list:
				return evaluate_combination(token)
			else:
				return token
		else:
			assert False
	elif type(token) is str:
		if token_in_charset(token, "1234567890"):
			return int(token)
		elif token_in_charset(token, "1234567890."):
			return float(token)
		else:
			return token
	else:
		assert False, "Could not evaluate token: %s" % token

def token_in_charset(token, charset):
	for ch in token:
		if ch not in charset:
			return False
	return True

def add(operands):
	return reduce(lambda x, y: x + y, operands)

def subtract(operands):
	return reduce(lambda x, y: x - y, operands)

def multiply(operands):
	return reduce(lambda x, y: x * y, operands)

def divide(operands):
	return reduce(lambda x, y: x / y, operands)

def equals(operands):
	return reduce(lambda x, y: x == y, operands)

def define(operands):
	if type(operands[0]) is str:
		environment[operands[0]] = operands[1]
	else:
		(declaration, body) = operands
		name = declaration[0]
		parameter_names = declaration[1:]	
		procedure = Procedure(name, parameter_names, body)
		environment[procedure.name] = procedure

environment = {
	"+": add,
	"-": subtract,
	"*": multiply,
	"/": divide,
	"=": equals
}

class Procedure(object):
	def __init__(self, name, parameter_names, body):
		self.name = name
		self.parameter_names = parameter_names
		self.body = body

if __name__ == "__main__":
	main()
