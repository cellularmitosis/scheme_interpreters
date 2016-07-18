#!/usr/bin/env python

# Assignment 2: Write a Scheme interpreter which reads and executes the following
# subset of Scheme:
# 1) Arithmetic combinations (including nested combinations)
#
# Example source file:
# (+ 1 2)
# (* 2 (+ 1 1))

import sys

def read_source_file():
	source_fname = sys.argv[1]	
	with open(source_fname, "r") as fd:
		return fd.read()

def tokenize_word(text, index):
	word = ""
	while index < len(text):
		ch = text[index]
		if ch in [" ", "\n", ")"]:
			break
		word += ch
		index += 1
	return (word, index)

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

def tokenize_combinations(text, index):
	combinations = []
	while index < len(text):
		ch = text[index]
		if ch == "(":
			(combination, new_index) = tokenize_combination(text, index)
			combinations.append(combination)
			index = new_index
			assert text[index] == ")"
		index += 1
		continue
	return combinations

def add(operands):
	return reduce(lambda x, y: x + y, operands)

def subtract(operands):
	return reduce(lambda x, y: x - y, operands)

def multiply(operands):
	return reduce(lambda x, y: x * y, operands)

def divide(operands):
	return reduce(lambda x, y: x / y, operands)

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

def parse_operand(token):
	if type(token) == str:
		return int(token)
	else:
		return token

def parse_combination(combination):
	operator = parse_operator(combination[0])
	operands = [parse_operand(token) for token in combination[1:]]
	return [operator] + operands

def evaluate(combination):
	# print "evaluating combination:", combination
	evaluated_combination = []
	for token in combination:
		if type(token) == list:
			evaluated_combination.append(evaluate(token))
		else:
			evaluated_combination.append(token)
	parsed_combination = parse_combination(evaluated_combination)
	operator = parsed_combination[0]
	operands = parsed_combination[1:]
	return operator(operands)

def main():
	for combination in tokenize_combinations(read_source_file(), 0):
		print evaluate(combination)

if __name__ == "__main__":
	main()
