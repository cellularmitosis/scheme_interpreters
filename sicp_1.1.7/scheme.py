#!/usr/bin/env python

# a scheme interpreter which can handle SICP through section 1.1.7.

import sys
import pprint

stdlib = """
(define (not x) (if x False True))
(define (>= x y) (or (> x y) (= x y)))
(define (<= x y) (or (< x y) (= x y)))
"""

def main():
	for statement in tokenize_statements(stdlib, 0):
		evaluate_combination(statement)
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

def evaluate_combination(combination):
	if type(combination) is list:
		operator = combination[0]
		operands = combination[1:]
		if operator == "define":
			define(operands)
			return None
		elif operator == "cond":
			return cond(operands)
		elif operator == "if":
			return _if(operands)
		elif operator == "and":
			return _and(operands)
		elif operator == "or":
			return _or(operands)
		elif type(operator) is str and operator in environment and type(environment[operator]) == Procedure:
			procedure = environment[operator]
			parameter_mapping = dict(zip(procedure.parameter_names, operands))
			combination = substitute_combination(parameter_mapping, procedure)
			return evaluate_combination(combination)
		else:
			combination = [evaluate_token(token) for token in combination]
			operator = combination[0]
			operands = combination[1:]
		return operator(operands)
	else:
		return evaluate_token(combination)

def substitute_combination(parameter_mapping, procedure):
	substituted_combination = []
	for token in procedure.body:
		if type(token) is list:
			sub_procedure = Procedure(procedure.name, procedure.parameter_names, token)
			substituted_combination.append(substitute_combination(parameter_mapping, sub_procedure))
		elif token in environment:
			substituted_token = environment[token]
			if type(substituted_token) is Procedure:
				substituted_combination.append(token)
			else:
				substituted_combination.append(substituted_token)
		elif token in parameter_mapping:
			substituted_combination.append(parameter_mapping[token])
		else:
			substituted_combination.append(token)
	return substituted_combination

def evaluate_token(token):
	if type(token) is list:
		return evaluate_combination(token)
	elif token in environment:
		return evaluate_token(environment[token])
	elif type(token) is str:
		if token == "True":
			return True
		elif token == "False":
			return False
		elif token_in_charset(token, "-1234567890"):
			return int(token)
		elif token_in_charset(token, "-1234567890."):
			return float(token)
		else:
			return token
	else:
		return token

def token_in_charset(token, charset):
	for ch in token:
		if ch not in charset:
			return False
	return True

def add(operands):
	return reduce(lambda x, y: x + y, operands)

def subtract(operands):
	if len(operands) == 1:
		return -operands[0]
	else:
		return reduce(lambda x, y: x - y, operands)

def multiply(operands):
	return reduce(lambda x, y: x * y, operands)

def divide(operands):
	return reduce(lambda x, y: x / y, operands)

def equals(operands):
	return reduce(lambda x, y: x == y, operands)

def less_than(operands):
	return operands[0] < operands[1]

def greater_than(operands):
	return operands[0] > operands[1]

def define(operands):
	if type(operands[0]) is str:
		environment[operands[0]] = operands[1]
	else:
		(declaration, body) = operands
		name = declaration[0]
		parameter_names = declaration[1:]
		procedure = Procedure(name, parameter_names, body)
		environment[procedure.name] = procedure

def cond(operands):
	for branch in operands:
		(predicate, body) = branch
		if type(predicate) is str and predicate == "else":
			return evaluate_combination(body)
		elif evaluate_combination(predicate):
			return evaluate_combination(body)
	assert False, "Undefined behavior: all branches of 'cond' were false."

def _if(operands):
	(predicate, branch1, branch2) = operands
	if evaluate_combination(predicate):
		return evaluate_combination(branch1)
	else:
		return evaluate_combination(branch2)

def _and(operands):
	for predicate in operands:
		if evaluate_combination(predicate):
			continue
		else:
			return False
	return True

def _or(operands):
	for predicate in operands:
		if evaluate_combination(predicate):
			return True
	return False

environment = {
	"+": add,
	"-": subtract,
	"*": multiply,
	"/": divide,
	"=": equals,
	"<": less_than,
	">": greater_than
}

class Procedure(object):
	def __init__(self, name, parameter_names, body):
		self.name = name
		self.parameter_names = parameter_names
		self.body = body
	def __repr__(self):
		return "<Procedure: %s %s: %s>" % (self.name, self.parameter_names, self.body)

if __name__ == "__main__":
	main()
