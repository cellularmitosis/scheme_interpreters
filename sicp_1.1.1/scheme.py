#!/usr/bin/env python

# a scheme interpreter which can handle handle section 1.1.1 and exercise 1.1.1 of SICP.

import sys

def main():
	for combination in tokenize_combinations(read_source_file(), 0):
		print evaluate(combination)

def read_source_file():
	source_fname = sys.argv[1]	
	with open(source_fname, "r") as fd:
		return fd.read()

def tokenize_combinations(text, index):
	combinations = []
	while index < len(text):
		ch = text[index]
		if ch == "(":
			(combination, new_index) = tokenize_combination(text, index)
			combinations.append(combination)
			index = new_index
			assert text[index] == ")"
		elif ch not in [" ", "\n"]:
			(literal, new_index) = tokenize_word(text, index)
			combinations.append(literal)
			index = new_index
		index += 1
		continue
	return combinations

def tokenize_combination(text, index):
	assert text[index] == "("
	index += 1
	tokens = []
	while index < len(text):
		if text[index] == ")":
			break
		elif text[index] == "(":
			(new_tokens, new_index) = tokenize_combination(text, index)
			tokens.append(new_tokens)
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

def evaluate(combination):
	evaluated_combination = []
	if type(combination) == list:
		for token in combination:
			if type(token) == list:
				evaluated_combination.append(evaluate(token))
			else:
				evaluated_combination.append(token)
	else:
		evaluated_combination = combination
	parsed_combination = parse_combination(evaluated_combination)
	if type(parsed_combination) == list:
		operator = parsed_combination[0]
		operands = parsed_combination[1:]
		return operator(operands)
	else:
		return parsed_combination

def parse_combination(combination):
	if type(combination) == list:
		operator = parse_operator(combination[0])
		operands = [parse_operand(token) for token in combination[1:]]
		return [operator] + operands
	else:
		return parse_operand(combination)

def parse_operand(token):
	if type(token) == str:
		if "." in token:
			return float(token)
		else:
			return int(token)
	else:
		return token

def parse_operator(token):
	if token == "+":
		return add
	elif token == "-":
		return subtract
	elif token == "*":
		return multiply
	elif token == "/":
		return divide
	else:
		assert False, "unknown operator: %s" % token

def add(operands):
	return reduce(lambda x, y: x + y, operands)

def subtract(operands):
	return reduce(lambda x, y: x - y, operands)

def multiply(operands):
	return reduce(lambda x, y: x * y, operands)

def divide(operands):
	return reduce(lambda x, y: x / y, operands)

if __name__ == "__main__":
	main()
