#!/usr/bin/env python

# a scheme interpreter which can handle SICP through section 1.1.2 and exercise 1.1.2.

import sys

def main():
	for combination in tokenize_combinations(read_source_file(), 0):
		result = evaluate_combination(combination)
		if result is not None:
			print result

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

def evaluate_combination(combination):
	if type(combination) == list:
		evaluated = [evaluate_token(token) for token in combination]
		operator = evaluated[0]
		operands = evaluated[1:]
		return operator(operands)
	else:
		return evaluate_token(combination)

def evaluate_token(token):
	if type(token) == list:
		return evaluate_combination(token)
	elif token in environment:
		return environment[token]
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
	(key, value) = operands
	environment[key] = value

environment = {
	"+": add,
	"-": subtract,
	"*": multiply,
	"/": divide,
	"define": define,
	"=": equals
}

if __name__ == "__main__":
	main()
