from typing import Iterable, Generator

NUMBER = "NUMBER"
ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
operators = ("+", "-", "*", "/", "(", ")")
operator_type_map = {
	"+": ADD,
	"-": SUB,
	"*": MUL,
	"/": DIV
}
operators_level = {
	ADD: 1,
	SUB: 1,
	MUL: 2,
	DIV: 2
}

def tokenizer(input: str)-> Generator[str, None, None]:
	buffer: str = ""
	ch: str = ""
	length: int = len(input)
	position: int = 0
	while (ch := input[position] if position < length else ""):
		if ch.isspace():
			if not buffer:
				position += 1
				continue
			yield buffer
			buffer = ""
		elif ch in operators:
			if buffer:
				yield buffer
				buffer = ""
			yield ch
			position += 1
			continue
		elif ch.isdigit() or (ch == "." and "." not in buffer):
			buffer += ch
			position += 1
		else:
			raise SyntaxError(f"unknown character {ch}")

	if buffer:
		yield buffer

def combine(stack)-> None:
	while len(stack) > 1:
		node = stack.pop()
		stack[-1].append(node)

def scanner(tokenizer: Iterable)-> list:
	root = ["root"]
	stack: list = []
	operand: float | None = None
	token = ""
	for token in tokenizer:
		try:
			float(token)
			if operand != None:
				raise SyntaxError("2 consecutive operand.")
			else:
				operand = float(token)
			continue
		except ValueError:
			pass

		if token == "(":
			if stack:
				stack[-1].append(scanner(tokenizer))
			else:
				stack.append(scanner(tokenizer))
			continue
		elif token == ")":
			break

		if len(stack) == 0:
			stack.append([operator_type_map[token], operand])
			operand = None
			continue

		if (operators_level[stack[-1][0]] >
		operators_level[operator_type_map[token]]):
			stack[-1].append(operand)
			operand = None

			combine(stack)

			stack.append(
				[operator_type_map[token],
					stack.pop()
				])
			continue
		elif (operators_level[stack[-1][0]] ==
		operators_level[operator_type_map[token]]):
			stack[-1].append(operand)
			operand = None
			stack.append(
				[operator_type_map[token],
					stack.pop()
				])
			continue
		else:
			stack.append([operator_type_map[token], operand])
			operand = None
	if operand != None:
		if stack:
			stack[-1].append(operand)
		else:
			combine(stack)
			stack.append(operand)

	root.append(stack.pop())
	return root

def evaluate(tree: list | float)-> float:
	if isinstance(tree, float) or isinstance(tree, int):
		return tree
	op = tree[0]
	if op == "root":
		return evaluate(tree[1])
	left = evaluate(tree[1])
	right = evaluate(tree[2])
	if op == ADD:
		return left + right
	elif op == SUB:
		return left - right
	elif op == MUL:
		return left * right
	elif op == DIV:
		return left / right
	else:
		raise Exception("我必须写这么一句话, 不然我的 lsp 一直类型错误")

def print_tree(node: list, depth: int = 0)-> None:
	for i in node:
		if isinstance(i, list):
			print_tree(i, depth + 1)
		else:
			print(f"{"\t" * depth}{i}")

def main()-> None:
	node = scanner(tokenizer("(42)"))
	print_tree(node)
	print("***")
	print(evaluate(node))

if __name__ == '__main__':
	main()
