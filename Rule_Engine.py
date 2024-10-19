import re


class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operand" or "operator"
        self.left = left  # left child Node
        self.right = right  # right child Node
        self.value = value  # a dictionary for "operand" or "AND"/"OR" for "operator"


def tokenize(rule):
    # Tokenizes by splitting around spaces, operators, and parentheses
    return re.findall(r"[\w']+|[()<>=>=]", rule)


def build_ast(tokens):
    stack = []  # Stack to hold the operands
    operators = []  # Stack to hold operators and parentheses
    precedence = {"AND": 1, "OR": 0}  # Define operator precedence

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Check if token is an operand (assumes attribute > value, attribute = value, etc.)
        if re.match(r"\w+", token) and i + 2 < len(tokens) and tokens[i + 1] in [">", "<", "="]:
            attr, operator, val = token, tokens[i + 1], tokens[i + 2]
            operand_value = {"attribute": attr, "operator": operator, "value": val}
            stack.append(Node("operand", value=operand_value))
            i += 3  # Skip the next two tokens (operator and value) since they’re processed here

        elif token in ["AND", "OR"]:  # Handle operators
            while operators and precedence.get(operators[-1], -1) >= precedence[token]:
                if len(stack) < 2:
                    raise ValueError("Malformed expression")  # Ensure two nodes are available
                right = stack.pop()
                left = stack.pop()
                op = operators.pop()
                stack.append(Node("operator", left=left, right=right, value=op))
            operators.append(token)
            i += 1

        elif token == "(":  # Left Parenthesis
            operators.append(token)
            i += 1

        elif token == ")":  # Right Parenthesis
            while operators and operators[-1] != "(":
                if len(stack) < 2:
                    raise ValueError("Malformed expression")  # Ensure two nodes are available
                right = stack.pop()
                left = stack.pop()
                op = operators.pop()
                stack.append(Node("operator", left=left, right=right, value=op))
            operators.pop()
            i += 1

    # Final combination for remaining operators
    while operators:
        if len(stack) < 2:
            raise ValueError("Malformed expression")  # Ensure two nodes are available
        right = stack.pop()
        left = stack.pop()
        op = operators.pop()
        stack.append(Node("operator", left=left, right=right, value=op))

    if len(stack) != 1:
        raise ValueError("Malformed expression")  # Ensure there’s only one root node
    return stack[0]  # Return the root of the AST


def create_rule(rule_string):
    tokens = tokenize(rule_string)
    return build_ast(tokens)


# Function to combine multiple rule ASTs using OR
def combine_rules(rules):
    ast_list = [create_rule(rule) for rule in rules]
    while len(ast_list) > 1:
        left = ast_list.pop(0)
        right = ast_list.pop(0)
        combined = Node("operator", left=left, right=right, value="OR")
        ast_list.insert(0, combined)
    return ast_list[0]


def evaluate_rule(ast_node, data):
    if ast_node.type == "operand":
        attr, operator, value = ast_node.value["attribute"], ast_node.value["operator"], ast_node.value["value"]
        if operator == ">":
            return data[attr] > int(value)
        elif operator == "<":
            return data[attr] < int(value)
        elif operator == "=":
            return data[attr] == value
        elif operator == ">=":
            return data[attr] >= int(value)
        elif operator == "<=":
            return data[attr] <= int(value)
    elif ast_node.type == "operator":
        left_eval = evaluate_rule(ast_node.left, data)
        right_eval = evaluate_rule(ast_node.right, data)
        if ast_node.value == "AND":
            return left_eval and right_eval
        elif ast_node.value == "OR":
            return left_eval or right_eval


def print_ast(node, level=0):
    if node is None:
        return
    indent = "  " * level
    if node.type == "operator":
        print(f"{indent}Operator: {node.value}")
    elif node.type == "operand":
        print(f"{indent}Operand: {node.value}")

    if node.left:
        print_ast(node.left, level + 1)
    if node.right:
        print_ast(node.right, level + 1)


if __name__ == "__main__":
    # Create individual rule
    rule1 = "age > 30 AND department = Sales"
    rule2 = "salary > 50000 OR experience > 5"

    # Build AST for individual rule
    ast1 = create_rule(rule1)
    ast2 = create_rule(rule2)
    print("AST Built Successfully!")
    print("AST Structure for Rule 1:")
    print_ast(ast1)
    print("\nAST Structure for Rule 2:")
    print_ast(ast2)

    # Combine rules
    combined_ast = combine_rules([rule1, rule2])
    print("\nCombined AST Structure:")
    print_ast(combined_ast)

    # Evaluate the combined rule with sample data
    sample_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    result = evaluate_rule(combined_ast, sample_data)
    print("\nEvaluation Result:", result)
