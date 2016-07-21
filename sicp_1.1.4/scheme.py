#!/usr/bin/env python

# a scheme interpreter which can handle SICP through section 1.1.2 and exercise 1.1.2.

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
		if ch == "(":
			(combination, new_index) = tokenize_combination(text, index)
			statements.append(combination)
			index = new_index
			assert text[index] == ")"
		elif ch not in [" ", "\n"]:
			(literal, new_index) = tokenize_word(text, index)
			statements.append(literal)
			index = new_index
		index += 1
		continue
	return statements

def tokenize_combination(text, index):
	assert text[index] == "("
	index += 1
	tokens = []
	while index < len(text):
		if text[index] == ")":
			break
		elif text[index] == "(":
			(combination, new_index) = tokenize_combination(text, index)
			tokens.append(combination)
			index = new_index + 1
		elif text[index] in [" ", "\n"]:
			index += 1
			continue
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

def substitute_combination(existing_combination, procedure_definition_tuple):
	(procedure_declaration, procedure_body) = procedure_definition_tuple
	substituted_combination = []
	substituted_operator = procedure_body[0]
	substituted_combination.append(substituted_operator)
	for parameter_name in procedure_body[1:]:
		if type(parameter_name) == list:
			substituted_combination.append(substitute_combination(existing_combination, (procedure_declaration, parameter_name)))
		elif parameter_name in environment:
			if type(environment[token]) is not tuple:
				return environment[token]
			else:
				assert False
		else:
			index = None
			for i in range(1, len(procedure_declaration)):
				if procedure_declaration[i] == parameter_name:
					index = i
					substituted_combination.append(existing_combination[index])
					break
			if index is None:
				substituted_combination.append(parameter_name)				
	return substituted_combination

def evaluate_combination(combination):
	if type(combination) == list:
		if combination[0] == "define":
			define(combination[1:])
			return None
		procedure_tuple = procedure_for_name(combination[0])
		if procedure_tuple is not None:
			substituted_combination = substitute_combination(combination, procedure_tuple)
			return evaluate_combination(substituted_combination)
		else:
			evaluated_tokens = [evaluate_token(token) for token in combination]
			operator = evaluated_tokens[0]
			operands = evaluated_tokens[1:]
			return operator(operands)
	else:
		return evaluate_token(combination)

def evaluate_token(token):
	if type(token) == list:
		return evaluate_combination(token)
	elif token in environment:
		if type(environment[token]) is not tuple:
			token = environment[token]
			if type(token) == str:
				if token_in_charset(token, "1234567890"):
					return int(token)
				elif token_in_charset(token, "1234567890."):
					return float(token)
				else:
					return token
			elif type(token) == list:
				return evaluate_combination(token)
			else:
				return token
		else:
			assert False
	elif type(token) == str:
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
	if type(operands[0]) == str:
		environment[operands[0]] = operands[1]
	else:
		(procedure_declaration, procedure_body) = operands
		procedure_name = procedure_declaration[0]
		environment[procedure_name] = (procedure_declaration, procedure_body)

environment = {
	"+": add,
	"-": subtract,
	"*": multiply,
	"/": divide,
	"=": equals
}

def procedure_for_name(name):
	for (k, v) in environment.iteritems():
		if type(v) == tuple:
			procedure_name = k
			if procedure_name == name:
				return v
	return None

if __name__ == "__main__":
	main()
