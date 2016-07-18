#!/usr/bin/env python

# Assignment 1: Write a Scheme interpreter which reads and executes the following
# subset of Scheme:
# 1) Non-nested arithmetic combinations.
#
# Example source file:
# (+ 1 2)
# (* 2 3)

import sys

def read_source_file():
	source_fname = sys.argv[1]	
	with open(source_fname, "r") as fd:
		return fd.read()

def minify_source_text(source_text):
	return source_text.replace("\n", " ")

def read_statement(iterator):
	statement = ""
	for ch in iterator:
		if ch == ")":
			return statement
		else:
			statement += ch

def parse_statement(statement):
	parameters = statement.split()
	operator = parameters[0]
	if operator == "+":
		operator = add
	elif operator == "-":
		operator = subtract
	elif operator == "*":
		operator = multiply
	elif operator == "/":
		operator = divide
	operands = [int(operand) for operand in parameters[1:]]
	return [operator] + operands

def parse_statements(iterator):
	statements = []
	for ch in iterator:
		if ch == "(":
			statements.append(parse_statement(read_statement(iterator)))
	return statements

def add(operands):
	return reduce(lambda x, y: x + y, operands)

def subtract(operands):
	return reduce(lambda x, y: x - y, operands)

def multiply(operands):
	return reduce(lambda x, y: x * y, operands)

def divide(operands):
	return reduce(lambda x, y: x / y, operands)

def execute(statement):
	operator = statement[0]
	operands = statement[1:]
	return operator(operands)

if __name__ == "__main__":
	statements = parse_statements(iter(minify_source_text(read_source_file())))
	for statement in statements:
		result = execute(statement)
		print result
